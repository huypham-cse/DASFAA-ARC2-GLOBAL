"""Rebuild the six frozen B1c/B2 review figures without writing to results/.

Requires NumPy, SciPy and Matplotlib. Uses the archived rendering helpers and
their exact saved means/intervals; never accesses qrels, fits or resamples.
Example: python reproduce/rebuild_review_figures.py --root .
Default output: checks/rebuilt_figures/<unique-UTC-timestamp>/.
An explicit --output must name a directory that does not already exist.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def output_path(root, value):
    path = Path(value)
    path = (root / path).resolve() if not path.is_absolute() else path.resolve()
    protected = ('results', 'src', 'ops', 'configs', 'protocols', 'tools', 'reproduce', 'manuscript')
    if path == root or any(path.is_relative_to(root / name) for name in protected):
        raise ValueError('Choose an output outside the frozen source/evidence directories, such as checks/rebuilt_figures')
    return path


def load_renderer(root, name):
    path = root / 'tools' / f'{name}.py'
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Cannot import archived renderer: {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


def latest_qa(bundle):
    paths = sorted(bundle.glob('qa_completed_*.json'))
    if not paths:
        raise FileNotFoundError(f'No completed independent QA receipt in {bundle}')
    # Do not silently fall back to an older receipt if the most recent fails.
    path = paths[-1]
    if json.loads(path.read_text(encoding='utf-8-sig')).get('status') != 'PASS':
        raise ValueError(f'Most recent independent QA is not PASS: {path}')
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, default=None,
        help='New output directory; omitted: checks/rebuilt_figures/<UTC timestamp>')
    args = parser.parse_args()
    root = args.root.resolve()
    run_stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    requested_output = args.output if args.output is not None else Path('checks/rebuilt_figures') / run_stamp
    out = output_path(root, requested_output)
    out.mkdir(parents=True, exist_ok=False)
    sources, outputs, counts = {}, [], {}
    for stage, folder, renderer_name in (
        ('B1c', 'b1c_r3_review_20261031', 'render_b1c_r3_report'),
        ('B2', 'b2_review_20261101', 'render_b2_report'),
    ):
        module, renderer_path = load_renderer(root, renderer_name)
        bundle = root / 'results' / folder
        qa_path = latest_qa(bundle)
        saved = module.verified_summary(bundle, qa_path)
        summary, summary_path, lookup = saved[:3]
        # Both archived styles are self-contained Matplotlib rcParams. Their
        # historical external skill paths are citations only, never imported.
        plt, _ = module.style()
        target = out / stage.lower()
        target.mkdir(exist_ok=True)
        for metric in ('ndcg10', 'recall100'):
            result = module.quality_figure(plt, lookup, target, metric)
            if stage == 'B1c':
                outputs.extend(result)
            else:
                paths, data = result
                outputs.extend(paths)
                data_path = target / f'figure_{metric}_values.csv'
                module.write_csv(data_path, data)
                outputs.append(data_path)
        if stage == 'B1c':
            outputs.extend(module.contrast_figure(plt, summary, target))
        else:
            paths, data = module.forest_figure(plt, saved[3], target)
            outputs.extend(paths)
            data_path = target / 'figure_primary_contrasts.csv'
            module.write_csv(data_path, data)
            outputs.append(data_path)
        for path in (renderer_path, summary_path, qa_path, summary_path.with_name('completed.json')):
            sources[path.relative_to(root).as_posix()] = sha256(path)
        counts[stage] = {'ranking_cells': summary['ranking_cells'], 'condition_means': len(summary['means']),
            'primary_contrasts': len(summary['aggregate_contrasts']) if stage == 'B1c' else len(summary['contrasts']),
            'source_summary_sha256': sha256(summary_path)}
    poppler = shutil.which('pdftoppm')
    preview_errors, preview_count = [], 0
    if poppler:
        for path in list(outputs):
            if path.suffix != '.pdf':
                continue
            prefix = path.parent / 'previews' / (path.stem + '_pdf')
            prefix.parent.mkdir(exist_ok=True)
            try:
                subprocess.run([poppler, '-f', '1', '-singlefile', '-scale-to', '1800', '-png', str(path), str(prefix)],
                    check=True, capture_output=True)
                outputs.append(prefix.with_suffix('.png'))
                preview_count += 1
            except (OSError, subprocess.CalledProcessError) as exc:
                preview_errors.append({'figure': path.relative_to(out).as_posix(), 'error': str(exc)})
    import matplotlib
    import numpy
    receipt = {'status': 'PASS', 'generated_utc': datetime.now(timezone.utc).isoformat(),
        'operation': 'Saved-score figure rebuild only; no qrels/scoring/fitting/resampling; frozen results untouched.',
        'python': platform.python_version(), 'numpy': numpy.__version__, 'matplotlib': matplotlib.__version__,
        'renderer_style': 'Archived self-contained Matplotlib helpers; no external style repository required.',
        'formats': ['pdf', 'svg', 'png'], 'png_dpi': 300,
        'pdf_preview_count': preview_count, 'optional_pdf_preview_errors': preview_errors,
        'pdf_previews': 'optional pdftoppm attempted' if poppler else 'skipped; optional pdftoppm not installed',
        'entrypoint_sha256': sha256(__file__),
        'output_selection': 'unique UTC timestamp default' if args.output is None else 'explicit exclusive directory',
        'figure_count': 6, 'matrix_counts': counts, 'source_sha256': sources,
        'outputs': {p.relative_to(out).as_posix(): {'sha256': sha256(p), 'bytes': p.stat().st_size} for p in outputs}}
    (out / 'rebuild_receipt.json').write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'figures': 6, 'output': str(out), 'pdf_previews': preview_count}, indent=2))


if __name__ == '__main__':
    main()

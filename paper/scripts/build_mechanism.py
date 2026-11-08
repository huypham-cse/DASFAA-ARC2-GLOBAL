"""Build the editable Computer-Modern TikZ mechanism, inspired by the user's v2."""
from pathlib import Path
import subprocess
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]

def main():
    src=ROOT/'figures'/'mechanism.tex'
    dest=ROOT/'build'/'mechanism'
    dest.mkdir(parents=True,exist_ok=True)
    p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                      '-output-directory='+str(dest),str(src)],cwd=ROOT,
                     capture_output=True,text=True,encoding='utf-8',errors='replace')
    (dest/'build_stdout.txt').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
    if p.returncode:
        raise RuntimeError((p.stdout+p.stderr)[-5000:])
    pdf=ROOT/'figures'/'mechanism.pdf'
    pdf.write_bytes((dest/'mechanism.pdf').read_bytes())
    subprocess.run(['pdftoppm','-r','400','-png','-singlefile',str(pdf),str(pdf.with_suffix(''))],check=True,capture_output=True)
    subprocess.run(['pdftocairo','-svg',str(pdf),str(pdf.with_suffix('.svg'))],check=True,capture_output=True)
    record={'kind':'worked migration schematic, toy24; not measured ranking or deployment cost',
            'method':'arc2_global_tangent2_r1','typography':'native LaTeX/TikZ, Computer Modern',
            'visual_reference':'D:/DASFAA-2027-MixIndex/figures/fig_arc2_mechanism_v2.png',
            'algorithm_reference':'src/arc2_global/model.py',
            'initialization':'centered rectangular Procrustes',
            'tangent_steps':2,'lambda':10,'local_residual':False,
            'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'outputs':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [pdf,pdf.with_suffix('.svg'),pdf.with_suffix('.png')]}}
    (ROOT/'review'/'mechanism_provenance.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('Built LaTeX/TikZ mechanism.pdf, .svg, .png')

if __name__=='__main__':main()

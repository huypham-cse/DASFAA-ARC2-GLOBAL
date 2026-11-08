"""Run only synthetic whole-group recovery checks, with no scientific inputs."""
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ops'))
from b1c_recovery import synthetic_checks

if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='b1c_recovery_synthetic_') as directory:
        print(json.dumps(synthetic_checks(Path(directory) / 'fixture'), indent=2))

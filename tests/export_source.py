#!/usr/bin/env python3
"""Export audited source only, without creating a Git repository or uploading."""
from pathlib import Path
import argparse
import subprocess
import sys
import zipfile

from release_audit import ROOT, ignored


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='New .zip path outside the project; refuses overwrite')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output == ROOT or ROOT in output.parents or output.suffix != '.zip' or output.exists():
        parser.error('Use a new .zip path outside the project; existing files are never overwritten')
    result = subprocess.run([sys.executable, str(ROOT / 'tests/release_audit.py')])
    if result.returncode:
        return result.returncode
    paths = [path for path in ROOT.rglob('*') if path.is_file() and not ignored(path.relative_to(ROOT))]
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(paths):
            archive.write(path, Path('hainan-thesis-reference') / path.relative_to(ROOT))
    print(f'Exported {len(paths)} source files. No Git repository or upload was created.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

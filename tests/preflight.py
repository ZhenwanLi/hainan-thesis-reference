#!/usr/bin/env python3
"""Dependency checks without installing software or changing the environment."""
import shutil
import subprocess
import sys

TOOLS = ['bash', 'xelatex', 'bibtex', 'kpsewhich', 'pdfinfo', 'pdffonts', 'pdftotext']
FILES = ['ctexart.cls', 'fontspec.sty', 'xeCJK.sty', 'geometry.sty', 'amsmath.sty',
         'amssymb.sty', 'booktabs.sty', 'caption.sty', 'titlesec.sty', 'tocloft.sty',
         'fancyhdr.sty', 'hyperref.sty', 'gbt7714.sty', 'etoolbox.sty', 'tabularx.sty',
         'longtable.sty', 'listings.sty', 'perpage.sty', 'tikz.sty', 'pgfplots.sty',
         'setspace.sty', 'gbt7714-2015-numeric.bst', 'FandolSong-Regular.otf',
         'FandolSong-Bold.otf', 'FandolHei-Regular.otf', 'FandolHei-Bold.otf',
         'FandolKai-Regular.otf', 'FandolFang-Regular.otf', 'texgyretermes-regular.otf',
         'texgyretermes-bold.otf', 'texgyretermes-italic.otf', 'texgyretermes-bolditalic.otf']


def main():
    missing = [tool for tool in TOOLS if not shutil.which(tool)]
    if sys.version_info < (3, 10):
        missing.append('Python >= 3.10')
    if shutil.which('kpsewhich'):
        for filename in FILES:
            result = subprocess.run(['kpsewhich', filename], capture_output=True, text=True)
            if result.returncode or not result.stdout.strip():
                missing.append(filename)
    if missing:
        print('Missing dependencies: ' + ', '.join(missing))
        print('See docs/BUILD.md. No software was installed automatically.')
        return 1
    print('PASS dependencies (open-font preview; no Microsoft fonts required)')
    print(subprocess.check_output(['xelatex', '--version'], text=True).splitlines()[0])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

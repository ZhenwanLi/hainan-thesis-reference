#!/usr/bin/env python3
"""Targeted fixtures: counter resets, page-local notes, multi-page contents."""
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports/structure'


def run_tex(work):
    for _ in range(3):
        result = subprocess.run(['xelatex', '-no-shell-escape', '-halt-on-error', '-interaction=nonstopmode', 'probe.tex'],
                                cwd=work, capture_output=True, text=True, timeout=90)
        if result.returncode:
            raise AssertionError(result.stdout[-3000:])
    return (work / 'probe.log').read_text(errors='replace')


def main():
    REPORT.mkdir(parents=True, exist_ok=True)
    outcomes = []
    for category in ['science', 'humanities', 'foreign', 'art']:
        with tempfile.TemporaryDirectory(prefix='thesis-structure-') as temp:
            work = Path(temp)
            for filename in ['hntouthesis.cls', 'fonts.tex']:
                shutil.copy2(ROOT / 'templates/海南热带海洋学院' / filename, work / filename)
            (work / 'probe.tex').write_text(r'''\documentclass[CATEGORY]{hntouthesis}
\begin{document}\hntbodylayout\pagestyle{hntmain}
\section{First}
\refstepcounter{figure}\typeout{FIG-A=\thefigure}
\refstepcounter{table}\typeout{TAB-A=\thetable}
\refstepcounter{equation}\typeout{EQ-A=\theequation}
\refstepcounter{figure}\typeout{FIG-B=\thefigure}
First\footnote{First note\label{note:first}}.
Second\footnote{Second note\label{note:second}}.
\clearpage
\section{Second}
\refstepcounter{figure}\typeout{FIG-C=\thefigure}
\refstepcounter{table}\typeout{TAB-C=\thetable}
\refstepcounter{equation}\typeout{EQ-C=\theequation}
Third\footnote{Third note\label{note:third}}.
\end{document}'''.replace('CATEGORY', category), encoding='utf-8')
            log = run_tex(work)
            (REPORT / f'{category}.log').write_text(log)
            for label, expected in [('FIG-A', '1.1'), ('TAB-A', '1.1'), ('EQ-A', '1.1'),
                                    ('FIG-B', '1.2'), ('FIG-C', '2.1'), ('TAB-C', '2.1'), ('EQ-C', '2.1')]:
                assert f'{label}={expected}' in log, f'{category}: {label} != {expected}'
            aux = (work / 'probe.aux').read_text()
            notes = {}
            for key in ['first', 'second', 'third']:
                line = next(line for line in aux.splitlines() if line.startswith('\\newlabel{note:' + key + '}'))
                notes[key] = line.split('{{', 1)[1].split('}{', 1)[0]
            assert notes['first'] == notes['third'] != notes['second'], f'Note reset failed: {notes}'
            assert not re.search(r'Missing character:|Overfull|Warning:', log), f'Unexpected fixture warning: {category}'
            outcomes.append(dict(test='counters_and_page_notes', category=category, success=True))

    with tempfile.TemporaryDirectory(prefix='thesis-toc-') as temp:
        work = Path(temp)
        for filename in ['style.tex', 'fonts.tex']:
            shutil.copy2(ROOT / 'templates/海南医科大学' / filename, work / filename)
        source = r'''\documentclass[12pt,a4paper,fontset=none]{ctexart}
\input{style}\begin{document}\pagestyle{empty}
\tableofcontents\clearpage
\section*{ContentStartMarker}
'''
        source += ''.join('\\section{Entry ' + str(i) + '}Text.\\par\n' for i in range(85))
        source += '\\end{document}\n'
        (work / 'probe.tex').write_text(source)
        run_tex(work)
        xml = subprocess.check_output(['pdftotext', '-bbox', str(work / 'probe.pdf'), '-'], text=True)
        tree = ET.fromstring(xml[xml.index('<html'):])
        namespace = {'h': 'http://www.w3.org/1999/xhtml'}
        toc_pages = 0
        for page in tree.findall('.//h:page', namespace):
            words = page.findall('.//h:word', namespace)
            if any(word.text == 'ContentStartMarker' for word in words):
                break
            toc_pages += 1
            footer = [word.text for word in words if float(word.attrib['yMin']) > 760
                      and re.fullmatch(r'[0-9IVXLCDMivxlcdm]+', word.text or '')]
            assert not footer, f'Contents page {toc_pages} has footer numbers: {footer}'
        assert toc_pages >= 2, 'Fixture did not create multi-page contents'
        outcomes.append(dict(test='medical_multipage_toc', pages=toc_pages, success=True))

    (REPORT / 'result.json').write_text(json.dumps(outcomes, ensure_ascii=False, indent=2))
    for outcome in outcomes:
        print('PASS', outcome)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

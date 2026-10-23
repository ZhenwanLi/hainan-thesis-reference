#!/usr/bin/env python3
"""编译本轮新增/改造的9个入口，并记录PDF、字体和最终日志检查结果。"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
import os
import json
import hashlib
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports'
TARGETS = [
    ('海南热带海洋学院', 'main'),
    ('海南热带海洋学院', 'main-humanities'),
    ('海南热带海洋学院', 'main-foreign'),
    ('海南热带海洋学院', 'main-art'),
    ('海口经济学院', 'main'),
    ('琼台师范学院', 'main'),
    ('海南医科大学', 'main'),
    ('三亚学院', 'main'),
    ('海南科技职业大学', 'main'),
]


def validate_school(school):
    results = []
    directory = ROOT / 'templates' / school
    for _, target in [x for x in TARGETS if x[0] == school]:
        name = f'{school}-{target}'
        args = ['bash', 'compile.sh']
        if school == '海南热带海洋学院':
            args.append(target)
        with (REPORT / f'{name}-编译输出.txt').open('w') as stream:
            try:
                completed = subprocess.run(args, cwd=directory, stdout=stream,
                                           stderr=subprocess.STDOUT, timeout=180)
            except subprocess.TimeoutExpired:
                stream.write('\nFAIL：编译超时（180秒）\n')
                completed = subprocess.CompletedProcess(args, 124)
        build = directory / '.build' / target
        logpath = build / f'{target}.log'
        text = logpath.read_text(errors='replace') if logpath.exists() else ''
        if logpath.exists():
            shutil.copy2(logpath, REPORT / f'{name}.log')
        biblog = build / f'{target}.blg'
        bibtext = biblog.read_text(errors='replace') if biblog.exists() else ''
        if biblog.exists():
            shutil.copy2(biblog, REPORT / f'{name}.blg')
        issues = {key: len(re.findall(pattern, text, re.M)) for key, pattern in {
            'errors': r'^!|^.*LaTeX Error:|Undefined control sequence',
            'missing_glyphs': r'Missing character:',
            'overfull': r'Overfull \\[hv]box',
            'undefined_references': r'(?:Reference|Citation).*undefined|There were undefined',
            'warnings': r'Warning:',
        }.items()}
        issues['bibtex_issues'] = len(re.findall(r'Warning--|error message|I couldn.t open|while executing---', bibtext))
        pdf = directory / f'{target}.pdf'
        pages, fonts_embedded = None, False
        if completed.returncode == 0 and pdf.exists():
            info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
            pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1])
            fontinfo = subprocess.check_output(['pdffonts', str(pdf)], text=True)
            (REPORT / f'{name}-字体.txt').write_text(fontinfo)
            fontrows = fontinfo.splitlines()[2:]
            # 最后五列为 emb/sub/uni/object/ID，所有字体均须嵌入。
            fonts_embedded = bool(fontrows) and all(row.split()[-5] == 'yes' for row in fontrows)
        bibliography_expected = target != 'main-art'
        success = (completed.returncode == 0 and logpath.exists()
                   and (not bibliography_expected or biblog.exists())
                   and pages is not None and fonts_embedded and not any(issues.values()))
        result = dict(school=school, target=target, pages=pages, returncode=completed.returncode,
                      fonts_embedded=fonts_embedded, success=success, **issues)
        results.append(result)
        print(f'{"PASS" if success else "FAIL"} {school}/{target}: {pages}页 {issues}', flush=True)
    return results


def main():
    REPORT.mkdir(exist_ok=True)
    schools = list(dict.fromkeys(school for school, _ in TARGETS))
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = [result for group in executor.map(validate_school, schools) for result in group]
    regression = subprocess.run([sys.executable, str(ROOT / 'tests/check_medical_toc.py')],
                                capture_output=True, text=True)
    (REPORT / '海医目录回归检查.txt').write_text(regression.stdout + regression.stderr)
    print(regression.stdout, end='')
    data = dict(timestamp=datetime.now().astimezone().isoformat(),
                font_mode=os.environ.get('THESIS_FONTS', 'preview'),
                scope='本轮新增与改造的9个入口；不重复验证海大海师',
                results=results, medical_toc_regression=regression.returncode == 0)
    (REPORT / '验证结果.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
    hashes = {}
    for school in schools:
        for path in (ROOT / 'templates' / school).rglob('*'):
            if '.build' not in path.parts and path.is_file() and path.suffix in {'.tex', '.cls', '.bib', '.bst', '.sh', '.pdf'}:
                hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    (REPORT / '源码与PDF校验.json').write_text(json.dumps(hashes, ensure_ascii=False, indent=2))
    return 0 if all(r['success'] for r in results) and regression.returncode == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())

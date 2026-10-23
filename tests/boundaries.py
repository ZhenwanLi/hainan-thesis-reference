#!/usr/bin/env python3
"""独立临时副本测试长字段、排序、固定行距，不改正式论文或文献库。"""
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports' / 'boundaries'
SCHOOLS = ['海南热带海洋学院', '海口经济学院', '琼台师范学院',
           '海南医科大学', '三亚学院', '海南科技职业大学']
ENV = dict(os.environ)
NS = {'h': 'http://www.w3.org/1999/xhtml'}


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def run(args, cwd):
    result = subprocess.run(args, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=180)
    check(result.returncode == 0, result.stdout[-5000:] + result.stderr[-1000:])
    return result.stdout


def long_cover(school):
    with tempfile.TemporaryDirectory(prefix='thesis-cover-') as temp:
        work = Path(temp) / '独立 模板副本'
        shutil.copytree(ROOT / 'templates' / school, work,
                        ignore=shutil.ignore_patterns('.build', '*.pdf', '*.aux', '*.log', '*.bbl', '*.blg', '*.toc', '*.out'))
        prefix = 'hnt' if school == SCHOOLS[0] else 'thesis'
        overrides = {
            f'{prefix}title': '面向海南自贸港多场景应用的复杂系统设计与服务质量评价方法研究',
            f'{prefix}major': '数据科学与大数据技术及跨学科应用方向',
            f'{prefix}advisor': '李明教授与王华企业高级工程师',
        }
        if prefix == 'hnt':
            overrides.update(hntcollege='海洋信息与数字技术跨学科研究学院',
                             hntadvisorB='赵明企业高级工程师')
        else:
            college_macro = 'thesisschool' if school in SCHOOLS[1:3] else 'thesiscollege'
            if school != '海南医科大学':
                overrides[college_macro] = '信息技术与现代服务产业交叉研究学院'
        code = '\\AtBeginDocument{' + ''.join(
            '\\renewcommand{\\' + key + '}{' + value + '}' for key, value in overrides.items()) + '}\n'
        main = work / 'main.tex'
        main.write_text(main.read_text().replace('\\begin{document}', code + '\\begin{document}', 1))
        if school == '海口经济学院':
            # 纯汉字题名避免xeCJK标点压缩/悬挂影响提取文字框的几何中心。
            chapter = work / 'chapters/research-practice.tex'
            chapter.write_text(chapter.read_text().replace('合成数据示例（非模型测试结果）', '合成数据排版示例'))
        # 从模板外启动，且副本路径含中文和空格，检查可独立使用。
        output = run(['bash', str(work / 'compile.sh')], Path(temp))
        log = (work / '.build/main/main.log').read_text(errors='replace')
        check(not re.search(r'Overfull|Missing character:|Warning:|^!', log, re.M), '长字段引发排版或编译警告')
        bbox = subprocess.check_output(['pdftotext', '-bbox', str(work / 'main.pdf'), '-'], text=True)
        root = ET.fromstring(bbox[bbox.index('<html'):])
        first = root.findall('.//h:page', NS)[0]
        words = first.findall('.//h:word', NS)
        width, height = float(first.attrib['width']), float(first.attrib['height'])
        check(bool(words), '封面没有提取到文字')
        for word in words:
            check(float(word.attrib['xMin']) >= 40 and float(word.attrib['xMax']) <= width - 40
                  and float(word.attrib['yMin']) >= 30 and float(word.attrib['yMax']) <= height - 25,
                  f'封面文字越过安全边界：{word.text} {word.attrib}')
        covertext = subprocess.check_output(['pdftotext', '-layout', '-f', '1', '-l', '1', str(work / 'main.pdf'), '-'], text=True)
        shutil.copy2(work / 'main.pdf', REPORT / f'{school}-长字段.pdf')
        (REPORT / f'{school}-封面文字.txt').write_text(covertext)
        normalized = re.sub(r'\s', '', covertext)
        for text in overrides.values():
            # Multiline table cells can interleave with row labels in PDF reading
            # order. Count glyphs on the first page instead of assuming one stream.
            required = Counter(text)
            available = Counter(normalized)
            check(all(available[char] >= count for char, count in required.items()),
                  f'封面字段被挤到下一页或缺失：{text}')
        shutil.copy2(work / 'main.pdf', REPORT / f'{school}-长字段.pdf')
        (REPORT / f'{school}-长字段.log').write_text(log)
        (REPORT / f'{school}-编译输出.txt').write_text(output)
        check(not list(work.glob('*.aux')) and not list(work.glob('*.log')),
              '编译中间文件污染了源码根目录')
        if school == '海口经济学院':
            title_words = []
            for page in root.findall('.//h:page', NS):
                candidates = page.findall('.//h:word', NS)
                for word in candidates:
                    if word.text == '合成数据排版示例':
                        title_words.append(word)
                        same_line = [item for item in candidates
                                     if abs(float(item.attrib['yMin']) - float(word.attrib['yMin'])) < 2]
                        units = [item for item in same_line if item.text == '单位见列题']
                        labels = [item for item in same_line if (item.text or '').startswith('表')]
                        check(bool(units) and bool(labels), '三栏表题缺少表号或单位')
                        center = (float(word.attrib['xMin']) + float(word.attrib['xMax'])) / 2
                        # 海经正文左右边距不对称，以版心而不是纸张中心检验。
                        expected_center = (25 * 72 / 25.4 + float(page.attrib['width']) - 20 * 72 / 25.4) / 2
                        check(abs(center - expected_center) < 2, '表题没有在版心居中')
                        check(float(labels[0].attrib['xMax']) < float(word.attrib['xMin'])
                              and float(units[0].attrib['xMin']) > float(word.attrib['xMax']), '表号/题名/单位发生交叠')
            check(len(title_words) == 1, '未唯一定位三栏表题')
            # 失败编译不能用半成品覆盖上一次成功PDF。
            old_pdf = (work / 'main.pdf').read_bytes()
            main.write_text(main.read_text().replace('\\begin{document}',
                            '\\begin{document}\\ThisCommandMustFailForRegression', 1))
            failed = subprocess.run(['bash', str(work / 'compile.sh')], cwd=temp, env=ENV,
                                    capture_output=True, text=True, timeout=180)
            check(failed.returncode != 0, '故意损坏的源码没有让脚本失败')
            check((work / 'main.pdf').read_bytes() == old_pdf, '失败编译覆盖了旧PDF')
    return dict(test='long_cover', school=school, success=True,
                standalone_copy=True, external_cwd=True, clean_source_directory=True,
                failure_keeps_pdf=True if school == '海口经济学院' else None)


def bibliography():
    source = ROOT / 'templates/海口经济学院/hkcu-gbt7714.bst'
    with tempfile.TemporaryDirectory(prefix='thesis-bib-') as temp:
        work = Path(temp)
        shutil.copy2(source, work / source.name)
        entries = [
            ('en-paper-old', 'article', 'english', 2000, ''),
            ('zh-book-new', 'book', 'chinese', 2025, ''),
            ('zh-paper-old', 'article', 'chinese', 2010, ''),
            ('en-paper-new', 'article', 'english', 2024, ''),
            ('zh-paper-tie-b', 'article', 'chinese', 2020, ''),
            ('zh-paper-new', 'article', 'chinese', 2023, ''),
            ('en-book-new', 'book', 'english', 2026, ''),
            ('zh-paper-tie-a', 'article', 'chinese', 2020, ''),
            ('zh-report', 'techreport', 'chinese', 2026, ''),
            ('en-report-as-paper', 'techreport', 'english', 2025, 'paper'),
            ('not-cited', 'article', 'chinese', 2026, ''),
        ]
        database = []
        for key, kind, lang, year, group in entries:
            database.append('@' + kind + '{' + key + ',\n'
                            + f'author={{Example, Test}}, title={{Synthetic test entry}}, year={{{year}}},\n'
                            + f'language={{{lang}}}, journal={{Test Journal}}, volume={{1}}, pages={{1--2}},\n'
                            + 'publisher={Test Publisher}, address={Test City}, institution={Test Institute},\n'
                            + (f'hkcuclass={{{group}}},\n' if group else '') + '}\n')
        (work / 'fixture.bib').write_text(''.join(database))
        cited = [entry[0] for entry in entries if entry[0] != 'not-cited']
        aux = '\\relax\n\\citation{' + ','.join(cited) + '}\n\\bibstyle{hkcu-gbt7714}\n\\bibdata{fixture}\n'
        (work / 'fixture.aux').write_text(aux)
        run(['bibtex', 'fixture'], work)
        bbl = (work / 'fixture.bbl').read_text()
        actual = re.findall(r'\\bibitem\[[^\n]*\]\{([^}]+)\}', bbl)
        expected = ['zh-paper-new', 'zh-paper-tie-a', 'zh-paper-tie-b', 'zh-paper-old', 'zh-book-new',
                    'zh-report', 'en-report-as-paper', 'en-paper-new', 'en-paper-old', 'en-book-new']
        check(actual == expected, f'书目顺序错误：{actual} != {expected}')
        # 反转引用顺序，证明不是依赖首次引用或nocite列表的偶然结果。
        (work / 'fixture.aux').write_text(aux.replace(','.join(cited), ','.join(reversed(cited))))
        run(['bibtex', 'fixture'], work)
        bbl_reversed = (work / 'fixture.bbl').read_text()
        check(re.findall(r'\\bibitem\[[^\n]*\]\{([^}]+)\}', bbl_reversed) == expected,
              '引用顺序改变导致书目顺序变化')
        (REPORT / '文献排序测试.bbl').write_text(bbl_reversed)
        (REPORT / '文献排序测试.blg').write_text((work / 'fixture.blg').read_text())
        # 缺年与非法年必须明确警告，而非悄悄给出似乎正确的排序。
        for year, key in [('', 'missing-year'), ('20xx', 'invalid-year')]:
            (work / 'bad.bib').write_text('@book{' + key + ',author={Example, Test},title={Synthetic},'
                                        + f'year={{{year}}},publisher={{Test}},address={{Test City}}' + '}')
            (work / 'bad.aux').write_text('\\relax\n\\citation{' + key
                                        + '}\n\\bibstyle{hkcu-gbt7714}\n\\bibdata{bad}\n')
            result = subprocess.run(['bibtex', 'bad'], cwd=work, env=ENV, capture_output=True, text=True)
            check('Warning--HKCU:' in result.stdout, f'{key}没有产生预期警告')
            (REPORT / f'{key}.blg').write_text((work / 'bad.blg').read_text())
    return dict(test='bibliography_sort', success=True, expected=expected)


def baseline():
    with tempfile.TemporaryDirectory(prefix='thesis-line-') as temp:
        work = Path(temp)
        for name in ['hntouthesis.cls', 'fonts.tex']:
            shutil.copy2(ROOT / 'templates/海南热带海洋学院' / name, work / name)
        results = {}
        for category, expected in [('science', 20), ('humanities', 20), ('foreign', 22), ('art', 20)]:
            source = r'''\documentclass[CATEGORY]{hntouthesis}
\begin{document}\hntbodylayout
\typeout{BASELINE-BEFORE=\the\baselineskip}
\section{Heading}\noindent Example text.\par
\typeout{BASELINE-AFTER=\the\baselineskip}
{\small Small text.\par}\normalsize
\typeout{BASELINE-RESTORE=\the\baselineskip}
\end{document}'''.replace('CATEGORY', category)
            (work / 'probe.tex').write_text(source)
            run(['xelatex', '-halt-on-error', '-interaction=nonstopmode', 'probe.tex'], work)
            log = (work / 'probe.log').read_text(errors='replace')
            values = re.findall(r'BASELINE-(?:BEFORE|AFTER|RESTORE)=([\d.]+)pt', log)
            expected_pt = expected * 72.27 / 72
            check(len(values) == 3 and all(abs(float(v) - expected_pt) < .03 for v in values),
                  f'{category}基线行距错误：{values}，应为{expected_pt}pt')
            results[category] = values
    return dict(test='fixed_baselines', success=True, values_pt=results)


def main():
    REPORT.mkdir(parents=True, exist_ok=True)
    outcomes = []

    def guarded(task):
        name, function = task
        try:
            result = function()
        except Exception as error:
            result = dict(test=name, success=False, error=str(error))
        print(('PASS ' if result['success'] else 'FAIL ') + name, flush=True)
        return result

    tasks = [(school, lambda school=school: long_cover(school)) for school in SCHOOLS]
    tasks += [('文献自动排序', bibliography), ('四类固定行距', baseline)]
    with ThreadPoolExecutor(max_workers=4) as executor:
        outcomes = list(executor.map(guarded, tasks))
    (REPORT / '结果.json').write_text(json.dumps(outcomes, ensure_ascii=False, indent=2))
    return 0 if all(result['success'] for result in outcomes) else 1


if __name__ == '__main__':
    raise SystemExit(main())

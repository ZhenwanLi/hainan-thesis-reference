#!/usr/bin/env python3
"""回归检查：实际PDF目录标题居中，且前置目录没有意外底部页码。"""
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

pdf = Path(__file__).resolve().parents[1] / 'templates/海南医科大学/main.pdf'
xml = subprocess.check_output(['pdftotext', '-bbox', str(pdf), '-']).decode()
root = ET.fromstring(xml[xml.index('<html'):])
ns = {'h': 'http://www.w3.org/1999/xhtml'}
pages = root.findall('.//h:page', ns)
matches = []
for index, candidate in enumerate(pages, 1):
    for word in candidate.findall('.//h:word', ns):
        if word.text == '目录' and float(word.attrib['yMin']) < 180:
            matches.append((index, candidate, word))
assert len(matches) == 1, f'FAIL：预期恰好一个目录标题，实际找到{len(matches)}个'
index, page, title = matches[0]
words = page.findall('.//h:word', ns)
center = (float(title.attrib['xMin']) + float(title.attrib['xMax'])) / 2
expected = float(page.attrib['width']) / 2
bottom_numbers = [w.text for w in words if float(w.attrib['yMin']) > 760 and (w.text or '').isdigit()]
print(f'目录在第{index}个物理页，中心 x={center:.2f}pt，页面中心={expected:.2f}pt；前置页底部数字={bottom_numbers}')
assert abs(center - expected) < 3, 'FAIL：目录标题没有居中'
assert not bottom_numbers, 'FAIL：前置目录出现了意外页码'
print('PASS：海医目录标题与前置页码')

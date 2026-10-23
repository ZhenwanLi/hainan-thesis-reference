# Hainan Thesis Reference — Unofficial LaTeX Thesis Templates

[![Preview validation](https://github.com/ZhenwanLi/hainan-thesis-reference/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/ZhenwanLi/hainan-thesis-reference/actions/workflows/validate.yml)

[中文](README.md) · English · [Build guide (Chinese)](docs/BUILD.md) · [FAQ (Chinese)](docs/FAQ.md) · [Report an issue](https://github.com/ZhenwanLi/hainan-thesis-reference/issues/new/choose)

An **unofficial collection of LaTeX thesis reference templates for universities in Hainan, China**, built with XeLaTeX, CTeX and BibTeX. Includes six institution directories, nine compilation entry points, Chinese/English writing examples, official-source links and automated validation.

**Not endorsed or certified by any university.** Successful compilation does not establish compliance with current departmental rules or permission to submit PDF instead of Word. All sample research text and data are illustrative, not actual findings.

## Templates and limits

Institution names below link directly to their scope notes. Chinese names are kept to match the source documents and directory names.

| Institution | What is included | Important limitation |
|---|---|---|
| [海南热带海洋学院](templates/海南热带海洋学院/README.md) | Four entries: science/engineering, humanities, foreign-language and art | Reconstructed from historical formatting materials; current requirements unconfirmed |
| [海口经济学院](templates/海口经济学院/README.md) | Reference based on the 2026-cohort attachment | Official instructions require an electronic Word document |
| [海南医科大学](templates/海南医科大学/README.md) | Pharmacy undergraduate reference based on 2019 rules only | Not a university-wide or graduate thesis template; cover/declaration placeholders |
| [琼台师范学院](templates/琼台师范学院/README.md) | Structural reference based on 2021 regulations | Detailed current formatting and declarations need verification |
| [三亚学院](templates/三亚学院/README.md) | Structural draft with editable examples | Department-approved current Word template not obtained |
| [海南科技职业大学](templates/海南科技职业大学/README.md) | Structural reference based on regulations effective from the 2026 cohort | Dedicated writing specifications/template not obtained |

海南大学 and 海南师范大学 have **upstream links only**, not bundled templates. See the [source index](sources/README.md). This project does not cover every Hainan institution or degree level.

## Features

- Editable abstracts, contents, chapters, figures, tables, equations, footnotes, code and appendices.
- Explicit GB/T 7714-2015 bibliography baseline; not a verified requirement for every institution.
- Open-font preview using Fandol and TeX Gyre Termes; no proprietary font files distributed.
- Separate school-font mode, requiring legally installed fonts; preview pagination may differ.
- Build outputs isolated in `.build/`; the final PDF is replaced only after a successful build.
- CI checks compilation, references, missing glyphs, font embedding, boundary cases and document structure.

## Quick start

Tested target: Linux, Bash, Python 3.10+, TeX Live 2026 and Poppler utilities. Install dependencies using the [build guide](docs/BUILD.md) first. Windows/macOS and Overleaf have not been validated end to end.

```bash
git clone https://github.com/ZhenwanLi/hainan-thesis-reference.git
cd hainan-thesis-reference
python3 tests/preflight.py
bash templates/海南热带海洋学院/compile.sh
```

Choose a different institution by running its `compile.sh`. For the humanities entry:

```bash
bash templates/海南热带海洋学院/compile.sh main-humanities
```

Read the institution README before editing. A PDF from a previous successful build may remain after a failed build: always check the exit status and log, not just whether a PDF exists.

## Validation

```bash
python3 tests/test_ci_profile.py
python3 tests/test_ci_texlive.py
python3 tests/compile_all.py
python3 tests/boundaries.py
python3 tests/structure.py
python3 tests/release_audit.py
```

The [validation record](docs/VALIDATION.md) identifies tested commits and limitations. CI installs a network-supplied TeX Live 2026 environment, not a fully pinned package snapshot. A green build is not academic, legal or university approval.

## Sources, licensing and contributions

- [Source index](sources/README.md): scope, dates, public links and missing materials.
- [Third-party notices](THIRD_PARTY_NOTICES.md): original project code/docs use MIT; the derived Haikou bibliography style remains under LPPL with upstream attribution.
- [Contributing](CONTRIBUTING.md): include institution, department, degree level, cohort and official source URL when proposing format changes.
- [Issue forms](https://github.com/ZhenwanLi/hainan-thesis-reference/issues/new/choose): build failures and source/format corrections.

Do not upload real student papers, signatures, medical records, private information, proprietary fonts or unreviewed official attachments. Share public source links and redacted minimal examples instead.

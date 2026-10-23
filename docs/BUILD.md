# 安装与构建

## 支持范围

开发验证以Linux、Bash、Python 3.10+、TeX Live 2026为目标。macOS可尝试MacTeX和Poppler，Windows可尝试WSL，但本项目尚未实测这些平台，不承诺原生PowerShell兼容。

脚本只使用PATH查找命令，不写死个人TeX目录，也不自动安装软件。安装完后按自己的发行版设置PATH，例如将TeX Live的`bin/<平台>`加入PATH。

## 依赖

- `xelatex`、`bibtex`、`kpsewhich`。
- TeX宏包：ctex、fontspec、xeCJK、geometry、amsmath、amssymb、booktabs、caption、titlesec、tocloft、fancyhdr、hyperref、gbt7714、etoolbox、tabularx、longtable、listings、perpage、tikz、pgfplots、setspace等。
- TeX字体包：fandol、tex-gyre；不用安装微软字体就可预览。
- `gbt7714`须提供`gbt7714-2015-numeric.bst`；本机验证版本为2026-09-27 v3.1.1，旧发行版可能缺少该显式年份样式。预检会直接提示，不能静默回退无年份别名。
- Python 3.10+，测试仅用标准库，无pip依赖。
- Poppler工具：`pdfinfo`、`pdffonts`、`pdftotext`。Ubuntu/Debian可安装`poppler-utils`，它不属于TeX Live。

TeX Live用户可用tlmgr安装所需集合（依安装方式选择，系统发行版的TeX请用其包管理器）：

```bash
tlmgr install collection-xetex collection-langchinese collection-latexextra \
  collection-fontsrecommended collection-bibtexextra collection-pictures collection-science
```

## 两种字体模式

默认`THESIS_FONTS=preview`：FandolSong/Hei/Kai/Fang、TeX Gyre Termes，由TeX安装提供，不从本仓库分发。中文族名映射写在每个模板的`fonts.tex`中，独立复制模板目录仍可用。

`THESIS_FONTS=school`：要求Times New Roman、SimSun、SimHei、FangSong、KaiTi。用户须有合法使用权并自行安装；缺字体验证失败时不静默换字体。此模式也不等于所有学校规定已核对。

字体替换会改变字宽、换行、分页和总页数。任何预览模式输出都不能当作学校字体验收证据。

## 运行

```bash
python3 tests/preflight.py
bash templates/海口经济学院/compile.sh
python3 tests/compile_all.py
python3 tests/boundaries.py
python3 tests/structure.py
```

中间产物与日志写在`.build`和`reports`，默认不入库。可用系统临时目录，或按系统约定设置`TMPDIR`；不依赖OpenCode目录。不提供宽泛递归删除的清理脚本。

## 故障

找不到命令先检查PATH；找不到bst先核对TeX发行版与宏包版本；找不到学校字体改用预览或合法安装所需字体。编译失败时旧PDF仍存在，请检查退出码和`.build/<入口>/<入口>.log`。

多个进程不要同时编译同一目录同一入口；当前脚本不提供并发锁。官方若要求Word提交，PDF成功也不代表允许替代Word。

# 海南高校论文 LaTeX 参考模板

**非官方、非学校认证项目。** 提供可编译的论文写作示例与官方来源索引；不保证符合任何学院当届提交要求。所有示例研究内容均非真实实验或调查结果，不可直接作为毕业论文提交。

## 范围与状态

| 模板目录 | 依据 / 适用边界 | 状态 |
|---|---|---|
| [海南热带海洋学院](templates/海南热带海洋学院/README.md) | 历史理工、文经管法、外语、艺术Word的格式信息；封面为本地重排 | 4个入口；不保证当届学院仍采用历史格式 |
| [海口经济学院](templates/海口经济学院/README.md) | 2026届附件13格式信息 | 仍需学院审核；官方要求Word电子文档，PDF不自动满足要求 |
| [海南医科大学](templates/海南医科大学/README.md) | **仅药学院2019本科规范** | 不代表全校本科或研究生；封面/声明为占位 |
| [琼台师范学院](templates/琼台师范学院/README.md) | 2021工作规定的组成结构 | 关键版式和声明待当届原件核对 |
| [三亚学院](templates/三亚学院/README.md) | 管理规定和2026届通知；学院确定并审核备案版式 | 完整结构工作稿，未取得学院备案Word |
| [海南科技职业大学](templates/海南科技职业大学/README.md) | 自2026届实施的第三次修订管理办法 | 仅结构依据；专门书写规范/模板未取得 |

海南大学及海南师范大学本版仅提供[来源链接](sources/README.md)，不捆绑上游代码、历史论文或原始压缩包。不代表这些学校没有模板，也不代表本项目覆盖海南全部高校或学位层次。

## 快速开始

依赖：Linux、Bash、Python 3.10+、TeX Live 2026及宏包、Poppler。详见[安装与构建](docs/BUILD.md)。不附带字体文件。

```bash
python3 tests/preflight.py
bash templates/海南热带海洋学院/compile.sh
bash templates/海南热带海洋学院/compile.sh main-humanities
bash templates/海南热带海洋学院/compile.sh main-foreign
bash templates/海南热带海洋学院/compile.sh main-art
bash templates/海南医科大学/compile.sh
```

其他学校同样在对应目录执行 `bash compile.sh`。中间文件在各自`.build/<入口>/`，最终PDF在模板目录；只有完整编译成功才替换最终PDF，失败保留旧PDF，务必查看退出码而不是仅看PDF存在。

**默认是开放字体预览模式，不是学校字体格式。** 使用TeX Live的Fandol及TeX Gyre Termes，PDF分页可能与学校字体模式不同。若已合法安装所需字体，可显式运行：

```bash
THESIS_FONTS=school bash templates/海口经济学院/compile.sh
```

不得分发微软字体文件或把开放字体预览称为官方合规输出。源码中个人信息均为示例占位，正式写作请自行替换。

## 验证

```bash
python3 tests/compile_all.py
python3 tests/boundaries.py
python3 tests/structure.py
python3 tests/release_audit.py
```

- 编译测试：6校9入口、最终日志、缺字、溢出、引用、字体嵌入和海医目录回归。
- 边界测试：独立副本、长字段、外部工作目录、路径空格、书目排序、失败保护、固定行距。
- 结构测试：跨节图表/公式重置、跨页脚注、海医多页目录。
- 发布检查：白名单、敏感路径/密钥形状、文献标准别名、外部文件和第三方声明。

本机与 GitHub Actions 实测结果、对应提交及限制见[验证说明](docs/VALIDATION.md)。已完成一次 Ubuntu 托管 runner 的安装到全部测试验证；这不代表其他平台或未来提交自动通过。格式校验和学校审核不是同一件事。

## 来源、许可与贡献

- [来源及资料缺口](sources/README.md)：以具体学院、层次、年份为单位，不外推。
- [第三方声明](THIRD_PARTY_NOTICES.md)：自有代码/文档采用MIT；海经书目样式衍生文件仍采用LPPL。
- [贡献约定](CONTRIBUTING.md)：请先脱敏，补齐官方依据，不上传未经确认的附件、国标全文或真实论文。
- [发布清单](docs/RELEASE.md)：源码范围、脱敏要求与首次发布检查；导出和测试脚本不会自动创建仓库或推送。
- 可用 `python3 tests/export_source.py ../hainan-thesis-reference-source.zip` 导出仅含源码/文档的干净包；不覆盖已有目标，详见发布清单。不要直接打包含本机产物的整个工作目录。

模板为工具，不代写研究；不提供真实性、学术质量或答辩资格保证。使用前请与所属学院确认是否接受LaTeX/PDF、签名和归档形式。

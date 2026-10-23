% !TEX program = xelatex
% 海南热带海洋学院本科毕业论文（设计）LaTeX 模板
% 依据教务处《毕业设计（论文）》理工/文经管法/外语/艺术四套 Word 模板整理
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{hntouthesis}[2026/10/23 Hainan Tropical Ocean University thesis]

\newif\ifhnt@foreign
\newif\ifhnt@art
\newif\ifhnt@human
\DeclareOption{foreign}{\hnt@foreigntrue}
\DeclareOption{art}{\hnt@arttrue}
\DeclareOption{humanities}{\hnt@humantrue}
\DeclareOption{science}{}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexart}}
\ProcessOptions\relax

\LoadClass[12pt,a4paper,fontset=none]{ctexart}

%====================== 页面 ======================
\RequirePackage{geometry}
\geometry{top=30mm,bottom=25mm,left=30mm,right=20mm,headheight=2pt,headsep=8mm}

%====================== 字体 ======================
\RequirePackage{fontspec}
\RequirePackage{xeCJK}
\input{fonts.tex}
\newcommand{\song}{\CJKfamily{zhsong}}
\newcommand{\hei}{\CJKfamily{zhhei}}
\newcommand{\kai}{\CJKfamily{zhkai}}
\newcommand{\fs}{\CJKfamily{zhfs}}

%====================== 宏包 ======================
\RequirePackage{amsmath,amssymb}
\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{caption}
\RequirePackage{titlesec}
\RequirePackage{tocloft}
\RequirePackage{fancyhdr}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{gbt7714}
\RequirePackage{indentfirst}
\RequirePackage{etoolbox,tabularx,longtable,listings,perpage}
\RequirePackage{tikz,pgfplots}
\usetikzlibrary{arrows.meta,positioning}
\pgfplotsset{compat=1.18}
\MakePerPage{footnote}
\renewcommand{\thefootnote}{\ifcase\value{footnote}\or①\or②\or③\or④\or⑤\or⑥\or⑦\or⑧\or⑨\or⑩\or⑪\or⑫\or⑬\or⑭\or⑮\or⑯\or⑰\or⑱\or⑲\or⑳\else\arabic{footnote}\fi}
\xeCJKDeclareCharClass{CJK}{"2460 -> "24FF,"3200 -> "32FF}
\lstset{basicstyle=\ttfamily\small,breaklines=true,columns=fullflexible,frame=single,numbers=left,numberstyle=\tiny,showstringspaces=false}

%====================== 论文信息 ======================
\newcommand{\hnttitle}{单片机在测温技术中的应用}
\newcommand{\hnttitleeng}{Application of DCU in Temperature Measurement Technology}
\newcommand{\hntauthor}{张\quad 三}
\newcommand{\hntstudentid}{2022000001}
\newcommand{\hntcollege}{海洋科学技术学院}
\newcommand{\hntmajor}{电子信息工程}
\newcommand{\hntclass}{2022 级 1 班}
\newcommand{\hntadvisor}{李\quad 四}
\newcommand{\hntadvisortitle}{副教授}
\newcommand{\hntadvisorB}{}
\newcommand{\hntadvisortitleB}{}
\newcommand{\hntdate}{二〇二六年六月}
\newcommand{\hntcohort}{26}
\newcommand{\hntauthoreng}{Zhang San}
\newcommand{\hntadvisoreng}{Li Si}
\newcommand{\hntdateeng}{June 2026}
% 旧 Word 各节页面设置不一致：正文按其实际节属性，艺术类按明文说明。
\newcommand{\hntbodylayout}{%
  \ifhnt@art
    \newgeometry{top=30mm,bottom=25mm,left=30mm,right=20mm,headheight=2pt,headsep=3mm}%
  \else
    \newgeometry{top=26mm,bottom=26mm,left=31.7mm,right=31.7mm,headheight=2pt,headsep=3mm}%
  \fi
  \linespread{1}\selectfont
  \let\hnt@normalsize\normalsize
  \renewcommand{\normalsize}{\hnt@normalsize\ifhnt@foreign\fontsize{12bp}{22bp}\else\fontsize{12bp}{20bp}\fi\selectfont}%
  \song\normalsize
}
\let\ifhntforeign\ifhnt@foreign
\let\ifhntart\ifhnt@art
\let\ifhnthuman\ifhnt@human

%====================== 标题 ======================
\setcounter{secnumdepth}{4}
\setcounter{tocdepth}{3}
\renewcommand{\thesection}{\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
\renewcommand{\thesubsubsection}{\thesubsection.\arabic{subsubsection}}
\renewcommand{\theparagraph}{\thesubsubsection.\arabic{paragraph}}
\ifhnt@human
  \renewcommand{\thesection}{\chinese{section}}
  \renewcommand{\thesubsection}{\ifcase\value{subsection}\or㈠\or㈡\or㈢\or㈣\or㈤\or㈥\or㈦\or㈧\or㈨\or㈩\else（\chinese{subsection}）\fi}
  \renewcommand{\thesubsubsection}{\arabic{subsubsection}}
  \renewcommand{\theparagraph}{\ifcase\value{paragraph}\or⑴\or⑵\or⑶\or⑷\or⑸\else（\arabic{paragraph}）\fi}
\fi

\titleformat{\section}{\centering\hei\zihao{3}}{\thesection}{0.6em}{}
\titleformat{\subsection}{\hei\zihao{-3}}{\thesubsection}{0.6em}{}
\titleformat{\subsubsection}{\hei\zihao{4}}{\thesubsubsection}{0.6em}{}
\titleformat{\paragraph}[block]{\hei\zihao{4}}{\theparagraph}{0.6em}{}
\ifhnt@foreign
  \titleformat{\section}{\centering\rmfamily\bfseries\zihao{3}}{\thesection}{0.6em}{}
  \titleformat{\subsection}{\rmfamily\bfseries\zihao{-3}}{\thesubsection}{0.6em}{}
  \titleformat{\subsubsection}{\rmfamily\bfseries\zihao{4}}{\thesubsubsection}{0.6em}{}
  \titleformat{\paragraph}[block]{\rmfamily\zihao{-4}}{\theparagraph}{0.6em}{}
\fi
\titlespacing*{\section}{0pt}{0.5\baselineskip}{0.5\baselineskip}
\titlespacing*{\subsection}{0pt}{0.5\baselineskip}{0.3\baselineskip}
\titlespacing*{\subsubsection}{0pt}{0.3\baselineskip}{0.2\baselineskip}
\titlespacing*{\paragraph}{0pt}{0.2\baselineskip}{0.2\baselineskip}

%====================== 目录 ======================
\renewcommand{\contentsname}{目\hspace{2em}录}
\renewcommand{\cfttoctitlefont}{\hfill\hei\zihao{3}}
\renewcommand{\cftaftertoctitle}{\hfill\mbox{}}
\renewcommand{\cftsecfont}{\hei\zihao{4}}
\renewcommand{\cftsecpagefont}{\hei\zihao{4}}
\renewcommand{\cftsubsecfont}{\song\zihao{-4}}
\renewcommand{\cftsubsecpagefont}{\song\zihao{-4}}
\renewcommand{\cftsubsubsecfont}{\song\zihao{-4}}
\renewcommand{\cftsubsubsecpagefont}{\song\zihao{-4}}
\renewcommand{\cftdotsep}{\cftnodots}
\setlength{\cftbeforesecskip}{0.3em}
\setlength{\cftbeforesubsecskip}{0pt}
\setlength{\cftbeforesubsubsecskip}{0pt}
\setlength{\cftsecindent}{0pt}
\setlength{\cftsubsecindent}{2em}
\setlength{\cftsubsubsecindent}{4em}

%====================== 页眉页脚 ======================
\fancypagestyle{hntfront}{%
  \fancyhf{}%
  \renewcommand{\headrulewidth}{0.5pt}%
}
\fancypagestyle{hntmain}{%
  \fancyhf{}%
  \fancyfoot[C]{\song\zihao{5}\thepage}%
  \renewcommand{\headrulewidth}{0.5pt}%
}
\tocloftpagestyle{hntfront}

%====================== 图表公式 ======================
\DeclareCaptionFont{wu}{\song\zihao{5}}
\captionsetup{font=wu,labelsep=space,justification=centering}
\captionsetup[table]{position=top}
\renewcommand{\thefigure}{\arabic{section}.\arabic{figure}}
\renewcommand{\thetable}{\arabic{section}.\arabic{table}}
\counterwithin{figure}{section}
\counterwithin{table}{section}
\counterwithin{equation}{section}
\renewcommand{\thefigure}{\arabic{section}.\arabic{figure}}
\renewcommand{\thetable}{\arabic{section}.\arabic{table}}
\renewcommand{\theequation}{\arabic{section}.\arabic{equation}}

%====================== 封面 ======================
\newcommand{\hntcoverfield}[1]{\parbox[c]{6.2cm}{\centering\song\zihao{-4}#1\par\kern2pt\hrule height0.4pt}}
\newcommand{\hntcoverfields}{%
  \renewcommand{\arraystretch}{1.9}%
  \begin{tabular}{r@{\hspace{0.4em}}l}
    {\hei\zihao{4} 学\quad\quad 院：} & \hntcoverfield{\hntcollege} \\[0.15cm]
    {\hei\zihao{4} 专\quad\quad 业：} & \hntcoverfield{\hntmajor} \\[0.15cm]
    {\hei\zihao{4} 学 生 姓 名：} & \hntcoverfield{\hntauthor} \\[0.15cm]
    {\hei\zihao{4} 班\quad\quad 级：} & \hntcoverfield{\hntclass} \\[0.15cm]
    {\hei\zihao{4} 学\quad\quad 号：} & \hntcoverfield{\hntstudentid} \\[0.15cm]
    {\hei\zihao{4} 指导教师姓名：} & \hntcoverfield{\hntadvisor\quad\hntadvisortitle} \\
    \ifdefempty{\hntadvisorB}{}{\hei\zihao{4} 第二指导教师： & \hntcoverfield{\hntadvisorB\quad\hntadvisortitleB}\\}
    {\hei\zihao{4} 日\quad\quad 期：} & \hntcoverfield{\hntdate} \\
  \end{tabular}%
}

\newcommand{\makehntcover}{%
  \begin{titlepage}
    \thispagestyle{empty}
    \begin{center}
      \vspace*{0.6cm}
      {\hei\zihao{1}\bfseries 海南热带海洋学院}\\[0.25cm]
      {\rmfamily\zihao{4} Hainan Tropical Ocean University}\\[1.6cm]
      {\hei\zihao{3} \hntcohort\hspace{0.3em}届本科毕业论文（设计）}\\[1.1cm]
      {\hei\zihao{3} \hnttitle}\\[2.0cm]
      \hntcoverfields
    \end{center}
    \vfill
    \begin{center}
      {\hei\zihao{-4} 海南热带海洋学院教务处}\\[0.2cm]
      {\hei\zihao{-4} 二〇二六年六月制}
    \end{center}
  \end{titlepage}%
}

\newcommand{\makehntinnercover}{%
  \begin{titlepage}
    \thispagestyle{empty}
    \begin{center}
      \vspace*{0.6cm}
      {\hei\zihao{3} \hntcohort\hspace{0.3em}届本科生毕业设计说明书\ifhnt@art\else（论文）\fi}\\[1.0cm]
      {\hei\zihao{3} \hnttitle}\\[1.6cm]
      \hntcoverfields
    \end{center}
    \vspace{0.8cm}
    \begin{center}
      {\hei\zihao{4} 最终评定成绩：\underline{\makebox[4cm]{}}}
    \end{center}
    \vfill
    \begin{center}
      {\hei\zihao{4} \hntdate}
    \end{center}
  \end{titlepage}%
}

\newcommand{\makehntengcover}{%
  \begin{titlepage}
    \thispagestyle{empty}
    \begin{center}
      \vspace*{1.2cm}
      {\rmfamily\zihao{2}\bfseries \hnttitleeng}\\[0.8cm]
      {\rmfamily\zihao{4} By \hntauthoreng}\\[1.2cm]
      {\rmfamily\zihao{4} A thesis}\\[0.2cm]
      {\rmfamily\zihao{4} Submitted to the School of Foreign Languages}\\[0.2cm]
      {\rmfamily\zihao{4} of Hainan Tropical Ocean University}\\[0.2cm]
      {\rmfamily\zihao{4} In partial fulfillment of the requirements}\\[0.2cm]
      {\rmfamily\zihao{4} For the degree of}\\[0.2cm]
      {\rmfamily\zihao{4} Bachelor of Arts}\\[1.2cm]
      {\rmfamily\zihao{4} Supervised by}\\[0.2cm]
      {\rmfamily\zihao{4} \hntadvisoreng}\\[1.2cm]
      {\rmfamily\zihao{4} \hntdateeng}
    \end{center}
  \end{titlepage}%
}

\endinput

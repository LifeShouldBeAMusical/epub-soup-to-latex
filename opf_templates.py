import re


unwrap_tags = ['html', 'body', 'metadata', 'opf:metadata', 'spine']
remove_tags = ['dc:description', 'description', 'dc:subject', 'subject', 'dc:rights', 'rights', 'meta', 'opf:meta', 'dc:identifier', 'identifier', 'dc:contributor', 'contributor', 'dc:publisher', 'publisher', 'dc:language', 'language', 'itemref', 'series_index', 'guide', 'reference']
title_tags = ['title', 'dc:title']
date_tags = ['date', 'dc:date']
creator_tags = ['creator', 'dc:creator']
source_tags = ['source', 'dc:source']
package_tags = ['package']
item_tags = ['item']
manifest_tags = ['manifest']


geometry = """% Geometry
\\usepackage{geometry}
"""
geometry_tradesize = """
\\geometry{paperheight=9in}
\\geometry{paperwidth=6in}
"""
geometry_lettersize = """
\\geometry{paperheight=11in}
\\geometry{paperwidth=8.5in}
"""
geometry_margins = """
\\geometry{rmargin=0.5in}
\\geometry{lmargin=0.5in}
\\geometry{tmargin=0.7in}
\\geometry{headsep=0.15in}
\\geometry{bmargin=0.5in}
\\geometry{bindingoffset=0.3in}

\\setlength{\\emergencystretch}{2em}

"""


titles = """
% Format Titles
\\usepackage{titlesec}
% \\renewcommand{\\thesection}{Part \\arabic{section}}
\\usepackage{changepage}
\\usepackage{etoolbox}
\\patchcmd{\\part}{\\thispagestyle{plain}}{\\thispagestyle{empty}}{}{\\errmessage{Cannot patch \\string\\part}}
\\patchcmd{\\chapter}{\\thispagestyle{plain}}{\\thispagestyle{empty}}{}{\\errmessage{Cannot patch \\string\\chapter}}
% \\patchcmd{\\chapter}{\\cleardoublepage}{\\clearpage}{}{\\errmessage{Cannot patch \\string\\chapter}}
% \\addto\\captionsenglish{
% 	\\renewcommand{\\chaptername}{Episode}
% }
% \\addto\\captionsenglish{
%	\\renewcommand{\\partname}{Arc}
% }


% Style Headings
\\usepackage{sectsty}
\\usepackage{fancyhdr}
\\renewcommand{\\headrulewidth}{0pt}
\\fancyhf{}
\\fancyhead[lo]{\\slshape\\nouppercase{\\rightmark}}
\\fancyhead[re]{\\slshape\\nouppercase{\\leftmark}}
\\fancyhead[ro,le]{\\thepage}

"""

blockquotes = """
% Block Quotes
\\usepackage{csquotes}

\\usepackage{hanging}
\\newenvironment{textmessage}
	{\\vspace*{0.2em}
	\\begin{hangparas}{1.2em}{1}}
	{\\end{hangparas}
	\\vspace*{0.2em}}

"""

images = """
% Images
\\usepackage{graphicx}

"""

underline = """
% Underline
\\usepackage[normalem]{ulem}

"""

drop_caps = """
% Drop Caps
\\usepackage{type1cm}
\\usepackage{lettrine}
\\setcounter{DefaultLines}{3}

"""

misc = """
% \\usepackage{setspace}

"""

font = """
% Font
\\usepackage[T3,T2A,T1]{fontenc}
\\usepackage[utf8]{inputenc}
\\usepackage[russian,english]{babel}
\\usepackage{CJKutf8}
% \\begin{CJK}{UTF8}{min} [kanji] \\end{CJK} % Chinese, Japanese
% \\begin{CJK}{UTF8}{mj} [hangul] \\end{CJK} % Korean
\\usepackage{staves}
\\newenvironment{courier}{\\ttfamily\\selectfont}{\par}
\\newenvironment{sansserif}{\\sffamily\\selectfont}{\par}

"""

symbols = """
% Symbols
%\\usepackage{gensymb}
%\\usepackage[gen]{eurosym}
%\\usepackage{tipa}
%\\usepackage{wasysym}
%\\usepackage{dingbat}

"""

toc = """
% TOC
\\usepackage{tocloft}
%\\renewcommand{\\cftchappresnum}{Chapter }
%\\setlength{\\cftchapnumwidth}{4.2em}
\\renewcommand{\\cftchapfont}{}
\\renewcommand{\\cftchappagefont}{}
\\renewcommand{\\cfttoctitlefont}{\\hfill\\Huge}
\\renewcommand{\\cftaftertoctitle}{\\hfill}
\\setlength{\\cftbeforechapskip}{0.2em}
\\renewcommand{\\cftchapdotsep}{\\cftdotsep}
"""

commands = """
% <hr/>
\\newcommand{\\centereddots}{
%\\vspace{-0.3em}
%\\vspace{0.0em}
%\\vspace{0.4em}
\\begin{center} * * * \\end{center}
%\\vspace{-0.7em}
%\\vspace{-0.4em}
%\\vspace{0.0em}
}

% Clear to Left Page
\\newcommand*\\cleartoleftpage{
  \\clearpage
  \\ifodd\\value{page}\\hbox{}\\newpage\\fi
}

% Unnumbered Chapter
\\newcommand*\\unnumberedchapter[1]{
	\\chapter*{#1}
	\\markboth{\MakeUppercase{#1}}{}
	\\addcontentsline{toc}{chapter}{#1}
}
% Custom Chapter
\\newcommand{\\customchapter}[1]{
	\\stepcounter{chapter}
	\\chapter*{\\chaptername\\ \\thechapter: \\\\ \\vspace{0.8em} #1}
	\\markboth{\\MakeUppercase{\\chaptername\\ \\thechapter: #1}}{}
	\\addcontentsline{toc}{chapter}{\\chaptername\\ \\thechapter: #1}
}


% Book
\\newcommand*{\\book}[2]{
	\\part*{
		Book #1: \\\\ \\vspace{1em} #2
		%\\addtocontents{toc}{\\protect\\vspace{10pt}}
		\\addcontentsline{toc}{part}{Book #1 -- #2}
		\\thispagestyle{empty}
	}
}

"""


fonts_hp = """
% HP Packages
\\usepackage{sectsty}
\\usepackage{Alegreya}

"""
commands_hp = """
% HP Commands
\\titleformat{\\chapter}[display]{\\huge\\centering\\fontfamily{antt}}{\\chaptertitlename\\ \\thechapter}{10pt}{\\huge}

\\partfont{\\fontfamily{antt}\\selectfont}
\\sectionfont{\\large\\normalfont\\fontfamily{antt}\\selectfont}

\\input{hp_hyphenation}

% Year
\\newcommand*{\\yearbook}[1]{
	\\part*{
		Year #1
		%\\addtocontents{toc}{\\protect\\vspace{10pt}}
		\\addcontentsline{toc}{part}{Year #1}
		\\thispagestyle{empty}
	}
}

"""

fonts_dp = """
% DP Packages
\\usepackage{kerkis}
%\\usepackage[T1]{fontenc}

"""

fonts_heathers = """
% Heathers Packages
\\usepackage[nf]{coelacanth}
%\\usepackage[T1]{fontenc}

"""

fonts_kp = """
% KP Packages
\\usepackage{kpfonts}
%\\usepackage[T1]{fontenc}

"""

fonts_we = """
% Wynonna Earp Packages
\\usepackage[bitstream-charter]{mathdesign}

"""

fonts_oz = """
% Oz Packages
\\linespread{1.025}
%\\usepackage[T1]{fontenc}
\\usepackage{newpxtext}

"""

fonts_hundred = """
% The 100 Packages
\\usepackage{cochineal}
%\\usepackage[T1]{fontenc}

"""

fonts_twilight = """
% Twilight Packages
\\usepackage[cmintegrals,cmbraces]{newtxmath}
\\usepackage{ebgaramond-maths}
%\\usepackage[T1]{fontenc}
"""

fonts_sw = """
% SW Commands
\\usepackage{PTSerifCaption}

"""


doc_dec_12 = """
\\\\documentclass[12pt]{book}

"""
doc_dec_11 = """
\\documentclass[11pt]{book}

"""
doc_dec_10 = """
\\documentclass[10pt]{book}

"""


begin_multi = """
\\begin{document}


\\frontmatter
\\pagenumbering{gobble}


\\maketitle


\\cleardoublepage


\\tableofcontents

\\clearpage

\\markboth{}{}


\\cleartoleftpage


\\mainmatter
\\pagenumbering{arabic}
%\\pagestyle{fancy}

"""
begin_single = """
\\begin{document}

\\frontmatter
\\pagenumbering{gobble}

\\maketitle

\\mainmatter
\\pagenumbering{arabic}
%\\pagestyle{fancy}

"""


title_underscore = re.compile(r"\\(title|author){([^\\]*)_(.*?)}")


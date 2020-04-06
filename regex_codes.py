import re

#FILE REGEX
html_regex = re.compile(r"\.x?html?")
style_regex = re.compile(r"\.css")
toc_regex = re.compile(r"\.ncx")
xml_regex = re.compile(r"\.xml")
opf_regex = re.compile(r"\.opf")
tex_regex = re.compile(r"\.tex")

cover_regex = re.compile(r".*cover\.(x?html?)")
title_regex = re.compile(r".*title[ \-_]*page\.(x?html?)")
chapter_regex = re.compile(r".*\d+\.x?html?")
stylesheet_regex = re.compile(r"OEBPS/stylesheet\.css")

b_fandom = re.compile(r"<b>[ \t\r\n]*Fandoms?:[ \t\r\n]*</b>[ \t\r\n]+([^<>]+)<br[^>]*>")
strong_fandom = re.compile(r"<strong>[ \t\r\n]*Fandoms?:[ \t\r\n]*</strong>[ \t\r\n]+([^<>]+)<br[^>]*>")
b_categories = re.compile(r"<b>[ \t\r\n]*Category:[ \t\r\n]*</b>[ \t\r\n]+([^<>]+)<br[^>]*>")
strong_categories = re.compile(r"<strong>[ \t\r\n]*Category:[ \t\r\n]*</strong>[ \t\r\n]+([^<>]+)<br[^>]*>")

#
bold_regex = re.compile(r"<(strong|b)>(.+?)</\1>", re.DOTALL) #\textbf{\2}
emph_regex = re.compile(r"<(em|i)>(.+?)</\1>", re.DOTALL)	#\emph{\2}




#css formatting

text_indent = re.compile(r"text-indent:[ ]*(\-?\d[0-9.]*)([a-z%]*)")

spacing_single = re.compile(r"(margin|padding)-(top|bottom|left|right):[ ]*(\-?\d+[0-9.]*)([a-z%]*)")
spacing_four = re.compile(r"(margin|padding):[ ]*(\-?\d+[0-9.]*[a-z%]*|auto)[ ]+(\-?\d+[0-9.]*[a-z%]*|auto)[ ]+(\-?\d+[0-9.]*[a-z%]*|auto)[ ]+(\-?\d+[0-9.]*[a-z%]*|auto)")
spacing_three = re.compile(r"(margin|padding):[ ]*(\-?\d+[0-9.]*[a-z%]*|auto)[ ]+(\-?\d+[0-9.]*[a-z%]*|auto)[ ]+(\-?\d+[0-9.]*[a-z%]*|auto)")
spacing_two = re.compile(r"(margin|padding):[ ]*(\-?\d+[0-9.]*[a-z%]*|auto)[ ]+(\-?\d+[0-9.]*[a-z%]*|auto)")
spacing_one = re.compile(r"(margin|padding):[ ]*(\-?\d+[0-9.]*[a-z%]*|auto)")

font_size = re.compile(r"font-size:[ ]*(\-?\d+[0-9.]*)([a-z%]*)")
font_size_other = re.compile(r"font-size:[ ]*(smaller|larger|xx-small|x-small|small|medium|large|x-large|xx-large|initial)")

bold_css_regex = re.compile(r"font-weight:[ ]*bold")
italic_css_regex = re.compile(r"font-style:[ ]*italic")
strike_css_regex = re.compile(r"text-decoration:[ ]*line-through")
underline_css_regex = re.compile(r"text-decoration:[ ]*underline")
small_caps_css_regex = re.compile(r"font-variant:[ ]*small-caps")

font_family_regex = re.compile(r"font-family:[ ]*.*(monospace|sans-serif|serif)")

display_regex = re.compile(r"display:[ ]*(inline-block|block|inline|none)")

align_regex = re.compile(r"text-align:[ ]*(center|left|right|justify)")
page_break = re.compile(r"page-break-(after|before):[ ]*(always|left|right|avoid)")

line_height = re.compile(r"line-height:[ ]*(\d[.0-9]*)")

no_hyphen = re.compile(r"adobe-hyphenate:[ ]*none")

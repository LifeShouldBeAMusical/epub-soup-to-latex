#Python modules
import re
import os
import logging
from bs4 import BeautifulSoup, Comment
from titlecase import titlecase
#files for this program
import regex_codes


def filter_chars01(read, logger):
	nbsp = re.compile(r" ")
	read = re.sub(nbsp, r" ", read)
	
	backslash = re.compile(r"\\")
	# count += len(re.findall(backslash, read))
	read = re.sub(backslash, r"\\backslash", read)
	
	read = re.sub(r"(\_)", r"\\\1", read)
	read = re.sub(r"([MSD][xrstz]{1,2}\.)([ ]+)", r"\1\\\2", read)
	
	return read

def filter_chars02(read, logger):
	read = filter_punctuation(read, logger)
	read = filter_language(read, logger)
	read = filter_symbols(read, logger)
	read = filter_greek(read, logger)
	read = filter_letters(read, logger)
	read = filter_whitespace(read, logger)
	return read


def filter_punctuation(read, logger):
	read = read.replace("&gt; ", "\\textgreater\ ")
	read = read.replace("&gt;", "\\textgreater ")
	read = read.replace("&lt; ", "\\textless\ ")
	read = read.replace("&lt;", "\\textless ")
	
	read = re.sub(r"(&)amp;", r"\1", read, flags=re.IGNORECASE)
	read = re.sub(r"(&)", r"\\\1", read)
	
	read = re.sub(r"“", r"``", read)
	read = re.sub(r"‘", r"`", read)
	read = re.sub(r'["”]', r"''", read)
	read = re.sub(r"[’̕´]", r"'", read)
	
	while(re.search(r"([ \t\r\n`])\"", read)):
		read = re.sub(r"([ \t\r\n`])\"", r"\1``", read)
	while(re.search(r"([ \t\r\n`])'", read)):
		read = re.sub(r"([ \t\r\n`])'", r"\1`", read)
	while(re.search(r"`([' \t\r]*\n{2})", read)):
		read = re.sub(r"`([' \t\r]*\n{2})", r"'\1", read)
	
	read = re.sub(r"[—―ー]", r"---", read)
	read = re.sub(r"[–─]", r"--", read)
	read = re.sub(r"̵", r"-", read)
	read = re.sub(r"(…|\.[ ]*\.[ ]*\.) ", r"\\dots\\ ", read)
	read = re.sub(r"(…|\.[ ]*\.[ ]*\.)", r"\\dots ", read)
	read = re.sub(r"(\$)", r"\\\1", read)
	read = re.sub(r"(\#)", r"\\\1", read)
	read = re.sub(r"(\%)", r"\\\1", read)
	read = re.sub(r"̸", r"/", read)
	read = re.sub(r"ː", r":", read)
	
	read = re.sub(r"(\\backslash)", r"$\1$", read)
	
	read = re.sub(r"¼", r'\\textsuperscript{1}/\\textsubscript{4}', read)
	read = re.sub(r"½", r'\\textsuperscript{1}/\\textsubscript{2}', read)
	read = re.sub(r"⅔", r"\\textsuperscript{2}/\\textsubscript{3}", read)
	read = re.sub(r"¾", r"\\textsuperscript{3}/\\textsubscript{4}", read)
	read = re.sub(r"™ ", r"\\texttrademark\ ", read)
	read = re.sub(r"™", r"\\texttrademark ", read)
	read = re.sub(r"° ", r"\\degree\ ", read)
	read = re.sub(r"°", r"\\degree ", read)
	read = re.sub(r"\^ ", r"\\textasciicircum\ ", read)
	read = re.sub(r"\^", r"\\textasciicircum ", read)
	read = re.sub(r"\~ ", r"\\textasciitilde\ ", read)
	read = re.sub(r"\~", r"\\textasciitilde ", read)
	read = re.sub(r"¬", r"$\\neg$", read)
	
	read = re.sub(r"$$", r"", read)
	read = re.sub(r"(\\\\)[ \t\r\n]*(\[.*?\])", r"\1\n{\2}", read)
	return read


def filter_whitespace(read, logger):
	read = re.sub(r"\\[ ]+\\\\", r" \\\\", read)
	read = re.sub(r"([.?!]['}]*)([ ]+[a-z\-])", r"\1\\\2", read)
	return read


def filter_language(read, logger):
	read = re.sub(r"([а-яј]+)", r"\\foreignlanguage{russian}{\1}", read, flags=re.IGNORECASE)
	while(re.search(r"\\foreignlanguage\{russian\}\{([а-я ]+)\}([ ]*)\\foreignlanguage\{russian\}\{([а-я ]+)\}", read, flags=re.IGNORECASE)):
		read = re.sub(r"\\foreignlanguage\{russian\}\{([а-я ]+)\}([ ]*)\\foreignlanguage\{russian\}\{([а-я ]+)\}", r"\\foreignlanguage{russian}{\1\2\3}", read, flags=re.IGNORECASE)
	# read = re.sub(u"([\x3400-\x4DB5\x4E00-\x9FCB\xF900-\xFA6A]+)", u"\begin{CJK}{UTF8}{min}\1\end{CJK}", read)
	return read


def filter_symbols(read, logger):
	read = re.sub(r"☺", r"$\\smiley$", read)
	read = re.sub(r"☼", r"$\\sun$", read)
	read = re.sub(r"●", r"$\\CIRCLE$", read)
	read = re.sub(r"○", r"$\\bigcirc$", read)
	read = re.sub(r"Ω", r"$\\Omega$", read)
	read = re.sub(r"❤", r'$\\heartsuit$', read)
	read = re.sub(r"♥", r'$\\heartsuit$', read)
	read = re.sub(r"♡", r'$\\heartsuit$', read)
	read = re.sub(r"∞", r'$\\infty$', read)
	read = re.sub(r"♫ ", r'\\twonotes\\ ', read)
	read = re.sub(r"♫", r'\\twonotes ', read)
	read = re.sub(r"✔ ", r'\\checkmark\ ', read)
	read = re.sub(r"✔ ", r'\\checkmark\ ', read)
	return read


def filter_greek(read, logger):
	read = re.sub(r"∑", r'$\\sum$', read)
	read = re.sub(r"Δ", r'$\\Delta$', read)
	read = re.sub(r"Ψ", r'$\\Psi$', read)
	return read


def filter_letters(read, logger):
	read = filter_a(read, logger)
	read = filter_b(read, logger)
	read = filter_c(read, logger)
	read = filter_d(read, logger)
	read = filter_e(read, logger)
	read = filter_f(read, logger)
	read = filter_g(read, logger)
	read = filter_h(read, logger)
	read = filter_i(read, logger)
	read = filter_j(read, logger)
	read = filter_k(read, logger)
	read = filter_l(read, logger)
	read = filter_m(read, logger)
	read = filter_n(read, logger)
	read = filter_o(read, logger)
	read = filter_p(read, logger)
	read = filter_q(read, logger)
	read = filter_r(read, logger)
	read = filter_s(read, logger)
	read = filter_t(read, logger)
	read = filter_u(read, logger)
	read = filter_v(read, logger)
	read = filter_w(read, logger)
	read = filter_x(read, logger)
	read = filter_y(read, logger)
	read = filter_z(read, logger)
	return read


def filter_a(read, logger):
	read = re.sub(r"ᚨ", r"\\runictext{a}", read)
	
	read = re.sub(r"æ ", r"\\ae\ ", read)
	read = re.sub(r"æ", r"\\ae ", read)
	read = re.sub(r"À", r"\\`{A}", read)
	read = re.sub(r"à", r"\\`{a}", read)
	read = re.sub(r"Á", r"\\'{A}", read)
	read = re.sub(r"á", r"\\'{a}", read)
	read = re.sub(r"Â", r"\\^{A}", read)
	read = re.sub(r"â", r"\\^{a}", read)
	read = re.sub(r"Ã", r"\\~{A}", read)
	read = re.sub(r"ã", r"\\~{a}", read)
	read = re.sub(r"Å", r"\\r{A}", read)
	read = re.sub(r"å", r"\\r{a}", read)
	read = re.sub(r"ą", r"\\k{a}", read)
	read = re.sub(r"ä", r'\\"{a}', read)
	read = re.sub(r"Ǎ", r'\\v{A}', read)
	read = re.sub(r"ǎ", r'\\v{a}', read)
	read = re.sub(r"Ā", r'\\={A}', read)
	read = re.sub(r"ā", r'\\={a}', read)
	return read

def filter_b(read, logger):
	read = re.sub(r"ᛒ", r"\\runictext{b}", read)
	return read

def filter_c(read, logger):
	read = re.sub(r"ᛇ", r"\\runictext{c}", read)
	
	read = re.sub(r"Ç", r"\\c{C}", read)
	read = re.sub(r"ç", r"\\c{c}", read)
	read = re.sub(r"Č", r'\\v{c}', read)
	read = re.sub(r"č", r'\\v{c}', read)
	return read

def filter_d(read, logger):
	read = re.sub(r"ᛞ", r"\\runictext{d}", read)
	
	read = re.sub(r"Ď", r'\\v{D}', read)
	read = re.sub(r"ď", r'\\v{d}', read)
	return read

def filter_e(read, logger):
	read = re.sub(r"ᛖ", r"\\runictext{e}", read)
	
	read = re.sub(r"€", r"\\euro{}", read)
	read = re.sub(r"È", r"\\`{E}", read)
	read = re.sub(r"è", r"\\`{e}", read)
	read = re.sub(r"É", r"\\'{E}", read)
	read = re.sub(r"é", r"\\'{e}", read)
	read = re.sub(r"ế", r"\\'{\\^{e}}", read)
	read = re.sub(r"Ê", r"\\^{E}", read)
	read = re.sub(r"ê", r"\\^{e}", read)
	read = re.sub(r"ȇ", r"\\^{e}", read)
	read = re.sub(r"Ě", r'\\v{E}', read)
	read = re.sub(r"ě", r'\\v{e}', read)
	read = re.sub(r"ē", r'\\={e}', read)
	return read

def filter_f(read, logger):
	read = re.sub(r"ᚠ", r"\\runictext{f}", read)
	return read

def filter_g(read, logger):
	read = re.sub(r"ᚷ", r"\\runictext{g}", read)
	read = re.sub(r"ᚸ", r"\\runictext{g}", read)
	
	read = re.sub(r"Ǧ", r'\\v{G}', read)
	read = re.sub(r"ǧ", r'\\v{g}', read)
	return read

def filter_h(read, logger):
	read = re.sub(r"ᚺ", r"\\runictext{h}", read)
	read = re.sub(r"ᚻ", r"\\runictext{h}", read)
	
	read = re.sub(r"Ȟ", r'\\v{H}', read)
	read = re.sub(r"ȟ", r'\\v{h}', read)
	return read

def filter_i(read, logger):
	read = re.sub(r"ᛁ", r"\\runictext{i}", read)
	
	read = re.sub(r"Ì", r"\\`{I}", read)
	read = re.sub(r"ì", r"\\`{\\i}", read)
	read = re.sub(r"Í", r"\\'{I}", read)
	read = re.sub(r"í", r"\\'{\\i}", read)
	read = re.sub(r"Î", r"\\^{I}", read)
	read = re.sub(r"î", r"\\^{\\i}", read)
	read = re.sub(r"ï", r'\\"{\\i}', read)
	read = re.sub(r"Ǐ", r'\\v{I}', read)
	read = re.sub(r"ǐ", r'\\v{i}', read)
	read = re.sub(r"ī", r'\\={\\i}', read)
	return read

def filter_j(read, logger):
	read = re.sub(r"ᚦ", r"\\runictext{j}", read)
	
	read = re.sub(r"ǰ", r'\\v{j}', read)
	return read

def filter_k(read, logger):
	read = re.sub(r"ᚲ", r"\\runictext{k}", read)
	read = re.sub(r"ᚳ", r"\\runictext{k}", read)
	read = re.sub(r"ᚴ", r"\\runictext{k}", read)
	
	read = re.sub(r"Ǩ", r'\\v{K}', read)
	read = re.sub(r"ǩ", r'\\v{k}', read)
	return read

def filter_l(read, logger):
	read = re.sub(r"ᛚ", r"\\runictext{l}", read)
	
	read = re.sub(r"ł", r"\\l{}", read)
	read = re.sub(r"Ľ", r'\\v{L}', read)
	read = re.sub(r"ľ", r'\\v{l}', read)
	read = re.sub(r"ḷ", r'\\d{l}', read)
	read = re.sub(r"ḻ", r'\\underbar{l}', read)
	return read

def filter_m(read, logger):
	read = re.sub(r"ᛗ", r"\\runictext{m}", read)
	
	read = re.sub(r"μ", r"$\\mu$", read)
	
	read = re.sub(r"ṃ", r"\\d{m}", read)
	read = re.sub(r"ˈm", r"\\d{m}", read)
	return read

def filter_n(read, logger):
	read = re.sub(r"ᚾ", r"\\runictext{n}", read)
	read = re.sub(r"ᚿ", r"\\runictext{n}", read)
	
	read = re.sub(r"Ñ", r"\\~{N}", read)
	read = re.sub(r"ñ", r"\\~{n}", read)
	read = re.sub(r"Ň", r'\\v{N}', read)
	read = re.sub(r"ň", r'\\v{n}', read)
	read = re.sub(r"ṉ", r'\\underbar{n}', read)
	read = re.sub(r"ṇ", r'\\d{n}', read)
	read = re.sub(r"ṅ", r'\\.{n}', read)
	return read

def filter_o(read, logger):
	read = re.sub(r"ᛟ", r"\\runictext{o}", read)
	
	read = re.sub(r"Ò", r"\\`{O}", read)
	read = re.sub(r"ò", r"\\`{o}", read)
	read = re.sub(r"Ó", r"\\'{O}", read)
	read = re.sub(r"ó", r"\\'{o}", read)
	read = re.sub(r"Ô", r"\\^{O}", read)
	read = re.sub(r"ô", r"\\^{o}", read)
	read = re.sub(r"Ǒ", r'\\v{O}', read)
	read = re.sub(r"ǒ", r'\\v{o}', read)
	read = re.sub(r"Õ", r"\\~{O}", read)
	read = re.sub(r"õ", r"\\~{o}", read)
	read = re.sub(r"ö", r'\\"{o}', read)
	read = re.sub(r"ō", r"\\={o}", read)
	read = re.sub(r"ŏ", r"\\u{o}", read)
	read = re.sub(r"ő", r"\\H{o}", read)
	read = re.sub(r"Ở", r"\\H{O}\\texthooktop{}", read)
	read = re.sub(r"ở", r"\\H{o}\\texthooktop{}", read)
	read = re.sub(r"ȯ", r"\\.{o}", read)
	read = re.sub(r"Ø ", r"\\O\ ", read)
	read = re.sub(r"ø ", r"\\o\ ", read)
	read = re.sub(r"Ø", r"\\O ", read)
	read = re.sub(r"ø", r"\\o ", read)
	
	read = re.sub(r"œ", r"{\\oe}", read)
	return read

def filter_p(read, logger):
	read = re.sub(r"ᛈ", r"\\runictext{p}", read)
	return read

def filter_q(read, logger):
	read = re.sub(r"ᛜ", r"\\runictext{p}", read)
	read = re.sub(r"ᛝ", r"\\runictext{p}", read)
	return read

def filter_r(read, logger):
	read = re.sub(r"ᚱ", r"\\runictext{r}", read)
	
	read = re.sub(r"Ř", r'\\v{R}', read)
	read = re.sub(r"ř", r'\\v{r}', read)
	read = re.sub(r"ṟ", r'\\underbar{r}', read)
	return read

def filter_s(read, logger):
	read = re.sub(r"ᛊ", r"\\runictext{s}", read)
	read = re.sub(r"ᛋ", r"\\runictext{s}", read)
	
	read = re.sub(r"Š", r"\\v{S}", read)
	read = re.sub(r"š", r"\\v{s}", read)
	read = re.sub(r"Ṧ", r"\\v{\\.{S}}", read)
	read = re.sub(r"ṧ", r"\\v{\\.{s}}", read)
	read = re.sub(r"ṣ", r"\\d{s}", read)
	return read

def filter_t(read, logger):
	read = re.sub(r"ᛏ", r"\\runictext{t}", read)
	read = re.sub(r"ᛐ", r"\\runictext{t}", read)
	
	read = re.sub(r"Ť", r"\\v{T}", read)
	read = re.sub(r"ť", r"\\v{t}", read)
	read = re.sub(r"ṭ", r"\\d{t}", read)
	return read

def filter_u(read, logger):
	read = re.sub(r"ᚢ", r"\\runictext{u}", read)
	read = re.sub(r"ᚣ", r"\\runictext{u}", read)
	
	read = re.sub(r"Ü", r'\\"{U}', read)
	read = re.sub(r"Ù", r"\\`{U}", read)
	read = re.sub(r"ù", r"\\`{u}", read)
	read = re.sub(r"Ú", r"\\'{U}", read)
	read = re.sub(r"ú", r"\\'{u}", read)
	read = re.sub(r"Û", r"\\^{U}", read)
	read = re.sub(r"û", r"\\^{u}", read)
	read = re.sub(r"ụ", r"\\d{u}", read)
	read = re.sub(r"Ǔ", r"\\v{U}", read)
	read = re.sub(r"ǔ", r"\\v{u}", read)
	read = re.sub(r"Ǚ", r'\\v{\\"{U}}', read)
	read = re.sub(r"ǚ", r'\\v{\\"{u}}', read)
	return read

def filter_v(read, logger):
	return read

def filter_w(read, logger):
	return read

def filter_x(read, logger):
	read = re.sub(r"×", r"$\\times$", read)
	return read

def filter_y(read, logger):
	read = re.sub(r"Ý", r"\\'{Y}", read)
	read = re.sub(r"ý", r"\\'{y}", read)
	read = re.sub(r"ẏ", r"\\.{y}", read)
	return read

def filter_z(read, logger):
	read = re.sub(r"Ž", r'\\v{Z}', read)
	read = re.sub(r"ž", r'\\v{z}', read)
	return read


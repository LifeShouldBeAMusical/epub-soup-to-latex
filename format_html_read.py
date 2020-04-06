#Python modules
import re
import os
import logging
from bs4 import BeautifulSoup, Comment
from titlecase import titlecase
#files for this program
import regex_codes_html
from format_strings import filter_chars01, filter_chars02


def format_html_read(read, multichapter, logger):
	read = filter_xml_tag(read, logger)
	
	read = bhr_tags(read, logger)
	
	read = strong_tags(read, logger)
	
	read = heading_tags(read, multichapter, logger)
	
	read = handle_images(read, logger)
	
	read = bhr_tags(read, logger)
	
	read = lettrine(read, logger)
	
	read = filter_chars02(read, logger)
	
	read = whitespace(read, logger)
	
	read = hyphen_quote(read, logger)
	
	if(re.search(regex_codes_html.any_tag, read)):
		logger.warning("\t\tTag encountered: %d" % len(re.findall(regex_codes_html.any_tag, read)))
	return read


def filter_xml_tag(read, logger):
	if(re.search(regex_codes_html.xml_tag, read)):
		read = re.sub(regex_codes_html.xml_tag, r"\n", read)
		logger.info("\t\t\t" + "Removed XML tag")
	if(re.search(regex_codes_html.doctype_tag, read)):
		read = re.sub(regex_codes_html.doctype_tag, r"", read)
		logger.info("\t\t\t" + "Removed DOCTYPE tag")
	return read

def bhr_tags(read, logger):
	count = 0
	
	while re.search(regex_codes_html.chapter_br, read):
		read = re.sub(regex_codes_html.chapter_br, r"\\\1{\2}", read)
	
	read = re.sub(regex_codes_html.chapter_br_br, r"\\\1{\2 \\\\ \3}", read)
	
	read = re.sub(r"\\chapter\{(.+)[ .;\|-]*Part ([2-9]+|1\d+|Two|Three|Four|Five|Six|Seven|Eight|Nine)[ .;\|-]*(.*)\}", r"\\section{\3}", read, flags=re.IGNORECASE)
	read = re.sub(r"\\chapter\{(.+)[ .;\|-]*Part ([xiv0-9]+|One)[ .;\|-]*(.*)\}", r"\\chapter{\1}\n\n\\section{\3}", read, flags=re.IGNORECASE)
	
	read = re.sub(regex_codes_html.p_br, r"\n\n", read)
	read = re.sub(regex_codes_html.br_p, r"\n\n", read)
	
	while(re.search(regex_codes_html.br_br, read) or re.search(regex_codes_html.br_hr, read) or re.search(regex_codes_html.hr_br, read) or re.search(regex_codes_html.hr_hr, read)):
		read = re.sub(regex_codes_html.br_br, r"\n\n", read)
		read = re.sub(regex_codes_html.br_hr, r"\n\n\\centereddots\n\n", read)
		read = re.sub(regex_codes_html.hr_br, r"\n\n\\centereddots\n\n", read)
		read = re.sub(regex_codes_html.hr_hr, r"\n\n\\centereddots\n\n", read)
	
	while(re.search(regex_codes_html.div_hr_div, read)):
		read = re.sub(regex_codes_html.div_hr_div, r"\2", read)
	
	while(re.search(regex_codes_html.div_br_div, read)):
		read = re.sub(regex_codes_html.div_br_div, r"\2", read)
	
	while(re.search(regex_codes_html.br_tag, read) or re.search(regex_codes_html.tag_br, read) or re.search(regex_codes_html.hr_tag, read) or re.search(regex_codes_html.tag_hr, read)):
		read = re.sub(regex_codes_html.br_tag, r"\2\1", read)
		read = re.sub(regex_codes_html.tag_br, r"\2\1", read)
		read = re.sub(regex_codes_html.hr_tag, r"\2\1", read)
		read = re.sub(regex_codes_html.tag_hr, r"\2\1", read)
	
	while(re.search(regex_codes_html.br_env, read) or re.search(regex_codes_html.env_br, read) or re.search(regex_codes_html.hr_env, read) or re.search(regex_codes_html.env_hr, read)):
		read = re.sub(regex_codes_html.br_env, r"\2\n\1", read)
		read = re.sub(regex_codes_html.env_br, r"\2\n\1", read)
		read = re.sub(regex_codes_html.hr_env, r"\2\n\1", read)
		read = re.sub(regex_codes_html.env_hr, r"\2\n\1", read)
	
	while(re.search(regex_codes_html.br_br, read) or re.search(regex_codes_html.br_hr, read) or re.search(regex_codes_html.hr_br, read) or re.search(regex_codes_html.hr_hr, read)):
		read = re.sub(regex_codes_html.br_br, r"\n\n", read)
		read = re.sub(regex_codes_html.br_hr, r"\n\n\\centereddots\n\n", read)
		read = re.sub(regex_codes_html.hr_br, r"\n\n\\centereddots\n\n", read)
		read = re.sub(regex_codes_html.hr_hr, r"\n\n\\centereddots\n\n", read)
	
	return read

def strong_tags(read, logger):
	read = re.sub(regex_codes_html.itshape_break_itshape, r"\1", read)
	read = re.sub(regex_codes_html.pipes_itshape_pips, r"", read)
	
	while(re.search(regex_codes_html.bold_break, read)):
		read = re.sub(regex_codes_html.bold_break, r"\\textbf{\1}\2\\textbf{", read)
	while(re.search(regex_codes_html.it_break, read)):
		read = re.sub(regex_codes_html.it_break, r"\\textit{\1}\2\\textit{", read)
	
	read = re.sub(r"\\textit\{([^{}]*[ `]+)\}([^{}]+)\\textit\{([! }]+)", r"\\textit{\1\\textup{\2}\3", read)
	while re.search(r"(\\textup\{[^{}]*\}[^{}]+[ `]+)\}([^{}]*)\\textit\{([! }]+)", read):
		read = re.sub(r"(\\textup\{[^{}]*\}[^{}]+[ `]+)\}([^{}]*)\\textit\{([! }]+)", r"\1\\textup{\2}\3", read)
	read = re.sub(regex_codes_html.empty_it, r"\1", read)
	read = re.sub(regex_codes_html.empty_bf, r"\1", read)
	return read

def heading_tags(read, multichapter, logger):
	count = 0
	
	while(re.search(regex_codes_html.chapter_bold, read)):
		read = re.sub(regex_codes_html.chapter_bold, r"\\\1{\2\3\4}", read)
	
	read = re.sub(regex_codes_html.part_part, r"\\part{", read)
	
	if(multichapter):
		read = re.sub(regex_codes_html.part_chapter, r"\\chapter{\1}", read)
		read = re.sub(regex_codes_html.section_chapter, r"\\chapter{\1}", read)
	
	read = re.sub(regex_codes_html.chapter_number, r"\\\1{\2}", read)
	
	for match in re.finditer(r"\\(part|chapter\*?){([^{}\|]+?)}\n", read):
		if(re.search(r"[a-z]", match.group(2))):
			try:
				read = re.sub(r"\\(part|chapter\*?){%s}" % match.group(2), r"\\\1{%s}" % titlecase(match.group(2)), read)
			except:
				logger.debug("\t\t\t" + "Could not titlecase title: %s" % match.group(2))
	
	read = re.sub(r"\\chapter{Chapter \d+[ ~\-:.]*[ ]+", r"\\chapter{", read, flags=re.IGNORECASE)
	read = re.sub(r"\\chapter{Chapter \d+(th|rd|nd|st|[a-z])[ ~\-:]*[ ]+", r"\\chapter{", read, flags=re.IGNORECASE)
	read = re.sub(r"\\chapter{Chapter \d+[ ]*\\textsuperscript{(th|rd|nd|st)}[ ~\-:]*[ ]+", r"\\chapter{", read, flags=re.IGNORECASE)
	
	read = re.sub(r"\\chapter{[ ~\-:.]+[ ]+", r"\\chapter{", read)
	
	read = re.sub(r"\\(part|chapter\*?|section\*){[ \t\r\n\-]+(.*?)}\n", r"\\\1{\2}\n", read)
	read = re.sub(r"\\(part|chapter\*?|section\*){(.*?)[ \t\r\n\-]+}\n", r"\\\1{\2}\n", read)
	
	read = re.sub(r"\\chapter{((Prologue|Epilogue|Interlude|Outtake|Bonus|Intermission).*)}", r"\\unnumberedchapter{\1}", read, flags=re.IGNORECASE)
	# read = re.sub(r"\\chapter{(.*Interlude.*)}\n", r"\\unnumberedchapter{\1}", read, flags=re.IGNORECASE)
	read = re.sub(r"\\(part|chapter\*?|section\*){\d{1,3}}", r"\\\1{}", read)
	
	read = re.sub(r"\\chapter{Chapter \d+}", r"\\chapter{}", read, flags=re.IGNORECASE)
	read = re.sub(r"\\(part|chapter\*?|section\*){}[ \t\r\n]*\\(\1)", r"\\\1", read)
	read = re.sub(r"\\(part|chapter\*?|section\*){(.+)}[ \t\r\n]*\\(\1){}", r"\\\1{\2}", read)
	
	while(re.search(regex_codes_html.chapter_noindent, read)):
		read = re.sub(regex_codes_html.chapter_noindent, r"\\\1{\2}\n\n", read)
	
	read = re.sub(r"\\(chapter\*?){}", r"\\\1{}\n\n\\vspace*{-20pt}", read)
	
	return read

def whitespace(read, logger):
	count = 0
	
	read = re.sub(regex_codes_html.chapter_whitespace_one, r"\\\1{\2}\n", read)
	read = re.sub(regex_codes_html.chapter_whitespace_two, r"\\\1{\2}\n", read)
	
	read = re.sub(r"\\begin{([^{}]+?)}([ \t\r\n]*)\\end{\1}", r"\2", read)
	read = re.sub(r"\\end{(.+?)}([ \t\r\n]*)\\begin{\1}\n", r"\2\n", read)
	
	read = re.sub(r"(\A)\n+", r"\1", read)
	read = re.sub(r"(\A)[ \t\r\n]*\\\\", r"\1", read)
	read = re.sub(r"(\A)[ \t\r\n]*\\centereddots", r"\1", read)
	
	read = re.sub(r"\\\\([ \t\r\n]*\Z)", r"\1", read)
	read = re.sub(r"\\centereddots([ \t\r\n]*\Z)", r"\1", read)
	read = re.sub(r"[ \t\r\n]+(\n\Z)", r"\1", read)
	
	read = re.sub(regex_codes_html.space_line, r"\n", read)
	
	read = re.sub(r"\n{3,}", r"\n\n", read)
	
	return read

def lettrine(read, logger):
	read = re.sub(r"\\lettrine{(.+?)}([^\\\r\n{}]{,5}[a-z]*)", r"\\lettrine{\1}{\2}", read)
	return read


def handle_images(read, logger):
	while(re.search(regex_codes_html.include_graphics_underscore, read)):
		read = re.sub(regex_codes_html.include_graphics_underscore, r"\\includegraphics{\1_\2}", read)
	
	read = re.sub(regex_codes_html.chapter_image, r"\2", read)
	return read



def hyphen_quote(read, logger):
	read = re.sub(r"([`]+\-+)", r"\\mbox{\1}", read)
	read = re.sub(r"(\-+[']+)", r"\\mbox{\1}", read)
	return read


#Python modules
import os
import re
import logging
import shutil
import progressbar
import glob
#files for this program
import regex_codes
import format_css
import format_html
import format_opf
import format_toc
import format_xml
import hp_hyphenation

def fetch_file_counts(destpath):
	html_count = 0
	css_count = 0
	opf_count = 0
	for root, dirs, files in os.walk(destpath):
		for file in files:
			pre, ext = os.path.splitext(file)
			if(re.match(regex_codes.html_regex, ext)):
				html_count += 1
			elif(re.match(regex_codes.style_regex, ext)):
				css_count += 1
			elif(re.match(regex_codes.opf_regex, ext)):
				opf_count += 1
	return css_count, html_count, opf_count

def format_style_files(destpath, formatted_css, formatted_html, formatted_opf, bar, logger):
	styled_classes = set()
	styled_ids = set()
	change_rules = {}
	for root, dirs, files in os.walk(destpath):
		for file in files:
			bar.update(formatted_html + formatted_css + formatted_opf)
			pre, ext = os.path.splitext(file)
			if(re.match(regex_codes.style_regex, ext)):
				with open(os.path.join(root, file), 'r', encoding='utf-8') as dataIn:
					read = dataIn.read()
					new_styled_classes = format_css.get_styled_classes(read, logger)
					if(len(new_styled_classes) > 0):
						styled_classes = (styled_classes | new_styled_classes)
						for new_styled_class in new_styled_classes:
							if not (new_styled_class in format_css.acceptable_rules):
								change_rules[new_styled_class] = format_css.get_change_rules(new_styled_class, ".", read, logger)
					new_styled_ids = format_css.get_styled_ids(read, logger)
					if(len(new_styled_ids) > 0):
						styled_ids = (styled_ids | new_styled_ids)
						for new_styled_id in new_styled_ids:
							if not (new_styled_id in format_css.acceptable_rules):
								change_rules[new_styled_id] = format_css.get_change_rules(new_styled_id, "#", read, logger)
				formatted_css += 1
			bar.update(formatted_html + formatted_css + formatted_opf)
	kill = list()
	for id in change_rules.keys():
		if(len(change_rules[id]) < 1):
			kill.append(id)
	for id in kill:
		del change_rules[id]
	return formatted_css, formatted_html, formatted_opf, styled_classes, styled_ids, change_rules

def format_html_files(destpath, formatted_css, formatted_html, formatted_opf, html_count, styled_classes, styled_ids, change_rules, bar, logger):
	for root, dirs, files in os.walk(destpath):
		for file in files:
			bar.update(formatted_html + formatted_css + formatted_opf)
			pre, ext = os.path.splitext(file)
			if(re.match(regex_codes.html_regex, ext)):
				with open(os.path.join(root, file), 'r', encoding='utf-8') as dataIn:
					read = dataIn.read()
					relpath = os.path.relpath(root, destpath)
					logger.info("\t\t" + "HTML File: %s" % file)
					read = format_html.format_html(read, html_count > 2, relpath, styled_classes, styled_ids, change_rules, logger)
					with open(os.path.join(root, "%s.tex" % pre), 'w', encoding='utf-8') as dataOut:
						dataOut.write(read)
				formatted_html += 1
			bar.update(formatted_html + formatted_css + formatted_opf)
	return formatted_css, formatted_html, formatted_opf

def format_head_files(destpath, fandom, logger):
	logger.info("\t\t" + "Head File")
	with open(os.path.join(destpath, "head.tex"), 'w', encoding='utf-8') as headOut:
		headOut.write(format_opf.get_head_file(fandom, 'trade', logger))
	return

def format_opf_files(destpath, formatted_css, formatted_html, formatted_opf, html_count, fandom, bar, logger):
	for root, dirs, files in os.walk(destpath):
		for file in files:
			bar.update(formatted_html + formatted_css + formatted_opf)
			pre, ext = os.path.splitext(file)
			if(re.match(regex_codes.opf_regex, ext)):
				with open(os.path.join(root, file), 'r', encoding='utf-8') as dataIn:
					input = dataIn.read()
					if(os.path.exists(os.path.join(root, "%s.htm" % pre)) or os.path.exists(os.path.join(root, "%s.html" % pre)) or os.path.exists(os.path.join(root, "%s.xhtml" % pre))):
						logger.info("\t\t" + "HTML File with the same name exists.  Skipping.")
					else:
						logger.info("\t\t" + "OPF File: %s" % file)
						output, title = format_opf.format_opf(input, html_count > 2, fandom, logger)
						output_file = "%s.tex" % (re.sub(r"[^A-z0-9 _]", "_", title))
						if pre == 'content':
							with open(os.path.join(root, output_file), 'w', encoding='utf-8') as dataOut:
								dataOut.write(output)
						else:
							with open(os.path.join(root, "%s.tex" % pre), 'w', encoding='utf-8') as dataOut:
								dataOut.write(output)
				if(fandom):
					if(re.search("Harry Potter", fandom)):
						with open(os.path.join(root, "hp_hyphenation.tex"), 'w', encoding='utf-8') as dataOut:
							dataOut.write(hp_hyphenation.hp_hyphenation)
				formatted_opf += 1
			bar.update(formatted_html + formatted_css + formatted_opf)
	return formatted_css, formatted_html, formatted_opf


def format_files(destpath, fandom, logger):
	css_count, html_count, opf_count = fetch_file_counts(destpath)
	bar = progressbar.ProgressBar(max_value = html_count + css_count + opf_count)
	formatted_css = 0
	formatted_html = 0
	formatted_opf = 0
	formatted_css, formatted_html, formatted_opf, styled_classes, styled_ids, change_rules = format_style_files(destpath, formatted_css, formatted_html, formatted_opf, bar, logger)
	formatted_css, formatted_html, formatted_opf = format_html_files(destpath, formatted_css, formatted_html, formatted_opf, html_count, styled_classes, styled_ids, change_rules, bar, logger)
	format_head_files(destpath, fandom, logger)
	formatted_css, formatted_html, formatted_opf = format_opf_files(destpath, formatted_css, formatted_html, formatted_opf, html_count, fandom, bar, logger)
	print("")


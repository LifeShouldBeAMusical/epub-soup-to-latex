#Python modules
import re
import os
import logging
from bs4 import BeautifulSoup, Comment
from datetime import datetime
#files for this program
import regex_codes
import opf_templates as templates
from format_strings import filter_chars01, filter_chars02


def get_head_file(fandom, size, logger):
	result = templates.geometry
	if size == 'letter':
		result += templates.geometry_lettersize
	else:
		result += templates.geometry_tradesize
	result += templates.geometry_margins
	
	result += templates.symbols
	
	result += templates.font
	if(fandom):
		if(re.search("The 100", fandom)):
			result += templates.fonts_hundred
		elif(re.search("Danny Phantom", fandom)):
			result += templates.fonts_dp
		elif(re.search("Harry Potter", fandom)):
			result += templates.fonts_hp
		elif(re.search("Heathers", fandom)):
			result += templates.fonts_heathers
		elif(re.search("Kim Possible", fandom)):
			result += templates.fonts_kp
		elif(re.search("Star Wars", fandom)):
			result += templates.fonts_sw
		elif(re.search("Twilight", fandom)):
			result += templates.fonts_twilight
		elif(re.search("Wizard of Oz", fandom, re.IGNORECASE) or re.search("\bWicked\b", fandom)):
			result += templates.fonts_oz
		elif(re.search("Wynonna Earp", fandom)):
			result += templates.fonts_we
	
	result += templates.titles
	if(fandom):
		if(re.search("Harry Potter", fandom)):
			result += templates.commands_hp
	result += templates.misc
	
	result += templates.toc
	
	result += templates.images
	
	result += templates.underline
	
	result += templates.drop_caps
	
	result += templates.blockquotes
	
	result += templates.commands
	
	return result


def handle_date_tag(tag, logger):
	relevant = True
	if(len(tag.attrs) > 0):
		if('opf:event' in tag.attrs):
			if(tag['opf:event'] == 'creation'):
				relevant = False
			elif(tag['opf:event'] == 'modification'):
				relevant = False
	if relevant:
		try:
			tag_date = datetime.strptime(tag.string.strip().replace("+00:00", ''), "%Y-%m-%dT%H:%M:%S")
			tag.string.replace_with(tag_date.strftime("%Y-%m-%d"))
		except ValueError:
			try: 
				tag_date = datetime.strptime(tag.string.strip(), "%Y-%m-%d")
				tag.string.replace_with(tag_date.strftime("%Y-%m-%d"))
			except ValueError:
				tag.string.replace_with(tag.string.strip())
		tag.insert_before("\n" + "\\date{")
		tag.insert_after("}" + "\n")
		tag.unwrap()
	else:
		tag.replace_with("\n\n")
	return

def handle_creator_tag(tag, logger):
	tag.string.replace_with(tag.string.strip())
	found_author = False
	if(len(tag.attrs) > 0):
		for attr in tag.attrs:
			if re.match(r"(opf:|ns\d:|)role", attr):
				if tag[attr] == 'aut':
					# print("\\author{%s}" % (tag.string))
					tag.insert_before("\n" + "\\author{")
					tag.insert_after("}" + "\n")
					tag.unwrap()
					found_author = True
	if not found_author:
		tag.replace_with("\n\n")
	return

def handle_title_tag(tag, logger):
	title_string = tag.string.strip()
	title = tag.string.strip()
	# title_string = re.sub(r"&(amp;|)", r"\\&", title_string)
	tag.string.replace_with(title_string)
	title = re.sub(r"[^A-z0-9 ]+", r"_", title)
	title = re.sub(r"[_]*([ ]+)[_]*", r" ", title)
	title = re.sub(r"[ ]{2,}", r" ", title)
	tag.insert_before("\n" + "\\title{")
	tag.insert_after("}" + "\n")
	tag.unwrap()
	return title

def handle_source_tag(tag, logger):
	tag.string.replace_with(tag.string.strip())
	tag.insert_before("\n" + "\\date{\\texttt{")
	tag.insert_after("}}" + "\n")
	tag.unwrap()
	return

def handle_manifest_tag(tag, multichapter, logger):
	if(multichapter):
		tag.insert_before(templates.begin_multi)
	else:
		tag.insert_before(templates.begin_single)
	tag.insert_after("\n" + "\\end{document}" + "\n")
	tag.unwrap()
	return

def handle_item_tag(tag, logger):
	if(re.search(r"title[_]?page", tag['id'])):
		tag.replace_with("\n\n")
	elif('media-type' in tag.attrs):
		if(re.match("application/x?html?", tag['media-type'])):
			pre, ext = os.path.splitext(tag['href'])
			tag.replace_with("\n" + "\\include{" + pre + "}" + "\n")
		else:
			tag.replace_with("\n\n")
	else:
		tag.replace_with("\n\n")
	return


def format_opf(read, multichapter, fandom, logger):
	soup = BeautifulSoup(read, 'lxml')
	title = None
	#Remove comments
	for comment in soup.find_all(string=lambda text:isinstance(text, Comment)):
		comment.extract()
	
	
	for tag in soup.find_all(templates.unwrap_tags):
		tag.insert_before("\n\n")
		tag.insert_after("\n\n")
		tag.unwrap()
	for tag in soup.find_all(templates.package_tags):
		tag.insert_before("\n\n" + "\\input{head}" + "\n\n")
		tag.unwrap()
	for tag in soup.find_all(templates.title_tags):
		title = handle_title_tag(tag, logger)
	for tag in soup.find_all(templates.source_tags):
		handle_source_tag(tag, logger)
	for tag in soup.find_all(templates.manifest_tags):
		handle_manifest_tag(tag, multichapter, logger)
	for tag in soup.find_all(templates.item_tags):
		handle_item_tag(tag, logger)
	for tag in soup.find_all(templates.date_tags):
		handle_date_tag(tag, logger)
	for tag in soup.find_all(templates.creator_tags):
		handle_creator_tag(tag, logger)
	for tag in soup.find_all(templates.remove_tags):
		tag.replace_with("\n\n")
	for tag in soup.find_all(True):
		tag.insert_before("\n")
		tag.insert_after("\n")
		logger.warning("\t\t\t" + tag.name)
	
	read = str(soup)
	read = re.sub(r"<\?xml[^>]*\?>[\r\n]*", templates.doc_dec_12, read)
	
	while(re.search(templates.title_underscore, read)):
		read = re.sub(templates.title_underscore, r"\\\1{\2\_\3}", read)
	
	read = re.sub("([&#$])", r"\\\1", read)
	read = re.sub("(&)amp;", r"\1", read, flags=re.IGNORECASE)
	
	read = re.sub(r"[ \t\r]+\n", r"\n", read)
	read = re.sub(r"\n{3,}", r"\n\n", read)
	
	read = re.sub(r"(\A)\n+", r"\1", read)
	read = re.sub(r"[ \t\r\n]+(\n\Z)", r"\1", read)

	return read, title


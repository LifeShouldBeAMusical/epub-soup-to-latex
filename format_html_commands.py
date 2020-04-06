#Python modules
import re
import os
import logging
from bs4 import BeautifulSoup, Comment
from titlecase import titlecase
#files for this program
from format_strings import filter_chars01, filter_chars02
import regex_codes_html


def swap_tags_commands(soup, multichapter, relpath, logger):
	
	for tag in soup.find_all(True):
		if('id' in tag.attrs):
			del tag['id']
		if('class' in tag.attrs):
			if('kill' in tag['class']):
				tag.extract()
			if('block' in tag['class']):
				tag.insert_before("\n\n")
				tag.insert_after("\n\n")
				tag['class'].remove('block')
			if('userstuff' in tag['class']):
				tag['class'].remove('userstuff')
	
	soup = swap_inline_tags(soup, logger)
	soup = swap_title_tags(soup, multichapter, logger)
	soup = swap_div_tags(soup, logger)
	soup = swap_p_tags(soup, logger)
	soup = swap_list_tags(soup, logger)
	soup = swap_bhr_tags(soup, logger)
	soup = swap_image_tags(soup, relpath, logger)
	
	#else
	for tag in soup.find_all(True):
		logger.warning("\t\t\t" + tag.name)

	return soup


def swap_inline_tags(soup, logger):
	soup = swap_italic_tags(soup, logger)
	soup = swap_bold_tags(soup, logger)
	soup = swap_strike_tags(soup, logger)
	soup = swap_super_tags(soup, logger)
	soup = swap_sub_tags(soup, logger)
	soup = swap_under_tags(soup, logger)
	soup = swap_cite_tags(soup, logger)
	soup = swap_span_tags(soup, logger)
	return soup

def swap_italic_tags(soup, logger):
	emphs = 0
	for tag in soup.find_all(['em', 'i']):
		if len(tag.parent.contents) == 1 and tag.parent.name == 'p':
			tag.insert_before("{\\itshape\n")
			tag.insert_after("\n} ||itshape||")
		else:
			tag.insert_before("\\textit{")
			tag.insert_after("}")
		tag.unwrap()
		emphs += 1
	if(emphs > 0):
		logger.info("\t\t\t" + "Italic tags replaced: %d" % emphs)
	return soup

def swap_bold_tags(soup, logger):
	bolds = 0
	for tag in soup.find_all(['strong', 'b']):
		tag.insert_before("\\textbf{")
		tag.insert_after("}")
		tag.unwrap()
		bolds += 1
	if(bolds > 0):
		logger.info("\t\t\t" + "Bold tags replaced: %d" % bolds)
	return soup

def swap_strike_tags(soup, logger):
	strikes = 0
	for tag in soup.find_all(['strike', 's']):
		tag.insert_before("\\sout{")
		tag.insert_after("}")
		tag.unwrap()
		strikes += 1
	if(strikes > 0):
		logger.info("\t\t\t" + "Strike tags replaced: %d" % strikes)
	return soup

def swap_super_tags(soup, logger):
	sups = 0
	for tag in soup.find_all('sup'):
		tag.insert_before("\\textsuperscript{")
		tag.insert_after("}")
		tag.unwrap()
		sups += 1
	if(sups > 0):
		logger.info("\t\t\t" + "Supertext tags replaced: %d" % sups)
	return soup

def swap_sub_tags(soup, logger):
	subs = 0
	for tag in soup.find_all('sub'):
		tag.insert_before("\\textsubscript{")
		tag.insert_after("}")
		tag.unwrap()
		subs += 1
	if(subs > 0):
		logger.info("\t\t\t" + "Subtext tags replaced: %d" % subs)
	return soup

def swap_under_tags(soup, logger):
	unders = 0
	for tag in soup.find_all('u'):
		tag.insert_before("\\uline{")
		tag.insert_after("}")
		tag.unwrap()
		unders += 1
	if(unders > 0):
		logger.info("\t\t\t" + "Underline tags replaced: %d" % unders)
	return soup

def swap_cite_tags(soup, logger):
	for tag in soup.find_all('cite'):
		if(len(tag.attrs) == 0):
			tag.insert_before("\\textit{")
			tag.insert_after("}")
			tag.unwrap()
		else:
			tag = handle_typeface(tag, logger)
			if('class' in tag.attrs):
				if('italic' in tag['class']):
					tag.insert_before("\\textit{")
					tag.insert_after("}")
					tag['class'].remove('italic')
				if('italics' in tag['class']):
					tag.insert_before("\\textit{")
					tag.insert_after("}")
					tag['class'].remove('italics')
				if('bold' in tag['class']):
					tag.insert_before("\\textbf{")
					tag.insert_after("}")
					tag['class'].remove('bold')
				if(len(tag['class']) == 0):
					del tag['class']
			if(len(tag.attrs) == 0):
				tag.unwrap()
			else:
				logger.warning("\t\t\t" + tag.name + "\t" + str(tag.attrs))
	return soup

def swap_span_tags(soup, logger):
	for tag in soup.find_all('span'):
		tag = handle_typeface(tag, logger)
		if('class' in tag.attrs):
			if('dropcap' in tag['class']):
				tag.insert_before("\\lettrine{")
				tag.insert_after("}")
				tag['class'].remove('dropcap')
			if('firstletter' in tag['class']):
				tag.insert_before("\\lettrine{")
				tag.insert_after("}")
				tag['class'].remove('firstletter')
			if('big' in tag['class']):
				tag.insert_before("{\\large{")
				tag.insert_after("}}")
				tag['class'].remove('big')
			if('small-caps' in tag['class']):
				tag.insert_before("\\textsc{")
				tag.insert_after("}")
				tag['class'].remove('small-caps')
			if('large' in tag['class']):
				tag.insert_before("{\\large{")
				tag.insert_after("}}")
				tag['class'].remove('large')
			if('x-large' in tag['class']):
				tag.insert_before("{\\Large{")
				tag.insert_after("}}")
				tag['class'].remove('x-large')
			if(len(tag['class']) == 0):
				del tag['class']
		if(len(tag.attrs) == 0):
			tag.unwrap()
		else:
			logger.warning("\t\t\t" + tag.name + "\t" + str(tag.attrs))
	return soup


def swap_title_tags(soup, multichapter, logger):
	#h\d tags
	h1s = 0
	h2s = 0
	h3s = 0
	h4s = 0
	h5s = 0
	h6s = 0
	for tag in soup.find_all('h1'):
		tag.insert_before("\n\n" + "\\part{")
		tag.insert_after("}" + "\n\n")
		tag.unwrap()
		h1s += 1
	if(h1s > 0):
		logger.info("\t\t\t" + "H1 tags replaced: %d" % h1s)
	for tag in soup.find_all('h2'):
		tag.insert_before("\n\n" + "\\part{")
		tag.insert_after("}" + "\n\n")
		tag.unwrap()
		h2s += 1
	if(h2s > 0):
		logger.info("\t\t\t" + "H2 tags replaced: %d" % h2s)
	for tag in soup.find_all('h3'):
		if(multichapter):
			tag.insert_before("\n\n" + "\\chapter{")
		else:
			tag.insert_before("\n\n" + "\\unnumberedchapter{")
		tag.insert_after("}" + "\n\n")
		tag.unwrap()
		h3s += 1
	if(h3s > 0):
		logger.info("\t\t\t" + "H3 tags replaced: %d" % h3s)
	for tag in soup.find_all('h4'):
		tag.insert_before("\n\n" + "\\section*{")
		tag.insert_after("}" + "\n\n")
		tag.unwrap()
		h4s += 1
	if(h4s > 0):
		logger.info("\t\t\t" + "H4 tags replaced: %d" % h4s)
	for tag in soup.find_all('h5'):
		tag.insert_before("\n\n" + "\\subsection*{")
		tag.insert_after("}" + "\n\n")
		tag.unwrap()
		h5s += 1
	if(h5s > 0):
		logger.info("\t\t\t" + "H5 tags replaced: %d" % h5s)
	for tag in soup.find_all('h6'):
		tag.insert_before("\n\n" + "\\subsubsection*{")
		tag.insert_after("}" + "\n\n")
		tag.unwrap()
		h6s += 1
	if(h6s > 0):
		logger.info("\t\t\t" + "H6 tags replaced: %d" % h6s)
	return soup

def swap_div_tags(soup, logger):
	#div tags
	div_blank = 0
	div_left = 0
	div_right = 0
	div_center = 0
	div_meh = 0
	div_byline = 0
	div_noindent = 0
	div_block = 0
	div_hang = 0
	div_font = 0
	div_email = 0
	blocks = 0
	block_left = 0
	block_center = 0
	block_right = 0
	block_hang = 0
	block_noindent = 0
	for tag in soup.find_all('center'):
		tag.insert_before("\n\n" + "\\begin{center}" + "\n")
		tag.insert_after("\n" + "\\end{center}" + "\n\n")
		tag.unwrap()
		div_center += 1
	for tag in soup.find_all('div'):
		tag.insert_before("\n\n")
		tag.insert_after("\n\n")
		tag = handle_hang_para(tag, logger)
		tag = handle_align(tag, logger)
		tag = handle_margins(tag, logger)
		tag = handle_padding(tag, logger)
		tag = handle_typeface(tag, logger)
		if('class' in tag.attrs):
			if('first' in tag['class']):
				div_meh += 1
				tag['class'].remove('first')
			if('container' in tag['class']):
				div_meh += 1
				tag['class'].remove('container')
			if('section' in tag['class']):
				div_meh += 1
				tag['class'].remove('section')
			if('level-2' in tag['class']):
				div_meh += 1
				tag['class'].remove('level-2')
			if('level-3' in tag['class']):
				div_meh += 1
				tag['class'].remove('level-3')
			if('message' in tag['class']):
				tag.insert_before("\\begin{textmessage}" + "\n")
				tag.insert_after("\n" + "\\end{textmessage}")
				div_hang += 1
				tag['class'].remove('message')
			if('monospace' in tag['class']):
				tag.insert_before("\n" + "\\begin{courier}" + "\n")
				tag.insert_after("\n" + "\\end{courier}" + "\n")
				div_font += 1
				tag['class'].remove('monospace')
			if('center' in tag['class']):
				tag.insert_before("\\begin{center}" + "\n")
				tag.insert_after("\n" + "\\end{center}")
				div_center += 1
				tag['class'].remove('center')
			if('byline' in tag['class']):
				tag.insert_before("\\begin{center}" + "\n")
				tag.insert_after("\n" + "\\end{center}")
				div_byline += 1
				tag['class'].remove('byline')
			if('story' in tag['class']):
				div_meh += 1
				tag['class'].remove('story')
			if('storytext' in tag['class']):
				div_meh += 1
				tag['class'].remove('storytext')
			if('storytextp' in tag['class']):
				div_meh += 1
				tag['class'].remove('storytextp')
			if('meta' in tag['class']):
				div_meh += 1
				tag['class'].remove('meta')
			if('line-block' in tag['class']):
				tag.insert_before("\n" + "\\vspace{1em}" + "\n")
				tag.insert_after("\n" + "\\vspace{1em}" + "\n")
				div_block += 1
				tag['class'].remove('line-block')
			if('transition' in tag['class']):
				tag.insert_before("\n" + "\\vspace{1em}" + "\n")
				tag.insert_after("\n" + "\\vspace{1em}" + "\n")
				div_block += 1
				tag['class'].remove('transition')
			if('line' in tag['class']):
				tag.insert_before("\\setlength{\\parindent}{0pt}" + "\n")
				tag.insert_after("\n" + "\\setlength{\\parindent}{15pt}")
				div_noindent += 1
				tag['class'].remove('line')
			if('email' in tag['class']):
				# tag.insert_before("\\setlength{\\parindent}{0pt}" + "\n")
				# tag.insert_after("\n" + "\\setlength{\\parindent}{15pt}")
				tag.insert_before("\\begin{adjustwidth*}{%s}{%s}" % ('1em', '1em'))
				tag.insert_after("\n" + "\\end{adjustwidth*}")
				div_email += 1
				tag['class'].remove('email')
			if('noindent' in tag['class']):
				tag.insert_before("\\setlength{\\parindent}{0pt}" + "\n")
				tag.insert_after("\n" + "\\setlength{\\parindent}{15pt}")
				div_noindent += 1
				tag['class'].remove('noindent')
			if(len(tag['class']) == 0):
				del tag['class']
		if(len(tag.attrs) == 0):
			tag.unwrap()
		else:
			logger.warning("\t\t\t" + tag.name + "\t" + str(tag.attrs))
	for tag in soup.find_all('blockquote'):
		tag.insert_before("\n\n" + "\\begin{displayquote}" + "\n")
		tag.insert_after("\n" + "\\end{displayquote}" + "\n\n")
		tag = handle_align(tag, logger)
		tag = handle_typeface(tag, logger)
		if('class' in tag.attrs):
			if('userstuff' in tag['class']):
				tag['class'].remove('userstuff')
			if('message' in tag['class']):
				tag.insert_before("\\begin{textmessage}" + "\n")
				tag.insert_after("\n" + "\\end{textmessage}")
				block_hang += 1
				tag['class'].remove('message')
			if('noindent' in tag['class']):
				tag.insert_before("\\setlength{\\parindent}{0pt}" + "\n")
				tag.insert_after("\n" + "\\setlength{\\parindent}{15pt}")
				block_noindent += 1
				tag['class'].remove('noindent')
			if(len(tag['class']) == 0):
				del tag['class']
		if(len(tag.attrs) == 0):
			tag.unwrap()
			blocks += 1
		else:
			logger.warning("\t\t\t" + tag.name + "\t" + str(tag.attrs))
	if(div_blank > 0):
		logger.info("\t\t\t" + "Blank div tags replaced: %d" % div_blank)
	if(div_left > 0):
		logger.info("\t\t\t" + "Left div tags replaced: %d" % div_left)
	if(div_right > 0):
		logger.info("\t\t\t" + "Right div tags replaced: %d" % div_right)
	if(div_center > 0):
		logger.info("\t\t\t" + "Center div tags replaced: %d" % div_center)
	if(div_block > 0):
		logger.info("\t\t\t" + "Block div tags replaced: %d" % div_block)
	if(div_hang > 0):
		logger.info("\t\t\t" + "Hang/message div tags replaced: %d" % div_hang)
	if(div_noindent > 0):
		logger.info("\t\t\t" + "No-indent div tags replaced: %d" % div_noindent)
	if(div_byline > 0):
		logger.info("\t\t\t" + "Byline div tags replaced: %d" % div_byline)
	if(div_font > 0):
		logger.info("\t\t\t" + "Font div tags replaced: %d" % div_font)
	if(div_meh > 0):
		logger.info("\t\t\t" + "Other div tags replaced: %d" % div_meh)
	if(blocks > 0):
		logger.info("\t\t\t" + "Blockquote tags replaced: %d" % blocks)
	if(block_left > 0):
		logger.info("\t\t\t" + "Left blockquote tags replaced: %d" % block_left)
	if(block_right > 0):
		logger.info("\t\t\t" + "Right blockquote tags replaced: %d" % block_right)
	if(block_center > 0):
		logger.info("\t\t\t" + "Center blockquote tags replaced: %d" % block_center)
	if(block_hang > 0):
		logger.info("\t\t\t" + "Hang blockquote tags replaced: %d" % block_hang)
	if(block_noindent > 0):
		logger.info("\t\t\t" + "No-indent blockquote tags replaced: %d" % block_noindent)
	return soup

def swap_p_tags(soup, logger):
	#p tags
	p_blank = 0
	p_left = 0
	p_right = 0
	p_center = 0
	p_font = 0
	p_address = 0
	p_message = 0
	p_byline = 0
	p_first = 0
	p_noindent = 0
	for tag in soup.find_all('p'):
		tag.insert_before("\n\n")
		tag.insert_after("\n\n")
		tag = handle_align(tag, logger)
		tag = handle_hang_para(tag, logger)
		tag = handle_margins(tag, logger)
		tag = handle_padding(tag, logger)
		tag = handle_typeface(tag, logger)
		if('class' in tag.attrs):
			if('center' in tag['class']):
				tag.insert_before("\\begin{center}" + "\n")
				tag.insert_after("\n" + "\\end{center}")
				p_center += 1
				tag['class'].remove('center')
			if('right' in tag['class']):
				tag.insert_before("\\begin{flushright}" + "\n")
				tag.insert_after("\n" + "\\end{flushright}")
				p_right += 1
				tag['class'].remove('right')
			if('message' in tag['class']):
				tag.insert_before("\\hangpara{2em}{1}" + "\n")
				p_message += 1
				tag['class'].remove('message')
			if('byline' in tag['class']):
				tag.insert_before("\\begin{center}" + "\n")
				tag.insert_after("\n" + "\\end{center}")
				p_byline += 1
				tag['class'].remove('byline')
			if('address' in tag['class']):
				tag.insert_before("\n\n" + "\\begin{displayquote}" + "\n")
				tag.insert_after("\n" + "\\end{displayquote}" + "\n\n")
				p_address += 1
				tag['class'].remove('address')
			if('monospace' in tag['class']):
				tag.insert_before("\n\n" + "\\begin{courier}" + "\n")
				tag.insert_after("\n" + "\\end{courier}" + "\n\n")
				tag['class'].remove('monospace')
				p_font += 1
			if('western' in tag['class']):
				tag['class'].remove('western')
			if('first' in tag['class']):
				p_first += 1
				tag['class'].remove('first')
			if('pfirst' in tag['class']):
				tag.insert_before("\\noindent" + "\n")
				p_first += 1
				tag['class'].remove('pfirst')
			if('noindent' in tag['class']):
				tag.insert_before("\\noindent" + "\n")
				p_noindent += 1
				tag['class'].remove('noindent')
			if(len(tag['class']) == 0):
				del tag['class']
		if('dir' in tag.attrs):
			if(tag['dir'] == 'ltr'):
				del tag['dir']
		if(len(tag.attrs) == 0):
			tag.unwrap()
		else:
			logger.warning("\t\t\t" + tag.name + "\t" + str(tag.attrs))
	if(p_blank > 0):
		logger.info("\t\t\t" + "Blank p tags replaced: %d" % p_blank)
	if(p_first > 0):
		logger.info("\t\t\t" + "First p tags replaced: %d" % p_first)
	if(p_noindent > 0):
		logger.info("\t\t\t" + "No-indent p tags replaced: %d" % p_noindent)
	if(p_left > 0):
		logger.info("\t\t\t" + "Left p tags replaced: %d" % p_left)
	if(p_right > 0):
		logger.info("\t\t\t" + "Right p tags replaced: %d" % p_right)
	if(p_center > 0):
		logger.info("\t\t\t" + "Center p tags replaced: %d" % p_center)
	if(p_address > 0):
		logger.info("\t\t\t" + "Address p tags replaced: %d" % p_address)
	if(p_message > 0):
		logger.info("\t\t\t" + "Message p tags replaced: %d" % p_message)
	if(p_byline > 0):
		logger.info("\t\t\t" + "Byline p tags replaced: %d" % p_byline)
	if(p_font > 0):
		logger.info("\t\t\t" + "Font p tags replaced: %d" % p_font)
	return soup

def swap_list_tags(soup, logger):
	#lists
	ols = 0
	uls = 0
	lis = 0
	for tag in soup.find_all('ol'):
		tag.insert_before("\n\n" + "\\begin{enumerate}" + "\n")
		tag.insert_after("\n" + "\\end{enumerate}" + "\n\n")
		tag = handle_align(tag, logger)
		tag.unwrap()
		ols += 1
	if(ols > 0):
		logger.info("\t\t\t" + "Ordered list tags replaced: %d" % ols)
	for tag in soup.find_all('ul'):
		tag.insert_before("\n\n" + "\\begin{itemize}" + "\n")
		tag.insert_after("\n" + "\\end{itemize}" + "\n\n")
		tag = handle_align(tag, logger)
		tag.unwrap()
		uls += 1
	if(uls > 0):
		logger.info("\t\t\t" + "Unordered list tags replaced: %d" % uls)
	for tag in soup.find_all('li'):
		tag.insert_before("\n\n" + "\\item ")
		tag.insert_after("\n\n")
		tag.unwrap()
		lis += 1
	if(lis > 0):
		logger.info("\t\t\t" + "List item tags replaced: %d" % lis)
	return soup

def swap_bhr_tags(soup, logger):
	brs = 0
	hrs = 0
	#br
	for tag in soup.find_all('br'):
		tag.replace_with(" \\\\ ")
		brs += 1
	if(brs > 0):
		logger.info("\t\t\t" + "Br tags replaced: %d" % brs)
	#hr
	for tag in soup.find_all('hr'):
		tag.replace_with("\n\n\\centereddots\n\n")
		hrs += 1
	if(hrs > 0):
		logger.info("\t\t\t" + "Hr tags replaced: %d" % hrs)
	return soup

def swap_image_tags(soup, relpath, logger):
	#images
	img_alt = 0
	img_saved = 0
	img_removed = 0
	for tag in soup.find_all('img'):
		tag = handle_align(tag, logger)
		if('src' in tag.attrs):
			if(tag['src'] == 'failedtoload'):
				if('alt' in tag.attrs):
					tag.replace_with("\n\n" + tag['alt'] + "\n\n")
					img_alt += 1
				else:
					tag.decompose()
					img_removed += 1
			else:
				tag.replace_with("\n\n" + "\\includegraphics{" + relpath + "/" + tag['src'] + "}" + "\n\n")
				img_saved += 1
		else:
			tag.decompose()
			img_removed += 1
	if(img_alt > 0):
		logger.info("\t\t\t" + "Images replaced with alt text: %d" % img_alt)
	if(img_removed > 0):
		logger.info("\t\t\t" + "Images removed: %d" % img_removed)
	if(img_saved > 0):
		logger.info("\t\t\t" + "Image tags replaced: %d" % img_saved)
	return soup


def handle_align(tag, logger):
	if('align' in tag.attrs):
		if(tag['align'].lower() == 'left'):
			tag.insert_before("\\begin{flushleft}" + "\n")
			tag.insert_after("\n" + "\\end{flushleft}")
			del tag['align']
		elif(tag['align'].lower() == 'right'):
			tag.insert_before("\\begin{flushright}" + "\n")
			tag.insert_after("\n" + "\\end{flushright}")
			del tag['align']
		elif(tag['align'].lower() == 'center'):
			tag.insert_before("\\begin{center}" + "\n")
			tag.insert_after("\n" + "\\end{center}")
			del tag['align']
		else:
			logger.warning("\t\t\t" + "Unhandled alignment")
	if('class' in tag.attrs):
		if('left' in tag['class']):
			tag.insert_before("\\begin{flushleft}" + "\n")
			tag.insert_after("\n" + "\\end{flushleft}")
			tag['class'].remove('left')
		if('right' in tag['class']):
			tag.insert_before("\\begin{flushright}" + "\n")
			tag.insert_after("\n" + "\\end{flushright}")
			tag['class'].remove('right')
		if('center' in tag['class']):
			tag.insert_before("\\begin{center}" + "\n")
			tag.insert_after("\n" + "\\end{center}")
			tag['class'].remove('center')
		if('justify' in tag['class']):
			tag['class'].remove('justify')
	return tag

def handle_page_break(tag, logger):
	if('class' in tag.attrs):
		if('page_break_after_always' in tag['class']):
			tag.insert_after("\n\n" + "\\clearpage" + "\n\n")
			tag['class'].remove('page_break_after_always')
		if('page_break_after_left' in tag['class']):
			tag.insert_after("\n\n" + "\\cleartoleftpage" + "\n\n")
			tag['class'].remove('page_break_after_left')
		if('page_break_after_right' in tag['class']):
			tag.insert_after("\n\n" + "\\cleardoublepage" + "\n\n")
			tag['class'].remove('page_break_after_right')
		if('page_break_before_always' in tag['class']):
			tag.insert_before("\n\n" + "\\clearpage" + "\n\n")
			tag['class'].remove('page_break_before_always')
		if('page_break_before_left' in tag['class']):
			tag.insert_before("\n\n" + "\\cleartoleftpage" + "\n\n")
			tag['class'].remove('page_break_before_left')
		if('page_break_before_right' in tag['class']):
			tag.insert_before("\n\n" + "\\cleardoublepage" + "\n\n")
			tag['class'].remove('page_break_before_right')
	return tag

def handle_hang_para(tag, logger):
	if('class' in tag.attrs):
		left = "0in"
		indent = "0in"
		for class_id in tag['class'].copy():
			if(re.match(regex_codes_html.margin, class_id)):
				match = re.match(regex_codes_html.margin, class_id)
				left = match.group(1)
			elif(re.match(regex_codes_html.text_indent, class_id)):
				match = re.match(regex_codes_html.text_indent, class_id)
				indent = match.group(1)
		if((left == indent) and (left != "0in")):
			tag.insert_before("\n")
			tag.insert_before("\\begin{hangparas}{%s}{1}" % left)
			tag.insert_before("\n")
			tag.insert_after("\n")
			tag.insert_after("\\end{hangparas}")
			tag.insert_after("\n")
			tag['class'].remove("margin_left_%s" % left)
			tag['class'].remove("indent_-%s" % indent)
	return tag

def handle_margins(tag, logger):
	return handle_spacing(tag, logger)

def handle_padding(tag, logger):
	return handle_spacing(tag, logger)

def handle_spacing(tag, logger):
	page_width = 6
	page_margin_left = 0.5
	page_margin_right = 0.5
	page_margin_spine = 0.3
	page_height = 9
	page_margin_top = 0.8
	page_margin_bottom = 0.5
	
	if('class' in tag.attrs):
		top = "0in"
		bottom = "0in"
		left = "0in"
		right = "0in"
		for class_id in tag['class'].copy():
			if(re.match(regex_codes_html.spacing, class_id)):
				match = re.match(regex_codes_html.spacing, class_id)
				tag['class'].remove(class_id)
				if(match.group(2) == 'left'):
					if(match.group(4) == '%'):
						left = str((page_width - page_margin_left - page_margin_right - page_margin_spine) * float(match.group(3)) / 100) + "in"
					else:
						left = "%s%s" % (match.group(3), match.group(4))
				elif(match.group(2) == 'right'):
					if(match.group(4) == '%'):
						right = str((page_width - page_margin_left - page_margin_right - page_margin_spine) * float(match.group(3)) / 100) + "in"
					else:
						right = "%s%s" % (match.group(3), match.group(4))
				elif(match.group(2) == 'top'):
					if(match.group(4) == '%'):
						top = str((page_height - page_margin_top - page_margin_bottom) * float(match.group(3)) / 100) + "in"
					else:
						top = "%s%s" % (match.group(3), match.group(4))
				elif(match.group(2) == 'bottom'):
					if(match.group(4) == '%'):
						bottom = str((page_height - page_margin_top - page_margin_bottom) * float(match.group(3)) / 100) + "in"
					else:
						bottom = "%s%s" % (match.group(3), match.group(4))
		if(top != "0in"):
			tag.insert_before("\n")
			tag.insert_before("\\vspace*{%s}" % top)
			tag.insert_before("\n")
			logger.info("\t\t\t" + "Added %s space to top" % top)
		if(tag.name != 'blockquote'):
			if((left != "0in") or (right != "0in")):
				tag.insert_before("\n\n")
				tag.insert_before("\\begin{adjustwidth*}{%s}{%s}" % (left, right))
				tag.insert_before("\n")
				tag.insert_after("\n\n")
				tag.insert_after("\\end{adjustwidth*}")
				tag.insert_after("\n")
				logger.info("\t\t\t" + "Added %s space to left, %s space to right" % (left, right))
		if(bottom != "0in"):
			tag.insert_after("\n")
			tag.insert_after("\\vspace*{%s}" % top)
			tag.insert_after("\n")
			logger.info("\t\t\t" + "Added %s space to bottom" % bottom)
	return tag

def handle_typeface(tag, logger):
	if('class' in tag.attrs):
		if('monospace' in tag['class']):
			if(tag.name in inline_tag_set):
				tag.insert_before("\\texttt{")
				tag.insert_after("}")
			else:
				tag.insert_before("\n\n" + "\\begin{courier}" + "\n")
				tag.insert_after("\n" + "\\end{courier}" + "\n\n")
			tag['class'].remove('monospace')
		if('sansserif' in tag['class']):
			if(tag.name in inline_tag_set):
				tag.insert_before("\\textsf{")
				tag.insert_after("}")
			else:
				tag.insert_before("\n\n" + "\\begin{sansserif}" + "\n")
				tag.insert_after("\n" + "\\end{sansserif}" + "\n\n")
			tag['class'].remove('sansserif')
		for class_id in tag['class'].copy():
			if re.match(regex_codes_html.font_size, class_id):
				match = re.match(regex_codes_html.font_size, class_id)
				the_size = int(match.group(1))
				if the_size <= 70:
					print("tiny")
					tag.insert_before("\n" + "{\\tiny" + "\n")
					tag.insert_after("\n" + "}" + "\n")
				if the_size > 70 and the_size <= 80:
					print("scriptsize")
					tag.insert_before("\n" + "{\\scriptsize" + "\n")
					tag.insert_after("\n" + "}" + "\n")
				if the_size > 80 and the_size <= 90:
					print("footnotesize")
					tag.insert_before("\n" + "{\\footnotesize" + "\n")
					tag.insert_after("\n" + "}" + "\n")
				if the_size > 90 and the_size < 100:
					print("small")
					tag.insert_before("\n" + "{\\small" + "\n")
					tag.insert_after("\n" + "}" + "\n")
				if the_size == 100:
					print("Normal Size")
					tag.insert_before("\n" + "{\\normalsize" + "\n")
					tag.insert_after("\n" + "}" + "\n")
				elif the_size > 100 and the_size <= 120:
					print("large")
					tag.insert_before("\n" + "{\\large" + "\n")
					tag.insert_after("\n" + "}" + "\n")
				elif the_size > 120 and the_size <= 144:
					print("Large")
					tag.insert_before("\n" + "{\\Large" + "\n")
					tag.insert_after("\n" + "}" + "\n")
				elif the_size > 144 and the_size <= 173:
					print("LARGE")
					tag.insert_before("\n" + "{\\LARGE" + "\n")
					tag.insert_after("\n" + "}" + "\n")
				elif the_size > 173 and the_size <= 200:
					print("huge")
					tag.insert_before("\n" + "{\\huge" + "\n")
					tag.insert_after("\n" + "}" + "\n")
				elif the_size > 200:
					print("HUGE")
					tag.insert_before("\n" + "{\\HUGE" + "\n")
					tag.insert_after("\n" + "}" + "\n")
				tag['class'].remove(class_id)
	return tag


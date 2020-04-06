#Python modules
import re
import logging
#files for this program
import regex_codes


def format_css(read, logger):
	return read

def get_styled_classes(read, logger):
	read = re.sub(r"/\*.*?\*/", r"", read, flags=re.DOTALL)
	read = re.sub(r"{.*?}", r"", read, flags=re.DOTALL)
	read = re.sub(r"[>,+]", r"\n", read)
	#print(read)
	
	return set(re.findall(r"\.([^ \r\n.,>+]+)", read))

def get_styled_ids(read, logger):
	read = re.sub(r"/\*.*?\*/", r"", read, flags=re.DOTALL)
	read = re.sub(r"{.*?}", r"", read, flags=re.DOTALL)
	read = re.sub(r"[>,+]", r"\n", read)
	#print(read)
	
	return set(re.findall(r"#([^ \r\n.,>+]+)", read))

def get_classes_from_rule(rule, logger):
	result = list()
	#bold
	if(re.search(regex_codes.bold_css_regex, rule)):
		result.append("bold")
	#italic
	if(re.search(regex_codes.italic_css_regex, rule)):
		result.append("italic")
	#strike
	if(re.search(regex_codes.strike_css_regex, rule)):
		result.append("strike")
	#underline
	if(re.search(regex_codes.underline_css_regex, rule)):
		result.append("underline")
	#small caps
	if(re.search(regex_codes.small_caps_css_regex, rule)):
		result.append("small_caps")
	#fonts
	if(re.search(regex_codes.font_family_regex, rule)):
		match = re.search(regex_codes.font_family_regex, rule)
		result.append(match.group(1))
	#font size
	if(re.search(regex_codes.font_size, rule)):
		match = re.search(regex_codes.font_size, rule)
		result.append("font_size_%s%s" % (match.group(1), match.group(2)))
	if(re.search(regex_codes.font_size_other, rule)):
		match = re.search(regex_codes.font_size_other, rule)
		result.append("font_size_%s" % match.group(1))
		
	#display
	if(re.search(regex_codes.display_regex, rule)):
		match = re.search(regex_codes.display_regex, rule)
		if(match.group(1) == 'none'):
			result.append("kill")
		else:
			result.append(match.group(1))
	#page-break
	if(re.search(regex_codes.page_break, rule)):
		for match in re.finditer(regex_codes.page_break, rule):
			result.append("page_break_%s_%s" % (match.group(1), match.group(2)))
	#alignment
	if(re.search(regex_codes.align_regex, rule)):
		match = re.search(regex_codes.align_regex, rule)
		result.append(match.group(1))
	#indent
	if(re.search(regex_codes.text_indent, rule)):
		match = re.search(regex_codes.text_indent, rule)
		if(match.group(1) == '0'):
			result.append("noindent")
		else:
			result.append("indent_%s%s" % (match.group(1), match.group(2)))
	#line height
	if(re.search(regex_codes.line_height, rule)):
		match = re.search(regex_codes.line_height, rule)
		result.append("line_spacing_%s" % match.group(1))
	#spacing
	#Hyphen
	if(re.search(regex_codes.no_hyphen, rule)):
		result.append("no_hyphen")
	#spacing single value specified
	if(re.search(regex_codes.spacing_single, rule)):
		for match in re.finditer(regex_codes.spacing_single, rule):
			if(match.group(3) != '0'):
				result.append("%s_%s_%s%s" % (match.group(1), match.group(2), match.group(3), match.group(4)))
	if(re.search(regex_codes.spacing_four, rule)):
		for match in re.finditer(regex_codes.spacing_four, rule):
			if(match.group(2) != '0'):
				result.append("%s_top_%s" % (match.group(1), match.group(2)))
			if(match.group(4) != '0'):
				result.append("%s_bottom_%s" % (match.group(1), match.group(4)))
			if(match.group(3) != '0'):
				result.append("%s_right_%s" % (match.group(1), match.group(3)))
			if(match.group(5) != '0'):
				result.append("%s_left_%s" % (match.group(1), match.group(5)))
	elif(re.search(regex_codes.spacing_three, rule)):
		for match in re.finditer(regex_codes.spacing_four, rule):
			if(match.group(2) != '0'):
				result.append("%s_top_%s" % (match.group(1), match.group(2)))
			if(match.group(4) != '0'):
				result.append("%s_bottom_%s" % (match.group(1), match.group(4)))
			if(match.group(3) != '0'):
				result.append("%s_right_%s" % (match.group(1), match.group(3)))
				result.append("%s_left_%s" % (match.group(1), match.group(3)))
	elif(re.search(regex_codes.spacing_two, rule)):
		for match in re.finditer(regex_codes.spacing_four, rule):
			if(match.group(2) != '0'):
				result.append("%s_top_%s" % (match.group(1), match.group(2)))
				result.append("%s_bottom_%s" % (match.group(1), match.group(2)))
			if(match.group(3) != '0'):
				result.append("%s_right_%s" % (match.group(1), match.group(3)))
				result.append("%s_left_%s" % (match.group(1), match.group(3)))
	elif(re.search(regex_codes.spacing_one, rule)):
		for match in re.finditer(regex_codes.spacing_four, rule):
			if(match.group(2) != '0'):
				result.append("%s_top_%s" % (match.group(1), match.group(2)))
				result.append("%s_bottom_%s" % (match.group(1), match.group(2)))
				result.append("%s_right_%s" % (match.group(1), match.group(2)))
				result.append("%s_left_%s" % (match.group(1), match.group(2)))
	return result

def get_change_rules(name, prefix, read, logger):
	new_rules = list()
	result = list()
	for match in re.finditer(r"%s%s.*?{[ \t\r\n]*(.*?)[ \t\r\n]*}" % (prefix, name), read, flags=re.DOTALL):
		result = list(set(result) | set(get_classes_from_rule(match.group(1), logger)))
	return result
	
acceptable_rules = {
	'address', 
	'big', 
	'block', 
	'bold', 
	'byline', 
	'center', 
	'container', 
	'dropcap', 
	'em', 
	'first', 
	'firstletter', 
	'inline', 
	'italic', 
	'italics', 
	'justify', 
	'kill', 
	'large', 
	'left', 
	'level-2', 
	'level-3', 
	'line', 
	'line-block', 
	'message', 
	'meta', 
	'monospace', 
	'noindent', 
	'page_break_after', 
	'page_break_after_left', 
	'page_break_after_right', 
	'page_break_before', 
	'page_break_before_left', 
	'page_break_before_right', 
	'pfirst', 
	'right', 
	'sansserif', 
	'section', 
	'serif', 
	'small-caps', 
	'story', 
	'storytext', 
	'storytextp', 
	'strike', 
	'transition', 
	'u', 
	'underline', 
	'userstuff', 
	'western', 
	'x-large'}


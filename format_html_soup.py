#Python modules
import re
import os
import logging
from bs4 import BeautifulSoup, Comment
from titlecase import titlecase
#files for this program
import regex_codes_html
from format_strings import filter_chars01, filter_chars02


def clean_soup(soup, styled_classes, styled_ids, change_rules, logger):
	soup = remove_comments(soup, logger)
	soup = unwrap_empty_tags(soup, logger)
	soup = remove_unneccesary_tags(soup, logger)
	soup = remove_unneccesary_attrs(soup, styled_classes, styled_ids, change_rules, logger)
	soup = remove_unneccesary_spans(soup, logger)
	soup = remove_kill_tags(soup, logger)
	return soup

def remove_comments(soup, logger):
	#Remove comments
	for comment in soup.find_all(string=lambda text:isinstance(text, Comment)):
		comment.extract()
	return soup


def unwrap_empty_tags(soup, logger):
	unwrapped = 0
	#Remove useless tags
	for tag in soup.find_all(True):
		unwrapped += empty_tag(tag, logger)
	if(unwrapped > 0):
		logger.info("\t\t\t" + "Tags unwrapped: %d" % unwrapped)
	return soup

def empty_tag(tag, logger):
	if(tag.string):
		if(re.match(regex_codes_html.just_whitespace, tag.string)):
			parent = tag.parent
			tag.unwrap()
			if(parent):
				return 1 + empty_tag(parent, logger)
			else:
				logger.warning("\t\t\t" + "ERROR PARENT NOT FOUND")
				return 1
	if(len(tag.contents) == 0):
		if not(tag.name in ('img', 'br', 'hr')):
			parent = tag.parent
			tag.unwrap()
			if(parent):
				return 1 + empty_tag(parent, logger)
			else:
				logger.warning("\t\t\t" + "ERROR PARENT NOT FOUND")
				return 1
	return 0


def remove_unneccesary_tags(soup, logger):
	#Remove useless classes and ids
	for tag in soup.find_all(['script', 'style']):
		tag.decompose()
	for tag in soup.find_all('head'):
		tag.extract()
	for tag in soup.find_all(['html', 'body', 'a']):
		tag.unwrap()
	for tag in soup.find_all(['strong', 'b']):
		wrapped = True
		for parent_tag in tag.parents:
			if not parent_tag is None:
				if(wrapped and (parent_tag.name in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'})):
					tag.unwrap()
					wrapped = False
	return soup

def remove_unneccesary_attrs(soup, styled_classes, styled_ids, change_rules, logger):
	classes_killed = 0
	classes_retained = 0
	ids_killed = 0
	ids_retained = 0
	
	for tag in soup.find_all(True):
		for attr in tag.attrs.copy():
			if attr not in ['align', 'class', 'id']:
				del tag[attr]
		if('align' in tag.attrs):
			if('align' in tag.parent.attrs):
				if(tag['align'] == tag.parent['align']):
					del tag['align']
		if('class' in tag.attrs):
			tag['class'] = list(set(tag['class']) & styled_classes)
			if('class' in tag.parent.attrs):
				tag['class'] = list(set(tag['class']) - set(tag.parent['class']))
			if(len(tag['class']) < 1):
				del tag['class']
				classes_killed += 1
			else:
				for tag_class in tag['class'].copy():
					if(tag_class in change_rules):
						tag['class'].extend(change_rules[tag_class])
						tag['class'].remove(tag_class)
					elif(re.search("bold", tag_class, flags=re.IGNORECASE)):
						tag['class'].append('bold')
						tag['class'].remove(tag_class)
					elif(re.search("italic", tag_class, flags=re.IGNORECASE)):
						tag['class'].append('italic')
						tag['class'].remove(tag_class)
				tag['class'].sort()
				classes_retained += 1
		if('id' in tag.attrs):
			tag['id'] = list(set(tag['id']) & styled_ids)
			if(len(tag['id']) < 1):
				del tag['id']
				ids_killed += 1
			else:
				for tag_id in tag['id']:
					if(tag_id in change_rules):
						tag['id'].append(change_rules[tag_id])
						tag['id'].remove(tag_id)
				tag['id'].sort()
				ids_retained += 1
	if(classes_killed > 0):
		logger.info("\t\t\t" + "Tags with all classes deleted: %d" % classes_killed)
	if(classes_retained > 0):
		logger.info("\t\t\t" + "Tags with classes retained: %d" % classes_retained)
	if(ids_killed > 0):
		logger.info("\t\t\t" + "Tags with all ids deleted: %d" % ids_killed)
	if(ids_retained > 0):
		logger.info("\t\t\t" + "Tags with ids retained: %d" % ids_retained)
	return soup

def remove_unneccesary_spans(soup, logger):
	#Remove useless span tags
	unwrapped_spans = 0
	remaining_spans = 0
	converted_spans = 0
	for span_tag in soup.find_all('span'):
		if('class' in span_tag.attrs):
			if("bold" in span_tag['class']):
				span_tag.wrap(soup.new_tag('strong'))
				span_tag['class'].remove("bold")
			if("IPA" in span_tag['class']):
				span_tag.insert_before("\\textipa{")
				span_tag.insert_after("}")
				span_tag['class'].remove("IPA")
			if("strike" in span_tag['class']):
				span_tag.wrap(soup.new_tag('strike'))
				span_tag['class'].remove("strike")
			if("u" in span_tag['class']):
				span_tag.wrap(soup.new_tag('u'))
				span_tag['class'].remove("u")
			if("italic" in span_tag['class']):
				span_tag.wrap(soup.new_tag('em'))
				span_tag['class'].remove("italic")
			if("em" in span_tag['class']):
				span_tag.wrap(soup.new_tag('em'))
				span_tag['class'].remove("em")
			if("underline" in span_tag['class']):
				span_tag.wrap(soup.new_tag('u'))
				span_tag['class'].remove("underline")
			if(len(span_tag['class']) == 0):
				del span_tag['class']
		if('id' in span_tag.attrs):
			remaining_spans += 1
		if('lang' in span_tag.attrs):
			del span_tag['lang']
		if(len(span_tag.attrs) > 0):
			logger.debug("\t\t\t" + "Span remaining: " + str(span_tag.attrs))
			remaining_spans += 1
		else:
			span_tag.unwrap()
			unwrapped_spans += 1
	if(unwrapped_spans > 0):
		logger.info("\t\t\t" + "Unwrapped Spans: %d" % unwrapped_spans)		
	if(remaining_spans > 0):
		logger.info("\t\t\t" + "Remaining Spans: %d" % remaining_spans)		
	if(converted_spans > 0):
		logger.info("\t\t\t" + "Converted Spans: %d" % converted_spans)		
	return soup

def remove_kill_tags(soup, logger):
	for tag in soup.find_all(True):
		if('class' in tag.attrs):
			if('kill' in tag['class']):
				tag.extract()
	return soup


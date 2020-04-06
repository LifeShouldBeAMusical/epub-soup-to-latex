#Python modules
import re
import os
import logging
from bs4 import BeautifulSoup, Comment
from titlecase import titlecase
#files for this program
import regex_codes_html
from format_strings import filter_chars01, filter_chars02
from format_html_soup import clean_soup
from format_html_commands import swap_tags_commands
from format_html_read import format_html_read


inline_tag_set = {'em', 'i', 'strong', 'b', 'strike', 's', 'sub', 'sup', 'u', 'cite', 'span'}


def format_html(read, multichapter, relpath, styled_classes, styled_ids, change_rules, logger):
	read = filter_chars01(read, logger)
	
	soup = BeautifulSoup(read, 'lxml')
	
	soup = clean_soup(soup, styled_classes, styled_ids, change_rules, logger)
	
	soup = swap_tags_commands(soup, multichapter, relpath, logger)
	
	read = str(soup)

	read = format_html_read(read, multichapter, logger)
	
	return read


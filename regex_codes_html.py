import re

chapter_br = re.compile(r"\\(part\*?|chapter\*?|section\*?){[ \t\r\n]*\\\\(.*?)}")
chapter_br_br = re.compile(r"\\(part\*?|chapter\*?|section\*){(.*?)\\\\[ \t]*\\\\(.*?)}")
chapter_whitespace_one = re.compile(r"\\(part|chapter\*?|section\*){[ \t\r\n\-]+(.*?)}\n")
chapter_whitespace_two = re.compile(r"\\(part|chapter\*?|section\*){(.*?)[ \t\r\n\-]+}\n")
chapter_bold = re.compile(r"\\(part|chapter\*?|section\*){(.*)\\textbf{([^{}]*)}(.*)}")
chapter_image = re.compile(r"\\(part|chapter|section*){(\\includegraphics{[^{}]+})}")
chapter_noindent = re.compile(r"\\(part|chapter\*?|section\*){(.*?)}[ \t\r\n]+\\noindent")

p_br = re.compile(r"\n{2,}[ \t\r\n]*?\\\\")
br_p = re.compile(r"\\\\[ \t\r\n]*?\n{2,}")
br_br = re.compile(r"\\\\[ \t\r\n]*\\\\")
br_hr = re.compile(r"\\\\[ \t\r\n]*\\centereddots")
hr_br = re.compile(r"\\centereddots[ \t\r\n]*\\\\")
hr_hr = re.compile(r"\\centereddots[ \t\r\n]*\\centereddots")
br_tag = re.compile(r"([ \t\r\n]*\\\\[ \t\r\n]*)(})")
hr_tag = re.compile(r"([ \t\r\n]*\\centereddots[ \t\r\n]*)(})")
tag_br = re.compile(r"(\\[a-z0-9@]+{)([ \t\r\n]*\\\\[ \t\r\n]*)")
tag_hr = re.compile(r"(\\[a-z0-9@]+{)([ \t\r\n]*\\centereddots[ \t\r\n]*)")
br_env = re.compile(r"([ \t\r\n]*\\\\[ \t\r\n]*)(\\end{[a-z]+})")
hr_env = re.compile(r"([ \t\r\n]*\\centereddots[ \t\r\n]*)(\\end{[a-z]+})")
env_br = re.compile(r"(\\begin{[a-z]+})([ \t\r\n]*\\\\[ \t\r\n]*)")
env_hr = re.compile(r"(\\begin{[a-z]+})([ \t\r\n]*\\centereddots[ \t\r\n]*)")
any_tag = re.compile(r"</?[a-z0-9]+\b[^>]*>", flags=re.IGNORECASE)
margin = re.compile("margin_left_(\d[0-9.]*[a-z%]+)")
text_indent = re.compile("indent_\-(\d[0-9.]*[a-z%]+)")
include_graphics_underscore = re.compile(r"\\includegraphics{([^{}]*)\\_([^{}]*)}")
div_hr_div = re.compile(r"\\begin{([^{}]*)}([ \t\r\n]*\\centereddots[ \t\r\n]*)\\end{\1}")
div_br_div = re.compile(r"\\begin{([^{}]*)}([ \t\r\n]*\\\\[ \t\r\n]*)\\end{\1}")
just_whitespace = re.compile(r"^[ \t\r\n]*$")
itshape_break_itshape = re.compile(r"[\r\n]+\} \|\|itshape\|\|([\r\n]+)\{\\itshape[\r\n]+")
bars_itshape_bars = re.compile(r"\|\|itshape\|\|")
bold_break = re.compile(r"\\textbf{([^}]*?)(\n{2,})")
it_break = re.compile(r"\\textit{([^}]*?)(\n{2,})")
spacing = re.compile("(margin|padding)_(left|right|top|bottom)_(\-?\d[0-9.]*)([a-z\%]*)")
xml_tag = re.compile(r"<\?xml[^>]*?\?>")
doctype_tag = re.compile(r"<!DOCTYPE\b[^>]*>")
space_line = re.compile(r"[ \t\r]+\n")
pipes_itshape_pips = re.compile(r"\|\|itshape\|\|")
empty_it = re.compile(r"\\textit{([ \t\r\n]*)}")
empty_bf = re.compile(r"\\textbf{([ \t\r\n]*)}")
part_part = re.compile(r"\\part{Part \d+[ ~\-]*")
part_chapter = re.compile(r"\\part{(Chapter[^{}]+?)}", flags=re.IGNORECASE)
section_chapter = re.compile(r"\\section\*{(Chapter[^{}]+?)}", flags=re.IGNORECASE)
chapter_number = re.compile(r"\\(part|chapter\*?|section\*){\d+[.:]?[ ]+(.+)}")

chapter_number_th = re.compile(r"\\chapter{Chapter \d+(th|rd|nd|st|[a-z])[ ~\-:]*[ ]+", flags=re.IGNORECASE)
chapter_number_super_th = re.compile(r"\\chapter{Chapter \d+[ ]*\\textsuperscript{(th|rd|nd|st)}[ ~\-:]*[ ]+", flags=re.IGNORECASE)
chapter_whitespace_plus = re.compile(r"\\chapter{[ ~\-:.]+[ ]+")
chapter_unnumbered = re.compile(r"\\chapter{((Prologue|Epilogue|Interlude|Outtake|Bonus|Intermission).*)}", flags=re.IGNORECASE)
start_br = re.compile(r"(\A)[ \t\r\n]*\\\\")
start_hr = re.compile(r"(\A)[ \t\r\n]*\\centereddots")
start_whitespace = re.compile(r"(\A)\n+")
br_end = re.compile(r"\\\\([ \t\r\n]*\Z)")
hr_end = re.compile(r"\\centereddots([ \t\r\n]*\Z)")
whitespace_end = re.compile(r"[ \t\r\n]+(\n\Z)")
too_many_newlines = re.compile(r"\n{3,}")
chapter_whitespace_one = re.compile(r"\\(part|chapter\*?|section\*){[ \t\r\n\-]+(.*?)}\n")
chapter_whitespace_two = re.compile(r"\\(part|chapter\*?|section\*){(.*?)[ \t\r\n\-]+}\n")
chapter_interlude = re.compile(r"\\chapter{(.*Interlude.*)}\n", flags=re.IGNORECASE)
chapter_number_end = re.compile(r"\\(part|chapter\*?|section\*){\d{1,3}}")
chapter_chapter_number = re.compile(r"\\chapter{Chapter \d+[ ~\-:.]*[ ]*", flags=re.IGNORECASE)
chapter_chapter_number = re.compile(r"\\chapter{Chapter \d+}", flags=re.IGNORECASE)
empty_environment = re.compile(r"\\begin{([^{}]+?)}([ \t\r\n]*)\\end{\1}")


font_size = re.compile("font_size_(\d+)\\%")
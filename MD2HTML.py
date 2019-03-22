"""
!!!IMPORTANT!!!
Please read all the information in the readme.md file before trying read the code below.
(I haven't wrote it yet, I'll write it tomorrow its very late and I want some sleep.)
update 2019/3/21 00:30 or something i forgot
im so fucking lazy
tomorrow it is then 
update 2019/3/21 afternoon
ill write the docs when im finished
"""
from io import StringIO, TextIOWrapper
from functools import reduce
import re, time

def count_time(func):
    def re_func(*args):
        start = time.time()
        re = func(*args)
        print("Rendered in %s ms" %((time.time() - start) * 1000))
        return re
    return re_func

# --- Constants ---
pattern_line_break = re.compile(r"(\s|\t)*\n")

# --- Text emphasis renderers ---

def links(match: re.Match) -> str:
    """
        Renders a hyperlink tag formatted in HTML
        Input values:   - Match object of the matched md tag
        Output values:  - Rendered text
    """
    text, url = match.groups()
    url = url.split(" ", 1)
    #print(url, match.groups())
    return "<a%s%s>%s</a>" %(" href=%s" %(url[0]), " title=%s" %(url[1]) if len(url) >=2 else "", text)

def images(match: re.Match) -> str:
    text, url = match.groups()
    url = url.split(" ", 1)
    #print(url, match.groups())
    return r"<img src=%s%s%s>" %("\"" + url[0] + "\"", " alt=%s" %("\"" + text + "\""), " title=%s" %(url[1]) if len(url) >= 2 else "")

emphasis_tags = {   
    re.compile(r"\!\[(.*?)\]\s?\((.+?)\)"): images,                                                            # Images
    re.compile(r"\[(.+)\]\s?\((.+?)\)"): links,                                                               # Hyper links
    re.compile(r"(?!<img\ssrc=\".*)[*_]{2}(.+)[*_]{2}(?!.*\">)"): lambda x: "<b>%s</b>" %(x.group(1)),     # Bold
    re.compile(r"(?!<img\ssrc=\".*)[*_](.+)[*_](?!.*\">)"): lambda x: "<i>%s</i>" %(x.group(1)),           # Italics
    re.compile(r"(?!<img\ssrc=\".*)~{2}(.+)~{2}(?!.*\">)"): lambda x: "<s>%s</s>" %(x.group(1)),           # Strike through
    re.compile(r"(?!<img\ssrc=\".*)`(.+?)`(?!.*\">)"): lambda x: "<code>%s</code>" %(x.group(1)),          # Code highlight
    re.compile(r"(?!<code>)#(.*)#(?!</code>)"): ""
}

def putEmphasis(line: str) -> str:
    """
        Replace all markdown emphasis tags with html tags.
        Input values:   - Text with md emphasis tags in it
        Output values:  - Rendered text
    """
    for i in emphasis_tags:
        line = re.sub(i, emphasis_tags[i], line)
    return line

# --- Block element renderers ---

def headers(line: str, file: TextIOWrapper, line_count: int) -> tuple:
    """
        Renders a html formatted header tag.
        Input values:   - Standard m2h function inputs
        Output values:  - Standard m2h function outputs
    """
    match = re.match(r"(#{1,6})\s(.*(?:~|_|\*|\b))(?:\s+#+)?\n?", line)
    length = len(match.group(1))
    print(match.group(2))
    return ("<h%s>%s</h%s>\n" %(length, putEmphasis(match.group(2)), length), line_count + 1)

def paragraph(line: str, file: TextIOWrapper, line_count: int) -> tuple:
    """
        Returns a html formatted paragraph tag.
        Input values:   - Standard m2h function inputs
        Output values:  - Standard m2h function outputs
    """
    pattern = re.compile(".+")
    text = line[:-1] if line[-1:] == "\n" else line
    
    while True:
        linebreak = text[-2:] == "  "
        pos = file.tell()
        line_count += 1
        line = file.readline()
        line = line[:-1] if line[-1:] == "\n" else line
        if line == "": break
        matched = False
        for i in md_tags:
            if i == pattern: continue
            if re.match(i, line):
                line_count -= 1
                file.seek(pos)
                matched = True
                break
        if matched: break
        text = (text[:-2] if linebreak else text) +  ("</br>" if linebreak else " ") + line
    return ("<p>%s</p>\n" %(putEmphasis(text[:-2] if text[-2:] == "  " else text)), line_count + 1)

# When I wrote this code, only I and God knew what I was writing. (ofc if he actually exists)
# Now I bet even God doesn't have a single clue how the fuck this code works.
def renderListItem(text_: str, text_par: bool, child_par: bool, tab_length: int) -> str:
    """
        Renders all the content in a list item
        (Including text and other lists)
        Returns rendered html formatted text
        Comments are left for future debugging purposes
        Input values:   - text_: The text needed to be rendered
                        - text_par: Whether or not the text in this item needs to be put in a <p> tag
                        - child_par: Whether or not the text in the children of this item needs to be put in a <p> tag
                        - tab_length: The tab length of this item
        Output values:  - Rendered text
    """
    pattern_item = r"(\s{%s,%s}|\t{%s})(\+|-|\*|\d+\.)\s(.*\n?)" %(tab_length * 4, tab_length * 4 + 3, tab_length)
    pattern_item_child = r"(\s{%s,%s}|\t{%s})(\+|-|\*|\d+\.)\s(.*)\n?" %(tab_length * 4 + 4, tab_length * 4 + 7, tab_length + 1)
    list_type = ""
    result = ""
    #print("-----\n%s\n-----" %(text_), child_par)
    f = StringIO(text_)
    while True:
        line = f.readline()
        if line == "": break
        match = re.match(pattern_item, line)
        if match:
            #print("******\n%s\n******" %(line))
            list_type_ = "ul" if re.match(r"\+|-|\*", match.group(2)) else "ol"
            if list_type_ != list_type:
                if list_type:
                    result += (" " * 4 * tab_length) + "</%s>\n" %(list_type)
                result += (" " * 4 * tab_length) + "<%s>\n" %(list_type_)
                list_type = list_type_
            item = match.group(3)
            child_par_ = False
            while True:
                pos = f.tell()
                line = f.readline()
                if line == "": break
                if re.match(pattern_item, line):
                    f.seek(pos)
                    break
                if re.match(pattern_line_break, line):
                    pos_ = f.tell()
                    line_ = f.readline()
                    if re.match(pattern_item_child, line_):
                        child_par_ = True
                    f.seek(pos_)
                    del pos_
                item += line
            #print("---------\n%s\n---------%s" %(item, tab_length + 1))
            result += (" " * 4 * (tab_length + 1)) + "<li>\n" + (" " * 4 * (tab_length + 2)) + renderListItem(item, child_par, child_par_, tab_length + 1) +  (" " * 4 * (tab_length + 1)) + "</li>\n"
        else:
            text = line[:-1] if line[-1] == "\n" else line
            while True:
                pos = f.tell()
                line = f.readline()
                if line == "": break
                line = line[:-1] if line[-1] == "\n" else line
                if re.match(pattern_item, line):
                    f.seek(pos)
                    break
                text += "</br>" + line if text[-2:] == "  " else " " + line
            #print(text)
            result += text + "\n" if not text_par else "<p>%s</p>\n" %(text)
    if list_type: result += (" " * 4 * tab_length) + "</%s>\n" %(list_type)
    return result

def lists(line: str, file: TextIOWrapper, line_count: int) -> tuple:
    """
        Reads a single list from the file and renders it into html by calling
        the function renderListItem()
        Input values:   - Standard m2h function inputs
        Return values:  - Standard m2h function outputs
    """
    tags_in_lists = [pattern_line_break, re.compile(r"(\+|-|\*|\d+\.)\s(.*)\n?"), re.compile(r".+"), re.compile(r"(\t|\s{4})(.*\n?)")]
    pattern_item = re.compile(r"(\+|-|\*|\d+\.)\s(.*)\n?")
    type_ = r"(\+|-|\*)" if re.match(r"(\+|-|\*)", re.match(pattern_item, line).group(1)) else r"(\d+\.)"
    pattern_current_item = re.compile(r"%s\s(.*)\n?" %(type_))
    full_list = line
    child_par = False
    while True:
        pos = file.tell()
        line = file.readline()
        if line == "": break
        line_count += 1
        if line == "\n":
            list_end = False
            while True:
                pos_ = file.tell()
                line = file.readline()
                if line == "": break
                line_count += 1
                if line != "\n" and not re.match(pattern_current_item, line):
                    list_end = True
                    file.seek(pos_)
                    line_count -= 1
                    del pos_
                    break
                else:
                    child_par = True
                    break
            if list_end: break
        if reduce(lambda x,y: x | y, [1 if i not in tags_in_lists and re.match(i, line) else 0 for i in md_tags]) or (re.match(pattern_item, line) and not re.match(pattern_current_item, line)): 
            file.seek(pos)
            line_count -= 1
            break
        full_list += line
    #print("----\n%s\n----" %(full_list))
    return (putEmphasis(renderListItem(full_list, False, child_par, 0)), line_count + 1)

def code_reverse_quote(line: str, file: TextIOWrapper, line_count: int) -> tuple:
    """
        Renders code blocks started with three reverse quotation marks.
        Input values:   - Standard m2h function inputs
        Output values:  - Standard m2h function outputs
    """
    result = "<pre><code>\n"
    while True:
        line = file.readline()
        line_count += 1
        if line == "" or re.match(r"```\n?", line): break
        result += line
    result += "</code></pre>\n"
    return (result, line_count + 1)

def code_tab(line: str, file: TextIOWrapper, line_count: int) -> tuple:
    """
        Renders code blocks started with tab or four spaces.
        Input values:   - Standard m2h function inputs
        Output values:  - Standard m2h function outputs
    """
    pattern_code = re.compile(r"(\t|\s{4})(.*\n?)")
    result = "<pre><code>\n"
    result += re.match(pattern_code, line).group(2)
    while True:
        pos = file.tell()
        line = file.readline()
        line_count += 1
        if line =="": break
        match = re.match(pattern_code, line)
        if not match:
            file.seek(pos)
            line_count -= 1
            break
        result += match.group(2)
    result += "</code></pre>\n"
    return (result, line_count + 1)

def block_quote(line: str, file: TextIOWrapper, line_count: int) -> tuple:
    pattern_block_quote = re.compile(r">?\s?(.*\n?)")
    result = ""
    result += re.match(pattern_block_quote, line).group(1)
    block_quote_md_tags = [re.compile(r">\s?.*"), re.compile(r".+")]
    while True:
        pos = file.tell()
        line = file.readline()
        line_count += 1
        if line == "": break
        if reduce(lambda x,y: x | y, [1 if re.match(i, line) and i not in block_quote_md_tags else 0 for i in md_tags]):
            file.seek(pos)
            line_count -= 1
            break
        result += re.match(pattern_block_quote, line).group(1)
    TempIO = StringIO(result)
    result = render(TempIO)
    del TempIO
    result = "<blockquote>\n" + result + "</blockquote>\n"
    return (result, line_count + 1)

def table(line: str, file: TextIOWrapper, line_count: int) -> tuple:
    pattern_row = re.compile(r"\|?((?:\s*.+\s*\|)+)(\s*[^\|\n]+\s*)\|?")
    result = "<table style=\"border:1px solid black;min-width: 500px\">\n"
    head = "".join(re.match(pattern_row, line).groups()).split("|")
    length = len(head)
    first_line = line
    pos = file.tell()
    line = file.readline()
    line_count += 1
    if line == "" or not re.match(r"\|((?::*-{3,}:*\|){%s})(\s*:*-{3,}:*\s*)\|" %(length-1), line):
        file.seek(pos)
        return ("<p>%s</p>\n" %(first_line if first_line[-1] != "\n" else line[-1:]), line_count)
    del first_line
    align = "".join(re.match(r"\|((?::*-{3,}:*\|){%s})(\s*:*-{3,}:*\s*)\|" %(length-1), line).groups()).split("|")
    for index, i in enumerate(align):
        if re.match(r"\s*:-+:\s*", i):
            align[index] = " style=\"text-align:center;border:1px solid black;width:33%;\""
        elif re.match(r"\s*:-+\s*", i):
            align[index] = " style=\"text-align:left;border:1px solid black;width:33%;\""
        elif re.match(r"\s*-+:\s*", i):
            align[index] = " style=\"text-align:right;border:1px solid black;width:33%;\""
        else:
            align[index] = ""
    result += "<tbody>\n" + " " * 4 + "<tr>\n"
    result += "\n".join([" " * 8 + "<th%s>%s</th>" %(align[index], i) for index, i in enumerate(head)])
    result += "\n" + " " * 4 + "</tr>\n"
    pattern_row = re.compile(r"\|?((?:\s*.+?\s*\|){%s})(\s*[^\|\n]+\s*)\|?" %(length - 1))
    while True:
        pos = file.tell()
        line = file.readline()
        line_count += 1
        match = re.match(pattern_row, line) 
        if line == "" or not match:
            line_count -= 1
            file.seek(pos)
            break
        items = "".join(match.groups()).split("|")
        result += " " * 4 + "<tr>\n"
        result += "\n".join([" " * 8 + "<td%s>%s</td>" %(align[index], i) for index, i in enumerate(items)])
        result += "\n" +  " " * 4 + "</tr>\n"
    result += "</tbody>\n</table>\n"
    return (putEmphasis(result), line_count)

md_tags = {
    re.compile(r"(#{1,6})\s(.*(?:~|_|\*|\b))(?:\s+#+)?\n?"): headers,               # Headers
    pattern_line_break: lambda line,file,line_count: ("</br>\n", line_count + 1),  # Line breaks
    re.compile(r"(\+|-|\*|\d+\.)\s(.*)\n?"): lists,                                # Lists
    re.compile(r"```\n?"): code_reverse_quote,                                     # Code blocks with reversed quotation marks
    re.compile(r"(\t|\s{4})(.*\n?)"): code_tab,                                    # Code blocks with tabs
    re.compile(r">\s?.*"): block_quote,
    re.compile(r"\|?(\s*.*\s*\|)+(\s*.+\s*)\|?"): table,
    re.compile(r".+"): paragraph,                                                  # Paragraphs
}

# --- Rendering ---

@count_time
def render(file: TextIOWrapper, line_count_display: bool = False, return_file: bool = False) -> TextIOWrapper:
    """
        Takes in a file and returns the rendered HTML formatted file.
        Input values:   - The file needed to be rendered
                        - Return a TextIO file type or a string type.
                        (Will create a html file if set to true)
                        - Display the count of the line being rendered
        Output values:  - Rendered file
    """
    line_count = 1
    result = ""
    while True:
        line = file.readline()
        if line == "": break
        for i in md_tags:
            if re.match(i, line):
                if line_count_display: result += str(line_count)
                output = md_tags[i](line, file, line_count)
                result += output[0]
                line_count = output[1]
                break
    if return_file:
        f = open("%s.html" %(re.match(r"(.+)\.md", file.name).group(1)), "w")
        f.write(result)
        return f
    else:
        return result

# --- Testing ---

file = open("readme.md")
f = render(file, False, True)
file.close()
f.close()
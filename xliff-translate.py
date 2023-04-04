import os

from translateChatGPT import TranslatorChatGPT
from translateWrapper import TranslatorWrapper

FOLDER_PATH = "xliff-files"
FOLDER_PATH_RESULT = "xliff-results"

# parameters for Google translator
# LANGUAGE_SOURCE = "en"
# LANGUAGE_TARGET = "zh-CN"

# parameters for chatGPT translator
LANGUAGE_SOURCE = "english"
LANGUAGE_TARGET = "chinese"


class Element:
    text: str = ""
    is_tag: bool = False

    def __init__(self, text: str, is_tag: bool):
        self.text = text
        self.is_tag = is_tag

    def __str__(self):
        # return f"<Element is_tag={self.is_tag} text='{self.text}'>"
        return f"({self.is_tag},'{self.text}')"


def build_elements(elements: [Element], text: str, line: str, line_nr: int):
    """Build list of elements. text is either """

    # check: text starts with tag
    if text.startswith("<"):
        # remove this element
        try:
            tag_end_index = text.index(">")  # should always find - if not error
        except ValueError:
            raise ValueError(f"Un-closed tag '<...' found in line nr {line_nr} (first line has line nr 1)\r\nTag with "
                             f"problem: {text}\r\nWhole line: {line}")

        # if tag is not closed, find closing tag
        if not text[tag_end_index - 1] == '/':
            # find tag name e.g. "<source ...>" -> "source" or "<source>" -> "source"
            try:
                tag_space_index = text.index(" ")
            except ValueError:
                tag_space_index = tag_end_index

            # space index is after closing of the tag
            if tag_space_index > tag_end_index:
                tag_space_index = tag_end_index

            tag_name = text[1:tag_space_index]

            # find closing tag </...>
            try:
                tag_close_index = text.index("</" + tag_name)  # should always find - if not error
            except ValueError:
                raise ValueError(
                    f"Un-closed tag '<{tag_name}>...' (no </{tag_name}>) found in line nr {line_nr} (first line has line nr 1)\r\nTag with problem: {text}\r\nWhole line: {line}")

            # find index where closing tag closes
            text_rest = text[tag_close_index:]
            try:
                close_end_index = tag_close_index + text_rest.index(">")  # should always find - if not error
            except ValueError:
                raise ValueError(
                    f"Un-closed tag '</{tag_name}' found in line nr {line_nr} (first line has line nr 1)\r\nTag with problem: {text}\r\nWhole line: {line}")

            # tag text, text inside the tag, closing tag text, text after the tag
            text_tag = text[:tag_end_index + 1]
            text_inside = text[tag_end_index + 1:tag_close_index]
            text_tag_close = text[tag_close_index:close_end_index + 1]
            text_after = text[close_end_index + 1:]

            # add opening tag
            elements.append(Element(text_tag, True))

            # recursion on inside elements
            if not text_inside == '':
                build_elements(elements, text_inside, line, line_nr)

            # after inside elements add closing tag
            elements.append(Element(text_tag_close, True))

            # do rest of the operations with rest of text
            text = text_after
        else:
            # tag is closed, just remove tag
            text_tag = text[:tag_end_index + 1]
            text_after = text[tag_end_index + 1:]

            # add opening tag
            elements.append(Element(text_tag, True))

            # do rest of the operations with rest of text
            text = text_after

    # does not begin with '<': find first tag
    try:
        first_tag_index = text.index("<")
    except ValueError:  # not found - rest is just text
        if not text == '':
            elements.append(Element(text, False))
        return

    # find text until tag
    text_until_tag = text[:first_tag_index]
    text_rest = text[first_tag_index:]

    # parse rest of text
    if not text_until_tag == '':
        elements.append(Element(text_until_tag, False))

    if not text_rest == '':
        build_elements(elements, text_rest, line, line_nr)

    # finished


def translate_file(translator: TranslatorWrapper, filename: str):
    """Translate .xlf file from source language to target language (Add <target> tags)"""

    # load file
    filename_full = os.path.join(FOLDER_PATH, filename)
    file = open(filename_full, 'r')

    # get new filename: remove .xlf and add .es.xlf where .es is the target language
    filename_new = os.path.join(FOLDER_PATH_RESULT, os.path.splitext(filename)[0] + "." + LANGUAGE_TARGET + ".xlf")
    file_result = open(filename_new, 'w')

    print(f"Translating file: {filename_full} -> {filename_new}")

    # translate sources, ignore target
    line_nr = 0
    while True:
        # read one line from file
        line: str = file.readline()
        if not line:
            break
        line_nr += 1

        # separate white space (indentation)
        try:
            first_tag_index = line.index("<")
        except ValueError:  # not found
            file_result.writelines(line)
            continue

        whitespace = line[0:first_tag_index]
        tag = line[first_tag_index:]

        # ignore <target> tags
        if tag.startswith("<target"):
            continue

        # write this line to file
        file_result.writelines(line)
        tag = tag[:-1]
        line = line[:-1]

        # save not <source> tags
        if not tag.startswith("<source"):
            continue

        # remove <source> and </source>
        tag = tag[8:-9]

        # get a list of all texts + elements
        element_list: [Element] = []
        build_elements(element_list, tag, line, line_nr)
        print(f"Reading line nr {line_nr}: {line}")
        print([str(el) for el in element_list])

        # build list of only texts (without elements)
        text_list: [str] = [el.text for el in element_list if not el.is_tag]

        # translate texts
        text_list_translated = translator.translate_multiple(text_list)

        # replace only texts
        for i in range(len(element_list)):
            el = element_list[i]
            if el.is_tag:
                continue
            el.text = text_list_translated.pop(0)

        # build <target> with replaced text
        result = whitespace + "<target>" + "".join([el.text for el in element_list]) + "</target>\n"

        # write <target> to file
        file_result.writelines(result)


def main():
    if not os.path.exists(FOLDER_PATH_RESULT):
        os.mkdir(FOLDER_PATH_RESULT)
    if not os.path.exists(FOLDER_PATH):
        raise Exception(f"Folder '{FOLDER_PATH}' does not exist. Please put your .xlf files into this folder for "
                        f"translating.")

    # create the translator you want here
    # translator = TranslatorGoogle()
    # translator.init(LANGUAGE_SOURCE, LANGUAGE_TARGET)

    translator = TranslatorChatGPT()
    translator.init(LANGUAGE_SOURCE, LANGUAGE_TARGET)

    # go through files and translate
    for filename in os.listdir(FOLDER_PATH):
        translate_file(translator, filename)

    return


if __name__ == "__main__":
    main()

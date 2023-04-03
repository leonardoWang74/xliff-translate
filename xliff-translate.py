import os
from googletrans import Translator
from translate.storage.xliff import xlifffile

FOLDER_PATH = "xliff-files"
FOLDER_PATH_RESULT = "xliff-results"
LANGUAGE_SOURCE = "en"
LANGUAGE_TARGET = "zh-CN"
TRANSLATOR_SOURCE = "en"
TRANSLATOR_TARGET = "zh-CN"


class TranslatorWrapper:
    def __int__(self):
        self.translator = Translator()

    def translate(self, text: str):
        res = self.translator.translate(text, src=TRANSLATOR_SOURCE, dest=TRANSLATOR_TARGET)
        return res.text


def translate_file(translator: TranslatorWrapper, filename: str):
    """Translate .xlf file from source language to target language (Add <target> tags)"""

    # load file
    filename_full = os.path.join(FOLDER_PATH, filename)
    print(f"Translating file: {filename_full}")
    file = open(filename_full, 'rb')
    content = file.read()

    xliff_file = xlifffile(inputfile=content, sourcelanguage=LANGUAGE_SOURCE, targetlanguage=LANGUAGE_TARGET)

    # translate units
    for number, unit in enumerate(xliff_file.getunits()):
        src_text = unit.source
        if src_text is None:
            continue

        target_text = translator.translate(src_text)

        print(f"Translation: {src_text} -> {target_text}")

        unit.settarget(target_text, lang=LANGUAGE_TARGET)

    # get new filename: remove .xlf and add .es.xlf where .es is the target language
    filename_new = os.path.splitext(filename)[0] + "." + LANGUAGE_TARGET + ".xlf"

    # save new file
    xliff_file.savefile(os.path.join(FOLDER_PATH_RESULT, filename_new))


def main():
    if not os.path.exists(FOLDER_PATH_RESULT):
        os.mkdir(FOLDER_PATH_RESULT)
    if not os.path.exists(FOLDER_PATH):
        raise Exception(f"Folder '{FOLDER_PATH}' does not exist. Please put your .xlf files into this folder for "
                        f"translating.")

    translator = TranslatorWrapper()

    # go through files and translate
    for filename in os.listdir(FOLDER_PATH):
        translate_file(translator, filename)

    return


if __name__ == "__main__":
    main()

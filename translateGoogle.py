from translateWrapper import TranslatorWrapper
from googletrans import Translator


# languages: should be the shorthand of the language
# e.g. 'en' for english, 'de' for german with 'en-US' also being possible

# uses https://pypi.org/project/googletrans/
class TranslatorGoogle(TranslatorWrapper):
    translator = None
    src = None
    dest = None

    def init(self, src, dest):
        self.translator = Translator()
        self.src = src
        self.dest = dest

    def translate(self, text: str):
        res = self.translator.translate(text, src=self.src, dest=self.dest)
        return res.text

    def translate_multiple(self, texts: [str]):
        res = self.translator.translate(texts, src=self.src, dest=self.dest)
        return [tr.text for tr in res]
        # return [self.translator.translate(t, src=self.src, dest=self.dest).text for t in texts]

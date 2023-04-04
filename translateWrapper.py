from abc import abstractmethod


class TranslatorWrapper:
    @abstractmethod
    def translate(self, text: str) -> str:
        pass

    @abstractmethod
    def translate_multiple(self, texts: [str]) -> [str]:
        pass

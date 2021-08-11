from googletrans import Translator

class TranslatorWrap:
    def __init__(self):
        self.translator = Translator(service_urls=[
            'translate.google.cn',
        ])

    def en2zh(self, text):
        try:
            return self.translator.translate(text, dest='zh-CN').text
        except Exception:
            return text
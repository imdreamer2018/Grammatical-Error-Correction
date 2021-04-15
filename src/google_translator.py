from googletrans import Translator

translator = Translator(service_urls=[
      'translate.google.cn'
    ])


def language_detect(msg):
    language = translator.detect(msg)
    return language.lang


def google_translator(msg):
    if language_detect(msg) == 'en':
        return translator.translate(msg, dest='zh-CN').text
    else:
        return translator.translate(msg, dest='en').text



import string

from googletrans import Translator


def translate_to_polish(name: string):
    return Translator().translate(name, dest='pl').text

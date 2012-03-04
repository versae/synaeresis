# -*- coding: utf-8 -*-
import fuzzy

from studies.utils.metaphone import dm
from studies.utils.phonetic_algorithm_es import PhoneticAlgorithmsES
from studies.utils.transcriptors import phonetic_transcript


def metaphone(text, language="en"):
    if language not in ("en", "es"):
        language = "en"
    if language == "es":
        alg = PhoneticAlgorithmsES()
        return alg.metaphone(text)
    else:
        return dm(text)[0]


def soundex(text, language="en"):
    soundex = fuzzy.Soundex(10)
    return soundex(text)


def transcript(text, language="en", alphabet="ipa"):
    return phonetic_transcript(text)

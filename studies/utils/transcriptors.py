# -*- coding: utf-8 -*-
import codecs
import os
import tempfile
import subprocess

from django.conf import settings


def phonetic_transcript(text, language="en", alphabet="ipa"):
    perkins = getattr(settings, "PERKINS_BIN", "")
    if not os.path.isfile(perkins):
        raise OSError("Perkins binary not found. Please, try to download it "
                      "from http://ssadowsky.hostei.com/perkins-es.html and "
                      "set the PERKINS_BIN setting to its path.")
    language = language[:2]
    if language not in ("en", "es"):
        language = "en"
    if alphabet not in ("rfe", "ipa", "afi"):
        language = "afi"
    try:
        i_name = tempfile.mktemp()
        i = codecs.open(i_name, "w", "latin-1")
        o = tempfile.NamedTemporaryFile(delete=False)
        i.write(text)
        i.close()
        command = [perkins,  "-i", i.name, "-o", o.name, "-l", language, "-sm"]
        if language == "rfe":
            command += ["-at"]
        else:
            command += ["-multi", "--pausas-afi"]
        out = subprocess.check_output(command)
        result = o.read().strip().strip("\n")
        o.close()
    finally:
        os.unlink(i.name)
        os.unlink(o.name)
    return result.decode("utf8")

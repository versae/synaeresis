#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Taken from https://github.com/amsqr/Spanish-Metaphone
'''
    Modified by Javier de la Rosa, <versae@gmail.com> in order to
    make it pass unicode string, PEP08 and PyFlakes. March, 2012.

    The Spanish Metaphone Algorithm (Algoritmo del Metáfono para el Español)

    This script implements the Metaphone algorithm (c) 1990 by Lawrence Philips.
    It was inspired by the English double metaphone algorithm implementation by
    Andrew Collins - January 12, 2007 who claims no rights to this work
    (http://www.atomodo.com/code/double-metaphone)


    The metaphone port adapted to the Spanish Language is authored
    by Alejandro Mosquera <amosquera@dlsi.ua.es> November, 2011
    and is covered under this copyright:

    Copyright 2011, Alejandro Mosquera <amosquera@dlsi.ua.es>.  All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice, this
    list of conditions and the following disclaimer in the documentation and/or
    other materials provided with the distribution.


    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''


class PhoneticAlgorithmsES(object):

    @staticmethod
    def string_at(string, start, string_length, lista):
        if ((start < 0) or (start >= len(string))):
            return 0
        for expr in lista:
            if string.find(expr, start, start + string_length) != -1:
                return 1
        return 0

    @staticmethod
    def substr(string, start, string_length):
        v = string[start:start + string_length]
        return v

    @staticmethod
    def is_vowel(string, pos):
        return string[pos] in [u'A', u'E', u'I', u'O', u'U']

    @staticmethod
    def strtr(st):
        if st:
            st = st.replace(u'á', u'A')
            st = st.replace(u'ch', u'X')
            st = st.replace(u'ç', u'S')
            st = st.replace(u'é', u'E')
            st = st.replace(u'í', u'I')
            st = st.replace(u'ó', u'O')
            st = st.replace(u'ú', u'U')
            st = st.replace(u'ñ', u'NY')
            st = st.replace(u'gü', u'W')
            st = st.replace(u'ü', u'U')
            st = st.replace(u'b', u'V')
            #st = st.replace(u'z', u'S')
            st = st.replace(u'll', u'Y')
            return st
        else:
            return u''

    def __init__(self):
            pass

    def metaphone(self, string):
        #initialize metaphone key string
        meta_key = ""
        #set maximum metaphone key size
        key_length = 6
        #set current position to the beginning
        current_pos = 0
        #get string length
        # string_length = len(string)  # never used
        #set to  the end of the string
        # var never used
        # end_of_string_pos = string_length - 1
        original_string = string + "    "
        #Let's replace some spanish characters  easily confused
        original_string = self.strtr(original_string.lower())
        #convert string to uppercase
        original_string = original_string.upper()
        # main loop
        while (len(meta_key) < key_length):
            #break out of the loop if greater or equal than the length
            if (current_pos >= len(original_string)):
                break
                #get character from the string
            current_char = original_string[current_pos]
            #if it is a vowel, and it is at the begining of the string,
            #set it as part of the meta key
            if (self.is_vowel(original_string, current_pos)
                and (current_pos == 0)):
                meta_key += current_char
                current_pos += 1
                 #Let's check for consonants  that have a single sound
                 #or already have been replaced  because they share the same
                 #sound like u'B' for u'V' and u'S' for u'Z'
            else:
                if (self.string_at(original_string, current_pos, 1,
                    [u'D', u'F', u'J', u'K', u'M', u'N', u'P', u'T', u'V',
                     u'L', u'Y'])):
                    meta_key += current_char
                    #increment by two if a repeated letter is found
                    if (self.substr(original_string,
                                    current_pos + 1, 1) == current_char):
                        current_pos += 2
                    else:  # increment only by one
                        current_pos += 1
                else:  # check consonants with similar confusing sounds
                    if current_char == u'C':
                        #special case u'macho', chato,etc.
                        #if (self.substr(original_string, current_pos + 1,1)== u'H'):
                        #    current_pos += 2
                        #special case u'acción', u'reacción',etc.
                        if (self.substr(original_string,
                                        current_pos + 1, 1) == u'C'):
                            meta_key += u'X'
                            current_pos += 2
                        # special case u'cesar', u'cien', u'cid', u'conciencia'
                        elif (self.string_at(original_string, current_pos, 2,
                                             [u'CE', u'CI'])):
                            meta_key += u'Z'
                            current_pos += 2
                        else:
                            meta_key += u'K'
                            current_pos += 1
                    elif current_char == u'G':
                        # special case u'gente', u'ecologia',etc
                        if (self.string_at(original_string, current_pos, 2,
                                           [u'GE', u'GI'])):
                            meta_key += u'J'
                            current_pos += 2
                        else:
                            meta_key += u'G'
                            current_pos += 1
                    #since the letter u'h' is silent in spanish,
                    #let's set the meta key to the vowel after the letter u'h'
                    elif current_char == u'H':
                        if (self.is_vowel(original_string,
                            current_pos + 1)):
                            meta_key += original_string[current_pos + 1]
                            current_pos += 2
                        else:
                            meta_key += u'H'
                            current_pos += 1
                    elif current_char == u'Q':
                        if (self.substr(original_string,
                            current_pos + 1, 1) == u'U'):
                            current_pos += 2
                        else:
                            current_pos += 1
                            meta_key += u'K'
                    elif current_char == u'W':
##                                                if (current_pos == 0):
##                                                        meta_key += u'V'
##                              current_pos += 2
                        meta_key += u'U'
                        current_pos += 1
                    # perro, arrebato, cara
                    elif current_char == u'R':
                        current_pos += 1
                        meta_key += u'R'
                    # spain
                    elif current_char == u'S':
                        if (not self.is_vowel(original_string, current_pos + 1)
                            and current_pos == 0):
                            meta_key += u'ES'
                            current_pos += 1
                        else:
                            current_pos += 1
                            meta_key += u'S'
                    # zapato
                    elif current_char == u'Z':
                        current_pos += 1
                        meta_key += u'Z'
                    elif current_char == u'X':
                    #some mexican spanish words like'Xochimilco','xochitl'
##                               if (current_pos == 0):
##
##                              meta_key += u'S'
##                              current_pos += 2
##
##                               else:
                        if (not self.is_vowel(original_string, current_pos + 1)
                            and len(string) > 1 and current_pos == 0):
                            meta_key += u'EX'
                            current_pos += 1
                        else:
                            meta_key += u'X'
                            current_pos += 1
                    else:
                        current_pos += 1
         #trim any blank characters
        meta_key = meta_key.strip()
         #return the final meta key string
        return meta_key

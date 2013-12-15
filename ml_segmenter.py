#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
    ml_segmenter.py

:Authors:
    Soufian Salim (soufi@nsal.im)

:Date:
    15 december 2013 (creation)

:Description:
    Japanese text segmentation with Wapiti
"""

from xml.dom.minidom import parse

import sys
import codecs
import subprocess
import os


# Parameters
WAPITI_TRAIN_FILE = "temp/wapiti_train.txt"
WAPITI_TEST_FILE = "temp/wapiti_test.txt"
WAPITI_RESULT_FILE = "temp/wapiti_result.txt"
WAPITI_MODEL_FILE = "temp/wapiti_model.txt"

PATTERN_FILE = "patterns"


# Main
def main(argv):
    if len(argv) != 3:
        print("Usage : ml_segmenter.py xml_training_file xml_test_file xml_output_file")
        sys.exit()

    print("Converting %s to wapiti datafile..." % argv[0])
    convertTrainFile(argv[0], WAPITI_TRAIN_FILE)

    print("Converting %s to wapiti datafile..." % argv[1])
    convertTestFile(argv[1], WAPITI_TEST_FILE)

    print("Training model...")
    subprocess.call("wapiti train -a rprop -p " + PATTERN_FILE + " " + WAPITI_TRAIN_FILE + " " + WAPITI_MODEL_FILE, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'), shell=True)

    print("Applying model on test data...")
    subprocess.call("wapiti label -m " + WAPITI_MODEL_FILE + " -p " + WAPITI_TEST_FILE + " " + WAPITI_RESULT_FILE, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'), shell=True)

    print("Building sentences from intermediate result file...")
    sentences = makeSentences(WAPITI_RESULT_FILE)

    print("Converting sentences to xml...")
    convertToXML(sentences, argv[2])
    print("XML exported: run 'python evaluation.py %s data/knbc-reference.xml' for evaluation" % argv[2])


# Creates wapiti train file
def convertTrainFile(xml_train_file, wapiti_train_file):
    with codecs.open(wapiti_train_file, 'w', 'utf-8') as train_file:
        for sentence in parse(xml_train_file).getElementsByTagName('sentence'):
            for token in sentence.getElementsByTagName('token'):
                string = token.firstChild.wholeText
                pos = 1

                for char in string:
                    line = char + '\tS\n' if pos == len(string) else char + '\tC\n'
                    train_file.write(line)
                    pos += 1

            train_file.write('\n')


# Creates wapiti test file
def convertTestFile(xml_test_file, wapiti_test_file):
    with codecs.open(wapiti_test_file, 'w', 'utf-8') as test_file:
        for sentence in parse(xml_test_file).getElementsByTagName('sentence'):
            raw = sentence.getElementsByTagName('raw')[0].firstChild.wholeText
            for car in raw:
                test_file.write(car + '\n')
            test_file.write('\n')


# make sentences
def makeSentences(wapiti_result_file):
    sentences = []

    with codecs.open(wapiti_result_file, "r", "utf-8") as results:
        sen = ""

        for line in results:
            if line == "\n":
                sentences.append(sen)
                sen = ""
            else:
                sen += line[:1] + " " if line[-2] == "S" else line[:1]

    return sentences


# Converts sentences to xml for evaluation
def convertToXML(sentences, output_file):
    with codecs.open(output_file, "w", "utf-8") as out:
        out.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        out.write('<dataset>\n')

        i = 0

        for sen in sentences:
            out.write('\t<sentence sid="' + str(i) + '">\n')
            out.write('\t\t<raw>' + sen[:-1] + '</raw>\n')
            out.write('\t</sentence>\n')
            i += 1

        out.write('</dataset>')

# Launch
if __name__ == "__main__":
    main(sys.argv[1:])

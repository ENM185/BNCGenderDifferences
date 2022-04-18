import xml.etree.ElementTree as ET
import os
from collections import defaultdict

def parse_turn(turn, sexes):
    u_sex = sexes[turn.attrib["who"]]

    f = ""
    if u_sex == 'm':
        f = open("male_sentences.txt", "a")
    elif u_sex == 'f':
        f = open("female_sentences.txt", "a")
    else:
        return

    for sentence in turn:
        if sentence.tag != "s":
            continue
        for word in sentence:
            if word.tag != "w":
                if word.tag == "mw":
                    for w in word:
                        f.write(w.attrib["hw"] + "_" + w.attrib["pos"] + " ")
                continue
            f.write(word.attrib["hw"] + "_" + word.attrib["pos"] + " ")
        f.write("\n")
    f.close()

folder = "/Users/eric/Downloads/download/Texts"
t = open("male_sentences.txt", "w")
t.close()
t = open("female_sentences.txt", "w")
t.close()
for subdir in os.listdir(folder):
    if not subdir.startswith('.'):
        for subsubdir in os.listdir(folder + '/' + subdir):
            if not subsubdir.startswith('.'):
                for fn in os.listdir(folder + '/' + subdir + '/' + subsubdir):
                    if fn.endswith('.xml'):
                        path = folder + '/' + subdir + '/' + subsubdir + '/' + fn
                        print(path)

                        tree = ET.parse(path)
                        root = tree.getroot()

                        header = root.find("teiHeader")
                        stext = root.find("stext")

                        if stext != None:
                            profileDesc = header.find('profileDesc')
                            particDesc = profileDesc.find('particDesc')

                            if profileDesc == None:
                                continue
                            if particDesc == None:
                                continue

                            sexes = defaultdict(lambda: "")

                            for person in particDesc:
                                assert person.tag == "person"
                                if "sex" in person.attrib:
                                    sexes[person.attrib["{http://www.w3.org/XML/1998/namespace}id"]] = person.attrib['sex']
                                else:
                                    sexes[person.attrib["{http://www.w3.org/XML/1998/namespace}id"]] = 'u'

                            for turn in stext:
                                if turn.tag == "div":
                                    for t in turn:
                                        if t.tag != "u":
                                            continue
                                        parse_turn(t, sexes)
                                else:
                                    assert turn.tag == "u"
                                    parse_turn(turn, sexes)


import json
import re
import sys
import html

def main():
    CUT_SM = 20
    CUT_ML = 100
    CUT_L = 300
    labelf_l = open("labels.long.txt", "w")
    labelf_m = open("labels.medium.txt", "w")
    labelf_s = open("labels.short.txt", "w")
    contentf_l = open("contents.long.txt", "w")
    contentf_m = open("contents.medium.txt", "w")
    contentf_s = open("contents.short.txt", "w")
    deleted = re.compile(r"\[deleted\]")
    punc = re.compile(r"[\(\)\[\]\{\}`~/\\<>\*\-\+\&\^%$#@_=\|]")
    white = re.compile(r"\s+")
    url = re.compile(r"\S*://\S+")
    quote = re.compile(r"\u2018|\u2019")
    dataf = open(sys.argv[1], "r")
    logf = open("log.txt", "w")
    for line in dataf:
        data = json.loads(line)
        label = data["label"]
        content = data['data']['title'] + " " + " ".join(data['data']['comments'])
        content = deleted.sub(" ", content)
        content = url.sub(" ", content)
        content = html.unescape(content)
        content = quote.sub("\'", content)
        content = punc.sub(" ", content)
        content = white.sub(" ", content)
        tokens = content.split(" ")
        if len(tokens) > CUT_L:
            content = " ".join(tokens[0:300])
            f = contentf_l
            lf = labelf_l
        elif len(tokens) < CUT_SM:
            f = contentf_s
            lf = labelf_s
        elif len(tokens) < CUT_ML:
            f = contentf_m
            lf = labelf_m
        else:
            f = contentf_l
            lf = labelf_l
        while True:
            try:
                f.write(content + "\n")
            except UnicodeEncodeError as err:   
                content = content[:err.start] + content[err.end:]
                continue
            break
        while True:
            try:
                lf.write(label + "\n")
            except UnicodeEncodeError as err:
                label = label[:err.start] + label[err.end:]
                continue
            break
    dataf.close()

main()
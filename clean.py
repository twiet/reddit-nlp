import json
import re
import sys
import html
import codecs

def main():
    CUT_SM = 20
    CUT_ML = 100
    CUT_L = 300
    labelf_l = codecs.open("labels." + str(CUT_L) + ".txt", "w", "utf-8")
    labelf_m = codecs.open("labels." + str(CUT_ML) + ".txt", "w", "utf-8")
    labelf_s = codecs.open("labels." + str(CUT_SM) + ".txt", "w", "utf-8")
    contentf_l = codecs.open("contents." + str(CUT_L) + ".txt", "w", "utf-8")
    contentf_m = codecs.open("contents." + str(CUT_ML) + ".txt", "w", "utf-8")
    contentf_s = codecs.open("contents." + str(CUT_SM) + ".txt", "w", "utf-8")
    deleted = re.compile(r"\[deleted\]")
    punc = re.compile(r"[\(\)\[\]\{\}`~/\\<>\*\-\+\&\^%$#@_=\|]")
    end1 = re.compile(r"\.")
    end2 = re.compile(r",")
    end3 = re.compile(r"\?")
    end4 = re.compile(r"\!")
    end5 = re.compile(r":")
    end6 = re.compile(r";")
    white = re.compile(r"\s+")
    url = re.compile(r"\S*://\S+")
    quote = re.compile(r"\u2018|\u2019")
    dquote = re.compile(r"\u201c|\u201d")
    quesmk = re.compile(r"\u003f")
    excmk = re.compile(r"\u0021")
    period = re.compile(r"\u002e")
    comma = re.compile(r"\u002c")
    colon = re.compile(r"\u003a")
    semicolon = re.compile(r"\u003b")
    dataf = codecs.open(sys.argv[1], "r", "utf-8")
    logf = open("log.txt", "w")
    for line in dataf:
        data = json.loads(line)
        label = data["label"]
        content = data['data']['title'] + " " + " ".join(data['data']['comments'])
        content = deleted.sub(" ", content)
        content = url.sub(" ", content)
        content = html.unescape(content)
        content = quote.sub("\'", content)
        content = dquote.sub("\"", content)
        content = quesmk.sub("?", content)
        content = excmk.sub("!", content)
        content = period.sub(".", content)
        content = comma.sub(",", content)
        content = colon.sub(":", content)
        content = semicolon.sub(";", content)
        content = punc.sub(" ", content)
        content = end1.sub(" . ", content)
        content = end2.sub(" , ", content)
        content = end3.sub(" ? ", content)
        content = end4.sub(" ! ", content)
        content = end5.sub(" : ", content)
        content = end6.sub(" ; ", content)
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
    labelf_l.close()
    labelf_m.close()
    labelf_s.close()
    contentf_l.close()
    contentf_m.close()
    contentf_s.close()

main()
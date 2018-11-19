import json
import re
import sys
import html

def main():
    maxN = 300
    labelf = open("labels.txt", "w")
    contentf = open("contents.txt", "w")
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
        if len(tokens) > 300:
            content = " ".join(tokens[0:300])
        while True:
            try:
                contentf.write(content + "\n")
            except UnicodeEncodeError as err:
                content = content[:err.start] + content[err.end:]
                continue
            break
        while True:
            try:
                labelf.write(label + "\n")
            except UnicodeEncodeError as err:
                label = label[:err.start] + label[err.end:]
                continue
            break
    labelf.close()
    contentf.close()
    dataf.close()

main()
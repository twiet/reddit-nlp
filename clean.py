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
    dataf = open(sys.argv[1], "r")
    for line in dataf:
        data = json.loads(line)
        label = data["label"]
        content = data['data']['title'] + " " + " ".join(data['data']['comments'])
        content = deleted.sub(" ", content)
        content = url.sub(" ", content)
        content = html.unescape(content)
        content = punc.sub(" ", content)
        content = white.sub(" ", content)
        tokens = content.split(" ")
        if len(tokens) > 300:
            content = " ".join(tokens[0:300])
        labelf.write(label + "\n")
        contentf.write(content + "\n")
    labelf.close()
    contentf.close()
    dataf.close()

main()
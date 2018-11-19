def main():
    stat = [0] * 300
    contentf = open("contents.txt")
    max = 0
    for line in contentf:
        stat[len(line.split(" ")) - 1] += 1
    result = open("result.txt", "w")
    result.write(str(stat))

main()
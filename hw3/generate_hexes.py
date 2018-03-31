def gen_all_hex():
    i = 0
    while i < 2 ** 8:
        yield "{0:0{1}x}".format(i, 2)
        yield "{0:0{1}X}".format(i, 2)
        i += 1


def main():
    with open("data/hexes.txt", "w") as out:
        for l in gen_all_hex():
            out.write("{}\n".format(l))


if __name__ == '__main__':
    main()

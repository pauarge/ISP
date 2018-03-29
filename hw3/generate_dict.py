def get_permutations(s):
    if s.isalnum():
        res = [s]
        res.append(s.title())
        for x in range(6):
            for y in range(6):
                for z in range(6):
                    res.append(s.replace("e", "3", x).replace("o", "0", y).replace("i", "1", z))
                    res.append(s.title().replace("e", "3", x).replace("o", "0", y).replace("i", "1", z))
                    res.append(s.replace("e", "3", x).replace("o", "0", y).replace("i", "1", z).title())
        return list(set(res))
    else:
        return []


def process_file(file, out):
    with open(file) as inp:
        for l in inp:
            for perm in get_permutations(l.strip()):
                out.write("{}\n".format(perm))
                print(perm)


def main():
    with open("data/dict-perms.txt", "w") as out:
        process_file("data/cain.txt", out)
        process_file("data/john.txt", out)
        process_file("data/rockyou.txt", out)


if __name__ == '__main__':
    main()

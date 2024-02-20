import argparse
import json

import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(
    prog="openbugbounty.org scraper",
    description="A program to scrape all scopes from programs listed on openbugbounty.org",
)
parser.add_argument("-oN", help="Output scopes to a text file")
parser.add_argument("-oJ", help="Output programs to a json file")
parser.add_argument("-a", "--all", help="Scrape all programs on the site")
parser.add_argument("-t", "--target", help="Scrape a single program on the site")
parser.add_argument("-p", "--page", default=1, type=int, help="Which page to start at")
parser.add_argument("-n", "--number", default=10, type=int, help="The number of programs to scrape")
args = vars(parser.parse_args())

programs = []
data = {"start": (args["page"] - 1) * 50}

r = requests.post("https://www.openbugbounty.org/bugbounty-list/ajax.php", data=data)
for index, page in enumerate(r.json()["data"]):
    if index == args["number"]:
        break

    program = {}
    program["url"] = "https://www.openbugbounty.org" + page[0].split('"')[1]
    programs.append(program)

for program in programs:
    p = requests.get(program["url"])
    soup = BeautifulSoup(p.content, "html.parser")
    wishlist = soup.find("table", class_="wishlist")

    program["scope"] = []
    for scope in wishlist.find_all("td"):
        program["scope"].append(scope.contents[0])

output = "\n".join(sum([program["scope"] for program in programs], []))

print(output)
if args["oN"]:
    with open(args["oN"], "w") as f:
        f.write(output)

if args["oJ"]:
    with open(args["oJ"], "w") as f:
        f.write(json.dumps(programs))

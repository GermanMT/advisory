import requests
from bs4 import BeautifulSoup

repo = "diverso-lab/pysat_metamodel"
# repo = "diverso-lab/pysat_metamodel"
url = f'https://github.com/{repo}/network/dependents'
dependets = []
i = 0

while True:
    i += 1
    # print("GET - " + url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    data = [
        "{}/{}".format(
            t.find('a', {"data-repository-hovercards-enabled":""}).text,
            t.find('a', {"data-hovercard-type":"repository"}).text
        )
        for t in soup.findAll("div", {"class": "Box-row"})
    ]

    dependets.extend(data)

    paginationContainer = soup.find("div", {"class":"paginate-container"})
    if paginationContainer:
        try:
            url = paginationContainer.find('a')["href"]
        except:
            break
    else:
        break

print(dependets)
print("Number of dependents: " + str(len(dependets)))
print("Number of pages: " + str(i))
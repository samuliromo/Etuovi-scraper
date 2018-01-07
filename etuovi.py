"""
Web scraper -tyyppinen ohjelma, jolla haetaan Etuovi.com:ista asuntojen tiedot
tietystä kaupungista, ja tallennetaan ne tiedostoon.
HUOM! Saattaa hajota jos sivuston rakenne muuttuu.
Viimeisin toimiva versio 8.1.2018
"""

import bs4 as bs, requests, datetime, json


def parse_pages(number):
    res = requests.get("{}&rd=50&page={}".format(link, number))
    soup = bs.BeautifulSoup(res.text, 'lxml')
    for column in soup.find_all("a", {"class" : "facts"}):
        try:
            apartment_info = []

            a_type = column.find("div", {"class" : "type"})
            a_type = a_type.find("label")
            apartment_info.append(a_type.text)
            
            address = column.find("div", {"class" : "address"})
            area = address.find("span")
            apartment_info.append(area.text.split(",")[0].split(" ")[0])

            size = column.find("div", {"class" : "size"})
            squares = size.find("span")
            apartment_info.append(handle_number(squares.text))

            price = column.find("div", {"class" : "price"})
            euros = price.find("span")
            apartment_info.append(handle_number(euros.text))

            year = column.find("div", {"class" : "year"})
            built = year.find("span")
            apartment_info.append(built.text)

            apartments.append(apartment_info)
            print(apartment_info)
        except:
            print("puutteelliset tiedot: " + str(apartment_info))
            
    print("sivu: "+str(number))
    print(len(apartments))
    button = soup.find("a", {"title" : "Seuraava"})
    if "disabled" not in button["class"]:
        parse_pages(number+1)


def handle_number(string):
    return "".join(string.split("m")[0].split("€")[0].split(" ")).replace(",",".")


cities = {}
apartments = []
index = 0
link = ""

try:
    cities = json.load(open("links.txt"))
except Exception as e:
    print(e)

city = input("Anna kaupungin nimi:")
if city not in cities:
    link = input("Anna Etuovi.com hakutuloksien linkki muodossa https://www.etuovi.com/myytavat-asunnot/tulokset?haku=M0123456789 (ei mitään ensimmäisen numeron jälkeen):")
    cities[city] = link
    print(link)
else:
    link = cities[city]
    print(link)


parse_pages(1)


output = "{}_asunnot_{}.csv".format(city, datetime.date.today())
try:
    with open(output,"w+")as output:
        output.write("type,area,size,price,year\n")
        for apartment in apartments:
            output.write(",".join(apartment)+"\n")
        json.dump(cities, open("links.txt","w"))
except Exception as e:
    print(e)

"""
Web scraper for getting apartment prices from Etuovi.com. Might break if
the website changes.
Samuli Romo 8.1.2018
"""

import bs4 as bs, requests, datetime, json, sys


def parse_pages(number):
    """This method returns the search results, parses them and saves the
information, and repeats the process until it gets to the end of search results.
Parameters
----------
number : int
    Number of the search result page where parsing starts
"""
    try:
        res = requests.get("{}&rd=50&page={}".format(link, number))
    except:
        print("Virheellinen url")
        return
    soup = bs.BeautifulSoup(res.text, 'lxml')
    for column in soup.find_all("li", {"class": "residental"}):
        try:
            apartment_info = []
            apartment_info.append(column["id"])
            
                
            a_type = column.find("div", {"class": "type"})
            a_type = a_type.find("label")
            apartment_info.append(a_type.text)
                
            address = column.find("div", {"class": "address"})
            area = address.find("span")
            apartment_info.append(area.text.split(",")[0].split(" ")[0])

            size = column.find("div", {"class": "size"})
            squares = size.find("span")
            apartment_info.append(handle_number(squares.text))

            price = column.find("div", {"class": "price"})
            euros = price.find("span")
            apartment_info.append(handle_number(euros.text))

            year = column.find("div", {"class": "year"})
            built = year.find("span")
            apartment_info.append(built.text)
                
            apartments.append(apartment_info)
            print(apartment_info)
        except Exception as e:
            #print("puutteelliset tiedot: " + str(apartment_info))
            print(e)

    print("sivu: " + str(number))
    print(len(apartments))
    button = soup.find("a", {"title": "Seuraava"})
    if "disabled" not in button["class"]:
        parse_pages(number + 1)


def handle_number(string):
    """This method will modify price and size information so they will be easier
to operate on
Parameters
----------
string : str
    String to be parsed for numbers
"""
    return "".join(string.split("m")[0].split("€")[0].split(" ")).replace(",", ".")


cities = {}
apartments = []
index = 0
city = ""
link = ""

try:
    cities = json.load(open("links.txt"))
except Exception as e:
    print(e)

if len(sys.argv) > 1:
    city = sys.argv[1]
else:
    city = input("Anna kaupungin nimi:")

try:
    if city not in cities:
        link = input(
            "Anna Etuovi.com hakutuloksien linkki muodossa:"
            "https://www.etuovi.com/myytavat-asunnot/tulokset?haku=M0123456789 "
            "(ei mitään ensimmäisen numeron jälkeen):")
        cities[city] = link
        print(link)
    else:
        link = cities[city]
        print(link)
except:
    print("Virheellinen url-osoite")

parse_pages(1)

output = "{}_asunnot_{}.csv".format(city, datetime.date.today())

try:
    with open(output, "w+")as output:
        output.write("type,area,size,price,year\n")
        for apartment in apartments:
            output.write(",".join(apartment) + "\n")
        json.dump(cities, open("links.txt", "w"))
except Exception as e:
    print(e)

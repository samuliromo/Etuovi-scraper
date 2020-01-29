# Etuovi-scraper
Python script for downloading apartment price information from Etuovi.com

<b>Does not work as of 1/2020 because Etuovi.com has changed its layout</b>

This is a simple program that lets you download house and apartment price information from Etuovi.com. It downloads apartment type, price, area, size in square meters, and the year of construction for every apartment from the city that the user specifies in the beginning, and outputs it to a csv-file. The information may be used to do some statistical analysis, for example to see how price changes vary in different areas within one city.

The program uses the Beautifulsoup library for scraping the search results from the website and lxml to parse them. Currently there is no way of getting the search result url by just typing the city name. The link has to be put in manually by the user, but all the links and their corresponding search result urls are saved in a text file, so this only has to be done once for each city.

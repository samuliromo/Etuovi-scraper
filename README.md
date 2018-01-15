# Etuovi-scraper
Python script for downloading apartment price information from Etuovi.com

This is a simple program that lets you download house and apartment price information from Etuovi.com. It downloads apartment type, price, area, size in square meters, and the year of construction for every apartment from the city that the user specifies in the beginning, and outputs it to a csv-file. The information may be used to do some statistical analysis, for example to see how price changes vary in different areas within one city.

The program uses the Beautifulsoup library for parsing the search results from the website. Currently there is no way of getting the search result url by just typing the city name. The link has to be put in manually by the user, but all the links and their corresponding search result urls are saved in a text file, so this only has to be done once for each city.

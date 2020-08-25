import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser = argparse.ArgumentParser()
parser.add_argument("--page_num_MAX", help="enter the number of pages to parse", type=int)
parse.add_argument("--dbname", help="enter the name of db", type=str)
args = parser.parse_args()
oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
page_num_MAX = args.page_num_max
scraped_info_list = []
connect.connect(args.dbname)
for page_num in range(1,page_num_MAX):
    url = oyo_url + str(page_num)
    print("GET Request for :"+url)
    req = requests.get(url)
    content = req.content
    soup =BeautifulSoup(content, "html.parser")
    all_hotels = soup.find_all("div",{"class": "hotelCardListing"})
    scraped_info_list=[]
    for hotel in all_hotels:
        hotel_dict={}
        hotel_dict["name"]=hotel.find("h3",{"class": "listningHotelDescription_hotelName"}).text
        hotel_dict["address"] =hotel.find("span",{"itemrop": "streetAddress"}).text
        hotel_dict["price"] = hotel.find("span", {"class": "listingPrice__finalPrice"}).text
        try:
            hotel_dict["rating"] =hotel.find("span",{"class": "hotel_rating__ratingSummary"}).text
        except AttributeError:
            hotel_dict["rating"] = None
        parent_ameities_element = hotel.find("div", {"class": "amenityWrapper"})
        ammenities_list = []
        for amenity in parent_ameities_element.find_all("div", {"class": "amenityWrapper__amenity"}):
            ammenities_list.append(amenity.find("span",{"class": "d-body-sm"}).text.strip())
        hotel_dict["amenity"] = ','.join(ammenities_list[:-1])
        scraped_info_list.append(hotel_dict)
        connect.insert_into_table(args.dbname, tuple(hotel_dict.values())
dataframe = pandas.dataframe(scraped_info_list)
print("creating csv file")
dataframe.to_csv("oyo.csv")
connect.get_hotel_info(args.dbname)

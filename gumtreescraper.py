"""
python-gumtree

Gumtree scraper written in Python

Copyright 2013 Oli Allen <oli@oliallen.com>
"""

USER_AGENT = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"
REQUEST_HEADERS = {'User-agent': USER_AGENT,}

import requests
import re
from bs4 import BeautifulSoup

class SearchListing:
    """
    A gumtree search result set containing GTItem objects
    """

    def __init__(self, category, query="", location=""):
        self.category = category
        self.query = query    
        self.location = location



        self.listing_results = self.doSearch()


    def __str__(self):
        return "Search listing"

    def doSearch(self):
        """
        Performs the search against gumtree
        """

        request = requests.get("http://www.gumtree.com/search?q=%s&search_location=%s&category=%s" % (self.query, self.location, self.category), headers=REQUEST_HEADERS)


        if request.status_code == 200:
            # Got a valid response

            listing_results = []

            souped = BeautifulSoup(request.text, "html5lib")
            for listings_wrapper in souped.find_all("ul", class_="ad-listings"):
                for listing in listings_wrapper.find_all("li", class_="offer-sale"):
                    title = listing.find("a", class_="description").get("title")
                    item_instance = GTItem(title=title)
                    item_instance.url = listing.find("a", class_="description").get("href")
                    item_instance.price = listing.find("span", class_="price").string
                    item_instance.summary = listing.find("div", class_="ad-description").find("span").string
                    item_instance.location =  listing.find("span", class_="location").string
                    item_instance.thumbnail = listing.find("img", class_="thumbnail").get("src")
                    item_instance.adref = listing.find("div", class_="ad-save").get("data-ad-id")

                    listing_results.append(item_instance)
            return listing_results
        else:
            # TODO: Add error handling
            print "Server returned code %s" % request.status_code
            return []



class GTItem:
    """
    An individual gumtree item
    """
    def __init__(self, title, summary="", description="", thumbnail="", price="", location="", adref="", url="", contact_name="", contact_number="", images=[]):
        self.title = title
        self.summary = summary
        self.thumbnail = thumbnail
        self.price = price
        self.location = location
        self.adref = adref
        self.url = url
                
        self._description = None
        self._contact_name = None
        self._contact_number = None
        self._images = None

        self._longitude = None
        self.latitude = None

    @property
    def images(self):
        if not self._images:
            
            self._images = ['test',]
        return self._images

    @property
    def description(self):
        if not self._description:
            self.getFullInformation()
        return self._description
	
    @property
    def contact_name(self):
        if not self._contact_name:
            self.getFullInformation()
        return self._contact_name

    @property
    def contact_number(self):
        if not self._contact_number:
            self.getFullInformation()
        return self._contact_number

    @property
    def latitude(self):
        if not self._latitude:
            self.getFullInformation()
        return self._latitude

    @property
    def longitude(self):
        if not self._longitude:
            self.getFullInformation()
        return self._longitude

    def __str__(self):
        return self.title
	

    def getFullInformation(self):
        """
        Scrape information from a full gumtree advert page
        """
        request = requests.get(self.url, headers=REQUEST_HEADERS)
        if request.status_code == 200:
            # Got a valid response
            souped = BeautifulSoup(request.text, "html5lib")
            description = souped.find("div", id="vip-description-text").string
            if description:
                self._description = description.strip()
            else:
                self._description = ""
            contact = souped.find(class_="phone")
            if not contact:
                self._contact_name, self._contact_number = ["",""]
            else:
                if " on " in contact.string:
                    self._contact_name, self._contact_number = contact.string.split(" on ")
                else:
                    self._contact_name, self._contact_number = ["", contact.string]

            gmaps_link = souped.find("a", class_="open_map")
            if gmaps_link:
                self._latitude, self._longitude = re.search("center=(-?\w.*),(-?\d.*)&sensor", gmaps_link.get("data-target")).groups()
            else:
                self._latitude, self._longitude = ["", ""]

            return
        else:
            # TODO: Add error handling
            print "Server returned code %s for %s" % (request.status_code, url)
            return []

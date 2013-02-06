"""
python-gumtree

Gumtree scraper written in Python

Copyright 2013 Oli Allen <oli@oliallen.com>

THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND, AND MAY BE
COPIED, MODIFIED OR DISTRIBUTED IN ANY WAY, AS LONG AS THIS NOTICE
AND ACKNOWLEDGEMENT OF AUTHORSHIP REMAIN.
"""

USER_AGENT = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"

import requests
from bs4 import BeautifulSoup

class SearchListing:
    """
    A gumtree search result set containing GTItem objects
    """

    def __init__(self, category, query=False, location=False):
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

        request_headers = {'User-agent': USER_AGENT,}

        request = requests.get("http://www.gumtree.com/motorbikes-scooters", headers=request_headers)

        if request.status_code == 200:
            # Got a valid response

            listing_results = []

            souped = BeautifulSoup(request.text, "html5lib")
            for listings_wrapper in souped.find_all("ul", class_="ad-listings"):
                for listing in listings_wrapper.find_all("li", class_="offer-sale"):
                    title = listing.find("a", class_="description").get("title")
                    item_instance = GTItem(title=title)
                    item_instance.price = listing.find("span", class_="price").string
                    item_instance.summary = listing.find("div", class_="ad-description").find("span").string
                    item_instance.location =  listing.find("span", class_="location").string
                    item_instance.thumbnail = listing.find("img", class_="thumbnail").get("src")
                    listing_results.append(item_instance)
            return listing_results
        else:
            # TODO: Add error handling
            return []

class GTItem:
    def __init__(self, title, summary="", description="", thumbnail="", price="", location="", adref="", url="", contact_name="", contact_number=""):
        self.title = title

    def __str__(self):
        return self.title

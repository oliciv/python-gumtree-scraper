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
        self.doSearch()

    def __str__(self):
        return "Search listing"

    def doSearch(self):
        """
        Performs the search against gumtree
        """

        request_headers = {'User-agent': 'Mozilla/5.0',}        

        request = requests.get("http://www.gumtree.com/motorbikes-scooters", headers=request_headers)

        if request.status_code == 200:
            # Got a valid response
            souped = BeautifulSoup(request.text, "html5lib")
            print souped.find_all("ul", class_="ad-listings")
        else:
            # TODO: Add error handling
            return []

"""
python-gumtree

Gumtree scraper written in Python

Copyright 2013 Oli Allen <oli@oliallen.com>


THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND, AND MAY BE
COPIED, MODIFIED OR DISTRIBUTED IN ANY WAY, AS LONG AS THIS NOTICE
AND ACKNOWLEDGEMENT OF AUTHORSHIP REMAIN.
"""
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

    def doSearch():
        """
        Performs the search against gumtree
        """
        

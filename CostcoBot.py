##########################################
# Written by Sim Singh Dhaliwal          #
# 2021                                   #
##########################################

import requests
from bs4 import BeautifulSoup

# This header is needed to bypass Costco's bot detection
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

# current page we are examining
url = 'https://www.costco.com/gaming-computers.html'


# This class will check if a item if found as a search result
# meaning that it is probably instock
class WebMonitor:
    def __init__(self, url, keyword):
        self.url = url
        self.keyword = keyword

    # Given a url return a Page will the contents
    def get_page(self, url):
        page = requests.get(url, headers=headers)
        return page

    # This function will take a page and return all tags we are
    # looking for and possibly a HTML attribute
    def filter_page(self, page, search_tag, search_attr=None):
        filtered_tags = []
        soup = BeautifulSoup(page.content, 'html.parser')
        input_tags = soup.findAll(search_tag)
        filtered_tags = input_tags
        if search_attr:
            filtered_tags = list(filter(lambda input_tag: input_tag.has_attr(search_attr), input_tags))


        return filtered_tags

    def find_keyword(self, page, keyword):
        soup = BeautifulSoup(page.content, 'html.parser')
        return keyword in soup.text

    def check_product(self):
        x = self.filter_page(self.get_page(self.url), 'input', 'data-description')
        
        for a in x:
            if self.keyword in str(a):
                return True

        return False

x = WebMonitor(url, 'i7')
print(x.check_product())

""" this will scrape all the information from billboard's site."""
# pylint: disable-msg=C0103
from urllib import urlopen
from bs4 import BeautifulSoup

class Scraper(object):
    """Class that'll contain the categories and its methods."""
    categories = dict()
    base = 'http://www.billboard.com/charts/'
    bsoup = ''

    def __init__(self, parser):
        self.bsoup = BeautifulSoup(urlopen(self.base), parser)

    def init_categories(self):
        """scrapes the charts site and collects all charts of each category."""
        table = self.bsoup.find("div", {"id" : "charts-list"})
        current_cat = ''
        for child in table.children:
            name = child.name
            if name == 'h3':
                current_cat = child.get_text()
                self.categories[current_cat] = dict()
            elif name == 'article':
                chart = child.findChild("a", {"class" : "chart-row__chart-link"})
                self.categories[current_cat][chart.get_text()] = chart['href']

    def get_charts(self, category):
        """gets list of all charts of a category."""
        return self.categories[category].keys()

    def get_link_of_chart(self, genre, chart):
        """gets trailing part of the link for the specified chart."""
        return self.categories[genre][chart]

    def get_full_link(self, genre, chart):
        """gets full link of the specified chart."""
        return 'http://www.billboard.com' + self.get_link_of_chart(genre, chart)

    def print_categories(self):
        """outputs all categories that were found on the charts site."""
        ctr = -1
        for cat in self.categories.keys():
            ctr += 1
            print ctr, ': ', cat

    def print_charts(self, category):
        """outputs all categories that were found on the charts site."""
        ctr = -1
        for cat in self.get_charts(category):
            ctr += 1
            print ctr, ': ', cat

billboard = Scraper('html.parser')
billboard.init_categories()
billboard.print_categories()

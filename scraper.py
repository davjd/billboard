""" this will scrape all the information from billboard's site."""
# pylint: disable-msg=C0103
from urllib import urlopen
from bs4 import BeautifulSoup

class Song(object):
    """Class that'll contain the categories and its methods."""
    title = ''
    artist = ''
    artist_href = ''
    img_src = ''
    current_week = ''
    last_week = ''

    def __init__(self, title, artist, artist_href, img_src, current_week, last_week):
        self.title = title
        self.artist = artist
        self.artist_href = artist_href
        self.img_src = img_src
        self.current_week = current_week
        self.last_week = last_week


class Scraper(object):
    """Class that'll contain the categories and its methods."""
    categories = dict()
    base = 'http://www.billboard.com/charts/'
    parser = ''
    bsoup = ''

    def __init__(self, parser):
        self.parser = parser
        self.bsoup = BeautifulSoup(urlopen(self.base), self.parser)

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
    
    def get_songs(self, genre, chart):
        """will get all songs of a chart, creating song objects."""
        link = self.get_full_link(genre, chart)
        soup = BeautifulSoup(urlopen(link), self.parser)
        cells = soup.find_all("div", {"class" : "chart-row__main-display"})
        for cell in cells:
            rank = cell.find("div", {"class" : "chart-row__rank"})
            current = rank.find("span", {"class" : "chart-row__current-week"}).get_text()
            last_week = rank.find("span", {"class" : "chart-row__last-week"}).get_text()
            img_block = cell.find("div", {"class" : "chart-row__image"})
            img_src = ''
            if img_block.has_attr('style'):
                img_src = img_block['style']
            elif img_block.has_attr('data-imagesrc'):
                img_src = img_block['data-imagesrc']
            print img_src, '\n'


billboard = Scraper('html.parser')
billboard.init_categories()
billboard.get_songs("R&B/Hip-Hop", "Hot R&B/Hip-Hop Songs")

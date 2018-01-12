""" this will scrape all the information from billboard's site."""
# pylint: disable-msg=C0103
from urllib import urlopen
from bs4 import BeautifulSoup

class Song(object):
    """Class that'll contain the categories and its methods."""
    title = ''
    artist = ''
    img_src = ''
    current_week = ''
    last_week = ''

    def __init__(self, title, artist, img_src, current_week, last_week):
        self.title = title
        self.artist = artist
        self.img_src = img_src
        self.current_week = current_week
        self.last_week = last_week


class Scraper(object):
    """Class that'll contain the categories and its methods."""
    categories = dict()
    base = 'http://www.billboard.com/charts/'
    parser = ''
    bsoup = ''

    def __init__(self, parser, initialize=False):
        self.parser = parser
        self.bsoup = BeautifulSoup(urlopen(self.base), self.parser)
        if initialize:
            self.init_categories()

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

    @staticmethod
    def parse_style_img(img_src):
        """parses url css format to obtain link of img src."""
        start_idx = img_src.find('(') + 1
        end_idx = img_src.find(')')
        return img_src[start_idx:end_idx]

    @staticmethod
    def parse_html_text(txt):
        """removes all newlines from a string, needed because of how get_text() works."""
        return txt.strip().replace("\t", " ").replace("\r", " ").replace('\n', ' ')

    def get_list(self, genre, chart):
        """will get songs/albums of a chart, creating song objects."""
        songs = []
        link = self.get_full_link(genre, chart)
        soup = BeautifulSoup(urlopen(link), self.parser)
        cells = soup.find_all("div", {"class" : "chart-row__main-display"})
        for cell in cells:
            img_src = ''
            artist = ''

            rank = cell.find("div", {"class" : "chart-row__rank"})
            current_week = rank.find("span", {"class" : "chart-row__current-week"}).get_text()
            last_week = rank.find("span", {"class" : "chart-row__last-week"}).get_text()

            img_block = cell.find("div", {"class" : "chart-row__image"})
            if img_block.has_attr('style'):
                img_src = self.parse_style_img(img_block['style'])
            elif img_block.has_attr('data-imagesrc'):
                img_src = img_block['data-imagesrc']
            else:
                img_src = 'https://www.billboard.com/assets/1515013425/images/chart-row-placeholder.jpg?e7e59651befde326da9c'

            info_row = cell.find("div", {"class" : "chart-row__container"})
            title = info_row.find("h2", {"class" : "chart-row__song"}).get_text()
            artist_anchor = info_row.find("a", {"class" : "chart-row__artist"})
            artist_span = info_row.find("span", {"class" : "chart-row__artist"})
            if artist_anchor is not None:
                artist = self.parse_html_text(artist_anchor.get_text())
            elif artist_span is not None:
                artist = self.parse_html_text(artist_span.get_text())
            songs.append(Song(title, artist, img_src, current_week, last_week))
        return songs

    def print_song_info(self, genre, chart):
        """prints song information of a given category and chart."""
        songs = self.get_list(genre, chart)
        for song in songs:
            print 'artist: ', song.artist
            print 'title: ', song.title
            print 'img: ', song.img_src
            print 'current rank: ', song.current_week
            print 'last week rank: ', song.last_week, '\n'



billboard = Scraper('html.parser')
billboard.init_categories()
billboard.print_song_info("Overall Popularity", "Hot 100")

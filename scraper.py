""" this will scrape all the information from billboard's site."""
# pylint: disable-msg=C0103
from urllib import urlopen
from bs4 import BeautifulSoup

base = 'http://www.billboard.com/charts/'
category = ''
date = ''

categories = dict()

r = urlopen(base + category + date)
soup = BeautifulSoup(r, 'html.parser')
#table = soup.find("div", {"id" : "charts-list"})

def scrape_categories(bsoup, category_dict):
    """scrapes the charts site and collects all charts of each category."""
    table = bsoup.find("div", {"id" : "charts-list"})
    current_cat = ''
    for child in table.children:
        name = child.name
        if name == 'h3':
            current_cat = child.get_text()
            category_dict[current_cat] = []
        elif name == 'article':
            chart = child.findChild("a", {"class" : "chart-row__chart-link"})
            category_dict[current_cat].append((chart.get_text(), chart['href']))
def print_charts(category_list):
    """outputs all charts in a category."""
    ctr = -1
    for chart in category_list:
        ctr += 1
        print ctr, ': ', chart[0]
def print_categories(category_dict):
    """outputs all categories that were found on the charts site."""
    ctr = -1
    for cat in category_dict.keys():
        ctr += 1
        print ctr, ': ', cat
scrape_categories(soup, categories)



# this will be used for testing for now. I'll modularize it later...

print 'Which genre do you want to view charts of?'
print_categories(categories)
pick = int(input("Enter a number: "))

if pick > len(categories.keys()) or pick < 0:
    print 'The inputted number isn\'t valid.'
else:
    print 'Which chart do you want to view?'
    charts = categories[categories.keys()[pick]]
    print_charts(charts)
    pick = int(input("Enter a number: "))
    if pick > len(charts) or pick < 0:
        print 'The inputted number isn\'t valid.'
    else:
        link = 'http://www.billboard.com' + charts[pick][1]
        print 'link: ', link
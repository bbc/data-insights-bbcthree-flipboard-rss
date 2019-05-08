# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 10:08:59 2019

@author: hibbep01
"""

"""Provides the RSS2Feed class."""

from calendar import timegm
from email.utils import formatdate
from xml.dom.minidom import Document
import requests
from bs4 import BeautifulSoup
import re

### Define RSS2Feed to create the XML Feed

class RSS2Feed(object):
    """An RSS 2.0 feed."""

    class FeedError(Exception):
        """Error encountered while producing a feed."""

    def __init__(self, title, link, description):
        """Initialize the feed with the specified attributes.
        :param title: brief title for the feed
        :param link: URL for the page containing the syndicated content
        :param description: longer description for the feed
        """
        self._document = Document()
        rss_element = self._document.createElement('?xml')
        rss_element.setAttribute('encoding', 'utf-8')
        rss_element.setAttribute('version', '1.0')
        rss_element = self._document.createElement('rss')
        rss_element.setAttribute('xmlns:media', 'http://search.yahoo.com/mrss/')
        rss_element.setAttribute('version', '2.0')
        self._document.appendChild(rss_element)
        self._channel = self._document.createElement('channel')
        rss_element.appendChild(self._channel)
        self._channel.appendChild(self._create_text_element('title', title))
        self._channel.appendChild(self._create_text_element('link', link))
        self._channel.appendChild(self._create_text_element('description', description))

    def _create_text_element(self, type_, text):
        """Create a text element and return it."""
        element = self._document.createElement(type_)
        element.appendChild(self._document.createTextNode(text))
        return element

    def append_item(self, title=None, link=None, description=None, pub_date=None, author=None, image=None, guid=None):
        """Append the specified item to the feed.
        :param title: brief title for the item
        :param link: URL for the page for the item
        :param description: longer drescription for the item
        :param pub_date: UTC timestamp or datetime instance of the item's publication date
        :param author: author for the page for the item
        :param image: image for the page for the item
        """
        # Either title or description *must* be present
        if title is None and description is None:
            raise self.FeedError("Either title or description must be provided.")
        element = self._document.createElement('item')
        if not title is None:
            element.appendChild(self._create_text_element('title', title))
        if not link is None:
            element.appendChild(self._create_text_element('link', link))
        if not description is None:
            element.appendChild(self._create_text_element('description', description))
        if not pub_date is None:
            element.appendChild(self._create_text_element('pubDate', pub_date))
#            try:
#                timestamp = int(pub_date)
#            except TypeError:
#                timestamp = timegm(pub_date.utctimetuple())
#            element.appendChild(self._create_text_element('pubDate', formatdate(timestamp)))
        if not author is None:
            element.appendChild(self._create_text_element('author', author))
        if not image is None:
#            element.appendChild(self._create_text_element('enclosure', image))
            element.appendChild(self._document.createElement('media:content url="' + image + '" medium="image" type="image/jpeg" width="704" height="396"'))
        if not guid is None:
            element.appendChild(self._create_text_element('guid', guid))
        self._channel.appendChild(element)

    def get_xml(self):
        """Return the XML for the feed.
        :returns: XML representation of the RSS feed
        """
        return self._document.toxml('utf8')



############
# settings #
############


# The name of the channel
channelTitle = "BBC Three"

# The URL to the HTML website corresponding to the channel.
channelLink = "http://www.bbc.co.uk/bbcthree"

# Phrase or sentence describing the channel.
channelDescription = "All the latest documentaries, comedy, videos, " \
                     "articles and more from the award winning digital " \
                     "channel, BBC Three. Makes you think. Makes you laugh."


# The language of the channel.
channelLanguage = "en"

# specify the url
three_page = 'http://www.bbc.co.uk/bbcthree'

#######################
# BeautifulSoup setup #
#######################

# query the website and return the html to the variable page
request = requests.get(three_page)
# print(request.encoding)
page = request.text

# parse the html using beautiful soup and store in variable `soup`
# soup = BeautifulSoup(page, 'html.parser')
soup = BeautifulSoup(page, 'lxml')

########################
# initialise variables #
########################

urls = []
titles = []
guids = []


##########################
# extract promo elements #
##########################


    

hero_list = soup.findAll('a', attrs={'class': 'Hero Hero--primary'})
heroitems = len(hero_list)

if heroitems > 0:
    
    for hero in hero_list:

    # extract href contents
        url = hero['href']
        titlesRaw = hero.findAll('h3', text=True)

        # clean up h3 element to leave only heading
        for title in titlesRaw:
            title = title.text.strip()  # strip() is used to remove starting and trailing
            title = re.sub(u"(\u2018|\u2019)", "'", title)
            titles.append(title)

        # for the bits we've found, append them to the two empty lists
        if 'bbcthree/article' in url:
            urls.append(url)
            guids.append(url)
        else:
            pass
else:
    pass
    


subhero_list = soup.findAll('a', attrs={'class': 'Hero'})
subheroitems = len(subhero_list)

if subheroitems > 0:
    
    for hero in subhero_list:

    # extract href contents
        url = hero['href']
        titlesRaw = hero.findAll('h3', text=True)

        # clean up h3 element to leave only heading
        for title in titlesRaw:
            title = title.text.strip()  # strip() is used to remove starting and trailing
            title = re.sub(u"(\u2018|\u2019)", "'", title)
            titles.append(title)

        # for the bits we've found, append them to the two empty lists
        if 'bbcthree/article' in url:
            urls.append(url)
            guids.append(url)
        else:
            pass
else:
    pass




promo_list = soup.findAll('a', attrs={'class': 'Promo--long-article'})
for promo in promo_list:

    # extract href contents
    url = promo['href']
    titlesRaw = promo.findAll('h3', text=True)

    # clean up h3 element to leave only heading
    for title in titlesRaw:
        title = title.text.strip()  # strip() is used to remove starting and trailing
        title = re.sub(u"(\u2018|\u2019)", "'", title)
        titles.append(title)

    # for the bits we've found, append them to the two empty lists
    urls.append(url)
    guids.append(url)



#%% 

### Define process to remove tags in article text

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)



### Lists to be populated by second scrape

article_texts = []
article_descriptions = []
article_author = []
article_date = []
images = []


#sample_url = [urls[0], urls[1]]
#for page in sample_url:

# Scrape URLs to pull out additional details required for Feed

for page in urls:    
    request_article = requests.get(page)
    article_page = request_article.text
    # parse the html using beautiful soup and store in variable `soup`
    soup_article = BeautifulSoup(article_page, 'lxml')    
    promo_list = soup_article.findAll('div', attrs={'class': 'Text gel-body-copy'})
    
    try:
        author = soup_article.find(class_="Info-authorName gel-long-primer").get_text()
    except:
        author = 'BBC Three'
    publish_time = soup_article.find('time',datetime=True)['datetime']
    publish_time = str(publish_time)[:19]
#    publish_time = publish_time.replace("T"," ")
    publish_time += " GMT"


    img_list = promo.findAll('div', attrs={'class': 'ImageContainer gs-o-responsive-image gs-o-responsive-image--16by9'})
    
    for img in img_list:
        w = img.find('img',src=True)['src']
        images.append(w)

    
    new_description = soup_article.find(class_="LongArticle-synopsis gel-double-pica").get_text()
    text = ""
    description = ""
    count = 0
    for x in promo_list:
        try:
            z = len(x.find('p').contents)
            for w in range(z):
                y = x.find('p').contents[w]
                text = text + str(y)          
            if count == 0:
                description += str(y)
                #print (description)
            else: 
                pass            
            count += 1

        except:
            pass
    cleantext = remove_tags(text)
    article_texts.append(cleantext)
    cleandescription = remove_tags(description)
    article_descriptions.append(new_description)
    article_author.append(author)
    article_date.append(publish_time)


### Build the RSS Feed

makeRSS = True  # unset if testing

if makeRSS:

    feed = RSS2Feed(
    title=channelTitle,
    link=channelLink,
    description=channelDescription
    )

    for Title, Link, Desc, Author, Image, PubDate, Guid in zip(titles, urls, article_descriptions, article_author, images, article_date, guids):
        feed.append_item(
        title=Title,
        link=Link,
        description=Desc,
        author=Author,
        image=Image,
        pub_date = PubDate,
        guid = Guid)


    x = feed.get_xml()
    file = open("bbc-three-rss-test8.xml", "wb")
    file.write(x)
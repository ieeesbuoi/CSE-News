# -*- coding: utf-8 -*-
from __future__ import print_function
import urllib
from bs4 import BeautifulSoup
import HTMLParser
import re
import sys
import generate_xml as xml
import generate_html as html


# function: find_new_posts()
# ARGUMENTS: None
# DESCRIPTION:
#   Collects news from all the pages
def find_new_posts():
    # current page of posts
    page = 1

    print("Searching for available pages...")
    urls = get_page_urls(page)    # get urls starting with index page
    print ("Found " + str(len(urls)) + " pages!")

    # while news page exists
    print("Collecting data...")
    data = [[]]
    for url in urls:
        print (str(page) + "/" + str(len(urls)), end='\r')
        sys.stdout.flush()
        new_data = find_page_posts(url)             # find all posts/news of that page
        for announcement in new_data:
            data.append(announcement)

        page += 1                                    # go to the next page
    print("Data fetched succesfully!")


    #######################################
    # clean data
    # save to html and xml
    # show some analytics
    no = 0
    for dt in data:
        if (not dt):
            data.remove(dt)
        else:
            no += 1
    print ("Announcements found: " + str(no))

    html.generate_html(data)
    xml.generate_xml(data)


    return


# function: get_page_url(page)
# ARGUMENTS: 'Integer page_index'
# DESCRIPTION:
#   Given a page number checks if that page exists and returns all next page urls
#   else returns empty array
def get_page_urls(page):
    urls = []
    while (True):
    #base url: http://cs.uoi.gr/en/index.php?menu=m5&page=1
        url = "http://cs.uoi.gr/en/index.php?menu=m5&page=" + str(page)
        soup = BeautifulSoup(urllib.urlopen(url).read(), "html.parser")
        posts = soup.find_all('div', class_ = 'newPaging')
        if (posts):
            urls.append(url)
            page += 1
        else:
            return urls


# function find_page_posts(url):
# ARGUMENTS: 'String url_of_page'
# DESCRIPTION:
#   Finds and prints all news of the given page
def find_page_posts(url):
    # get html for current page's url
    html = urllib.urlopen(url).read()

    # convert html to BeautifulSoup element for further processing
    soup = BeautifulSoup(html, "html.parser")

    # find all <div class"newPaging"> elements. Those elements contain post info.
    posts = soup.find_all('div', class_ = 'newPaging')

    # store announcements data in array
    # data[0] = url
    # data[1] = date
    # data[2] = title
    # data[3] = id
    data = [[]]

    for post in posts:
        # find links for all the news
        links = post.find_all('a')
        link = links[0]['href']

        # get text of the post and fix it's encoding
        post_text = post.text.encode('utf-8').lstrip()
        # remove double spaces
        post_text = " ".join(post_text.split()).split("-")


        news_link = link
        news_date = post_text[0]
        news_title = post_text[1]
        news_id = int(link.split("=")[-1])


        data.append([news_link, news_date, news_title, news_id])
    return data


if __name__ == '__main__':
    find_new_posts()


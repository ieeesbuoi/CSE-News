# -*- coding: utf-8 -*-git config --global user.email "you@example.com"
import modules



try:
    from tqdm import tqdm,trange
except:
    modules.install("git+https://github.com/tqdm/tqdm.git@master#egg=tqdm")



import urllib

try:
    from bs4 import BeautifulSoup
except:
    modules.install("beautifulsoup4")

import HTMLParser
import re

# function: find_new_posts()
# ARGUMENTS: None
# DESCRIPTION:
#   Collects news from all the pages
def find_new_posts(base_url,xml_file):
    # current page of posts
    page = 1

    print("Searching for available pages...")
    urls = get_page_urls(base_url,page)    # get urls starting with index page
    print("Found " + str(len(urls)) + " pages!")

    # while news page exists
    xml_file = open(xml_file, "w")
    xml_file.write("<announcements>")

    print("Collecting data...")
    for url_i in trange(len(urls)):
        url=urls[url_i]
        #print page, "/", len(urls)
        find_page_posts(url, xml_file)    # find all posts/news of that page
        page += 1               # go to the next page
    xml_file.write("</announcements>")
    xml_file.close()
    print("Data fetched succesfully!")
    return


# function: get_page_url(page)
# ARGUMENTS: 'Integer page_index'
# DESCRIPTION:
#   Given a page number checks if that page exists and returns all next page urls
#   else returns empty array
def get_page_urls(base_url,page):
    urls = []
    while (True):
    #base url: http://cs.uoi.gr/en/index.php?menu=m5&page=1
        url = base_url + str(page)
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
def find_page_posts(url, xml_file):
    # get html for current page's url
    html = urllib.urlopen(url).read()

    # convert html to BeautifulSoup element for further processing
    soup = BeautifulSoup(html, "html.parser")

    # find all <div class"newPaging"> elements. Those elements contain post info.
    posts = soup.find_all('div', class_ = 'newPaging')
    xml = ""
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

        save_to_xml(news_link, news_date, news_title, str(news_id), xml_file)
    return


def save_to_xml(url, date, title, id, xml_file):
    xml_file.write("<announcement>")
    xml_file.write("<url>")
    url = url.replace("&", "&amp;")
    xml_file.write(url)
    xml_file.write("</url>")

    xml_file.write("<date>")
    xml_file.write(date)
    xml_file.write("</date>")

    title = title.replace("&", "&amp;")
    xml_file.write("<title>")
    xml_file.write(title)
    xml_file.write("</title>")

    xml_file.write("<id>")
    xml_file.write(id)
    xml_file.write("</id>")
    xml_file.write("</announcement>\n")

if __name__ == '__main__':
    find_new_posts("http://cs.uoi.gr/en/index.php?menu=m5&page=","announcements.xml")

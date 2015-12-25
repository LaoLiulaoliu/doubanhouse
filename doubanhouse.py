#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuande Liu <miraclecome (at) gmail.com>

from __future__ import print_function, division
import time
import sqlite3
import requests
import lxml.html

SEED = 'http://www.douban.com/group/shanghaizufang/discussion?start={}'
INTERVAL = 25
CONN = sqlite3.connect('hourse/douban.db')
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Host': 'www.douban.com',
    'Upgrade-Insecure-Requests': 1,
}

def crawl(url):
    ret = requests.get(url, headers=HEADER)
    html = lxml.html.fromstring(ret.content)
    return html


def parse(html):
    for item in html.cssselect('tr td.title'):
        author = item.getnext().cssselect('a')[0]
        link = author.get('href')
        author_id = link[link.find('people/')+7:].strip('/')
        author_name = author.text_content().strip().encode('utf-8')
        href = item.cssselect('a')[0]
        title = href.get('title').encode('utf-8')
        link = href.get('href').encode('utf-8')
        post_id = link[link.find('topic/')+6:].strip('/')

        to_db(author_id, author_name, post_id, title, link)


def to_db(author_id, author_name, post_id, title, link):
    if author_name.find("'") != -1:
        author_name = author_name.replace("'", "\\'")

    c = CONN.cursor()
    person_sql = 'insert into sh_person (id, name) select "{}", "{}" where not exists (select 1 from sh_person where id="{}");'.format(author_id, author_name, author_id)
    print(person_sql)
    c.execute(person_sql)
    post_sql = "insert into sh_post (id, title, link, person_id) select {}, '{}', '{}', '{}' where not exists (select 1 from sh_post where id={});".format(post_id, title, link, author_id, post_id)
    print(post_sql)
    c.execute(post_sql)
    CONN.commit()


def control(first=False):
    pages = 50 if first is True else 7
    num = 0
    while num <= INTERVAL * pages:
        url = SEED.format(num)
        html = crawl(url)
        parse(html)
        num += 25
        time.sleep(10)

def run():
    control(first=True)
    while True:
        control()
        time.sleep(500)
    CONN.close()

if __name__ == '__main__':
    run()

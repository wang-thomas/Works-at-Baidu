#coding=utf-8

import re
import urllib

overall_link = "http://zxhb.com/xuetang/7-1-1"


def read_single_page(l1, l2, url, act_output):
    page = urllib.urlopen(url).read()
    init_list = re.findall('<ul id="item-list">.+<span>标签：', page, re.DOTALL)
    art_list = re.findall('<li><a href="/\w+/\d+" title="[^"]+"', init_list[0])

    for art in art_list:
        link = "http://zxhb.com" + art[art.index("href=") + 6: art.index("\" title")]
        title = art[art.index("title=\"") + 7: len(art) - 1]

        content_page = urllib.urlopen(link).read()
        words_list = re.findall('<div class="words">\s+.+', content_page)

        if len(words_list) == 0:
            act_output.write(l1 + "\t" + l2 + "\t" + title + "\t" + link + "\t" + "\n")
        else:
            sec_content = re.sub(r'<[^>]+>', '', words_list[0])
            third_content = re.sub(r'\s', '', sec_content)
            content = re.sub(r'&nbsp.|&emsp.', '', third_content)

            #print (l1 + "\t" + l2 + "\t" + title + "\t" + link + "\t" + content + "\n")
            act_output.write(l1 + "\t" + l2 + "\t" + title + "\t" + link + "\t" + content + "\n")


def read_all_cats(url, act_output):
    page = urllib.urlopen(url).read()
    init_list = re.findall('<li><h4><strong>.+', page)
    all_cats = re.findall('<li><h4><strong><a href="/xuetang/\d+-\d+-\d+">[^<]+</a>|'
                          '<a href="/xuetang/\d+-\d+-\d+">[^<]+</a>', init_list[0])
    l1 = ""
    for cat in all_cats:
        if '<li>' in cat:
            l1 = cat[cat.index("\">") + 2: cat.index("</a>")]

        else:
            l2 = cat[cat.index("\">") + 2: cat.index("</a>")]
            link = "http://zxhb.com" + cat[cat.index("href=") + 6: cat.index("\">")]
            read_single_page(l1, l2, link, act_output)


with open("xuetang_info", "w") as text_file:
    #read_single_page("装修前", "房产知识", overall_link, text_file)
    read_all_cats(overall_link, text_file)


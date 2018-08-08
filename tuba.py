#coding=utf-8

import re
import urllib

overall_link = "https://www.to8to.com/yezhu/fangchan/"


def read_single_page(l1, l2, url, act_output): #reads a single page and all its articles and content of each
    page = urllib.urlopen(url).read()
    init_list = re.findall('list-item-title.+', page)

    for i in range(len(init_list)):
        item = init_list[i]
        link = item[item.index("href=") + 6: item.index(".html") + 5]
        title = item[item.index("html") + 6: item.index("</a>")]

        #get the content of each article
        content_page = urllib.urlopen(link).read()
        pre_content = re.findall('<div class="yezhu-zxcs-content">.*<div class="yezhu-detail-praise">',
                                 content_page, re.DOTALL)
        if len(pre_content) == 0:
            act_output.write(l1 + "\t" + l2 + "\t" + title + "\t" + link + "\t" + "\n")
        else:
            sec_content = re.sub(r'<[^>]+>', '', pre_content[0])
            third_content = re.sub(r'\s', '', sec_content)
            content = re.sub(r'&nbsp.', '', third_content)

            act_output.write(l1 + "\t" + l2 + "\t" + title + "\t" + link + "\t" + content + "\n")


def read_all_pages(l1, l2, url, act_output):
    page = urllib.urlopen(url).read()
    init_list = re.findall('<div class="pages-box">.+', page)
    pages_list = re.findall('/yezhu/\w+/list_\d+.html', init_list[0])

    root = pages_list[0][0: pages_list[0].index("_") + 1]
    total_num = re.findall('\d+', pages_list[len(pages_list) - 2])
    num = int(total_num[0])

    read_single_page(l1, l2, url, act_output)
    for i in range(2, num + 1):
        read_single_page(l1, l2, "https://www.to8to.com" + root + str(i) + ".html", act_output)


def read_all_cats(url, act_output):
    page = urllib.urlopen(url).read()
    init_list = re.findall('<div class="selection-arrow"></div>.+\n.+', page)

    for i in range(len(init_list)):
        item = init_list[i]
        result = item[item.index("/yezhu"): item.index("/\">") + 1]
        l2 = item[item.index("/\">") + 3: item.index("</a>")]
        cat_link = "https://www.to8to.com" + result
        if i <= 4:
            read_all_pages("装修前", l2, cat_link, act_output)
        elif i <= 12:
            read_all_pages("装修中", l2, cat_link, act_output)
        else:
            read_all_pages("装修后", l2, cat_link, act_output)


with open("lastRuzhu.txt", "w") as text_file:
    # read_all_cats(overall_link, text_file)
    read_all_pages("装修后", "入住", "https://www.to8to.com/yezhu/ruzhu/", text_file)


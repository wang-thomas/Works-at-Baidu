#coding=utf-8

import re
import urllib

over_all_link = "http://baike.yangche51.com/zhenduanweixiu/"
over_all_output = "故障维修.txt"

url_file = urllib.urlopen(over_all_link).read()

pattern = re.compile(r'<p><a rel="nofollow" href="http://baike.yangche51.com/catagory/\d+.html">更多.+')

selected_titles_links = pattern.findall(url_file) #a list of strings of big titles

output = open(over_all_output, "w")


def read_single_page(url):
    page_info = urllib.urlopen(url).read()
    art_pattern = re.compile(r'<dt><div><a href="http://baike.yangche51.com/article/\d+.html"><h2>.+')
    selected_articles = art_pattern.findall(page_info)

    # get the small titles on one page
    for art in selected_articles:
        art_name = art[art.index("<h2>") + 4: art.index("</h2>")]
        output.write(art_name + "\t")


for title in selected_titles_links: #open each of the big title and read the initial info
    name = title[title.index(" >") + 2: title.index("<", title.index(" >"))]
    output.write("\n\n" + name + ": ")

    link = title[title.index("href=") + 6: title.index("\">")]
    new_page = urllib.urlopen(link).read() #the first page of articles

    #get page numbers and loop into each page
    pn_pattern = re.compile(r'<hr/><div id=\'rptArtilce\'class=\'pageNav\'>&nbsp;.+') #line of pns
    pn = pn_pattern.findall(new_page)
    pn_list = re.findall("/catagory/\d+_\d+\.html", pn[0]) #pn links

    cat_num = pn_list[0][pn_list[0].index("/", 1) + 1: pn_list[0].index("_")]
    second_to_last = pn_list[len(pn_list) - 2]
    total_num = int(second_to_last[second_to_last.index("_") + 1: second_to_last.index(".")])

    read_single_page(link)
    for i in range(2, total_num + 1):
        read_single_page("http://baike.yangche51.com/catagory/" + cat_num + "_" + str(i) + ".html")

output.close()

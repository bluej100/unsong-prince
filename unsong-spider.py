#!/usr/bin/python
import sys, time, os, random, re, urllib2

titlere = re.compile('<h1.*?>(.*?)</h1>', re.DOTALL);
contentre = re.compile('<div class="pjgm-postcontent">(.*?)<div class="sharedaddy', re.DOTALL);
nextre = re.compile('<div class="pjgm-navnex"><a href="(.*?)" rel="next"', re.DOTALL);
url = "http://unsongbook.com/prologue-2/"
i = 1

while url:
    print url
    request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    response = urllib2.urlopen(request)
    html = response.read()

    title = titlere.search(html).group(1)
    content = contentre.search(html).group(1)
    path = "chapters/%03d.html" % i
    f = open(path, 'w')
    f.write('<h2 id="'+str(i)+'">'+title+'</h2>')
    f.write(content)
    f.close()
    print path

    nextsearch = nextre.search(html)
    url = nextsearch and nextsearch.group(1)
    i += 1

    time.sleep(1+3*random.random())

print 'done'

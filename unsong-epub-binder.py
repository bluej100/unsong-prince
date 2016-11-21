#!/usr/bin/python
import os, zipfile, glob
from bs4 import BeautifulSoup

epub = zipfile.ZipFile('output/unsong.epub', 'w')

# The first file must be named "mimetype"
epub.writestr("mimetype", "application/epub+zip")

# We need an index file, that lists all other HTML files
# This index file itself is referenced in the META_INF/container.xml
# file
epub.writestr("META-INF/container.xml", '''<container version="1.0"
           xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>''');

# The index file is another XML file, living per convention
# in OEBPS/Content.xml
index_tpl = '''<package version="2.0"
  unique-identifier="bookid"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns="http://www.idpf.org/2007/opf">
  <metadata>
    <dc:title>Unsong</dc:title>
    <dc:creator>Scott Alexander</dc:creator>
    <dc:publisher>Scott Alexander</dc:publisher>
    <dc:date>2016</dc:date>
    <dc:language>en</dc:language>
    <dc:identifier id="bookid">http://unsongbook.com/</dc:identifier>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
    %(manifest)s
  </manifest>
  <spine toc="ncx">
    %(spine)s
  </spine>
</package>'''

# OEBPS/toc.ncx
toc_tpl = '''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
                 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid"
content="urn:uuid:77a19404-c4cc-43d9-9652-284184825e9e"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>Unsong</text>
  </docTitle>
  <navMap>
    %(navmap)s
  </navMap>
</ncx>
'''

manifest = ""
spine = ""
navmap = ""

for i, chapter in enumerate(sorted(glob.glob('chapters/*.html'))):
    basename = os.path.basename(chapter)

    soup = BeautifulSoup(open(chapter), "lxml", from_encoding="UTF-8")
    soup.html['xmlns'] = 'http://www.w3.org/1999/xhtml'
    h2 = soup.h2
    del h2['id']
    chapter_title = h2.string.encode("UTF-8")
    head = soup.new_tag("head")
    title = soup.new_tag("title")
    title.append(chapter_title)
    head.append(title)
    soup.html.insert(0, head)
    for font in soup.find_all('font'):
        font.unwrap()
    epub.writestr('OEBPS/'+basename, soup.prettify().encode("UTF-8"))

    manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (
                  i+1, basename)
    spine += '<itemref idref="file_%s" />' % (i+1)
    navmap += '''<navPoint id="navpoint-%s" playOrder="%s">
      <navLabel>
        <text>%s</text>
      </navLabel>
      <content src="%s"/>
    </navPoint>
''' % (i+1, i+1, chapter_title, basename)

# Write the toc
epub.writestr('OEBPS/toc.ncx', toc_tpl % {
  'navmap': navmap,
})

# Finally, write the index
epub.writestr('OEBPS/Content.opf', index_tpl % {
  'manifest': manifest,
  'spine': spine,
})

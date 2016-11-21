#!/usr/bin/python
import sys, os, glob

f = open('output/unsong.html', 'w')
f.write(open('unsong-header.html', 'r').read())

for chapter in sorted(glob.glob('chapters/*.html')):
    f.write('<article>')
    f.write(open(chapter).read())
    f.write('</article>')

f.write(open('unsong-footer.html', 'r').read())

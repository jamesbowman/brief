#!/usr/bin/env python
import sys
from string import Template
import hashlib
import time

import feedparser

DEFAULT_TEMPLATE = Template(u"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>NEWS</title>
    <style type="text/css">
    body {
        margin:40px auto;
        max-width:650px;
        line-height:1.6;
        font-size:18px;
        color:#000;
        padding:0 10px }
    .subhead { font-size:14px; }
    .toc { font-size:17px; line-height:1.0; }
    1,h2,h3{line-height:1.2}
    </style>
  </head>
  <body>
    <p class="subhead">${time}</p>
    ${tocs}
    ${arts}
  </body>
</html>
""")

FEED_TEMPLATE = Template(u"""\
    <div class="feed">
      <h1><a href="${link}">${title}</a></h1>
      <div class="toc">${toc}</div>
    </div>
""")

DIR_TEMPLATE = Template(u"""\
  <p><a href="#${hash}">${title}</a></p>
""")

ENTRY_TEMPLATE = Template(u"""\
<a name="${hash}"></a>
<hr>
<div class="entry">
  <h2>${title}</h2>
  <p class="subhead">By ${author} on ${published} <a href="${link}">link</a></p>
  <div class="entrybody">${content}</div>
</div>
""")

def entry(e):
    if hasattr(e, 'content'):
        content = e.content[0].value
    elif hasattr(e, 'summary'):
        content = e.summary
    else:
        content = ""
    ee = {
        'link' : e.link,
        'hash' : hashlib.sha1(e.link).hexdigest(),
        'title' : e.title,
        'published' : e.get('published', '?'),
        'author' : e.get('author', '?'),
        'content' : content,
    }
    return (DIR_TEMPLATE.substitute(ee), ENTRY_TEMPLATE.substitute(ee))

def feed(rssd):
    d = feedparser.parse(rssd)
    title = d['feed'].get('title', 'NO TITLE')
    link = d['feed'].get('link', '')
    converted = [entry(e) for e in d.entries[:10]]
    toc = "".join([d for (d,e) in converted])
    articles = "".join([e for (d,e) in converted])
    return (FEED_TEMPLATE.substitute(locals()), articles)

    for e in d.entries:
        # print e.title
        # print e.content[0].value
        pass
    
def makepaper(rsses):
    for rss in rsses:
        d = feedparser.parse(rss)
        print d['feed']['title']

if __name__ == '__main__':
    out = open("index.html", "w")
    # feeds = [feed(open(f).read()) for f in ("frozen1", "frozen2")]
    feeds = [feed(r) for r in sys.argv[1:]]
    time = time.strftime("%c")
    tocs = "".join([t for (t,a) in feeds])
    arts = "".join([a for (t,a) in feeds])
    out.write(DEFAULT_TEMPLATE.substitute(locals()).encode('utf-8'))
    out.close()

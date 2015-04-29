---
title:  "Wikipedia to Plain Text"
authors: [ben]
tags: mddn442 mediawiki xml
image:
---

Before we can do any text analysis on Wikipedia, we need to pull articles out of the exported files, and then deal with the markup that gives them their formatting and structure.

Articles exported from Wikipedia (the 45GiB dump of English Wikipedia, as well as individual article exports like [this](https://en.wikipedia.org/wiki/Special:Export/Roman_Britain)) are XML documents, with page title and some other metadata as XML tags, and then the page body all in one XML tag. The body consists of [MediaWiki markup](https://www.mediawiki.org/wiki/Markup_spec).

Getting the wikitext out of the XML is easy; my favourite library for getting things out of XML and HTML [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) is more than a match for this (did I mention I'm developing this in Python?). Next we must parse the wikitext itself, in order to deal with links, templates, bold, italics, bulleted lists, numbered lists, headings, HTML entities etc. However, MediaWiki markup has no formal specification or grammar description, and thus is rather hard to parse corectly. Enter the [MediaWiki Parser from Hell](https://github.com/earwig/mwparserfromhell/).

With the structure of the wikitext parsed, we then have to remove unwanted elements, before flattening into plain text. We identify sections with headings like _References_, _Popular Culture_, _In Fiction_ etc. and remove them, because they are either unwanted noise or plain fiction (and while interesting, a fictional history of the world is not what we're here for). File and image links are removed altogether, as are `<ref>` and `<br>` HTML tags. A function of the parser is then used to produce plain text by removing templates, squashing links and headings, converting HTML entities like `&amp;` to text and so on.

Now, we can do some analysis.

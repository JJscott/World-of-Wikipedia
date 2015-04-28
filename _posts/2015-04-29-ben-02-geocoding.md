---
title:  "Extracting Locations"
authors: [ben]
tags: mddn442 geocoding perl
image:
---

Our orginal intention was to use article with geotags as seen [here](https://en.wikipedia.org/wiki/Lincoln_Memorial) to get a location for an article as a whole, and then to try and extract date-based events from such articles. Then Josh found [this](http://www.dlib.org/dlib/september12/leetaru/09leetaru.html) paper, which details a procedure they call _full text geocoding_: searching plain text for references to locations listed in gazetteers, which then give latitude and longitude. As we had realized that many articles, even those describing a relatively specific location, did not have geotags, I wanted to give this a go.

I didn't want to implement it from scratch though. Fortunately, I was able to find the implementation that was built for that paper, in the [CyberGIS Toolkit](http://cybergis.cigi.uiuc.edu/cyberGISwiki/doku.php/ct/spatialtext).

## Modifications

I ended up having to make quite a few modifications to the internals of the geocoder (and possibly fix a few bugs) to get it to produce the output I required. As the geocoder is written in Perl (a language that I did not know prior to this project, and would like to forget as quickly as possible) this was not an easy task. Complicating matters were a profusion of global variables and some of the worst code indenting I have ever seen. At least it _was_ commented, but not to the degree that would make maintenance easy.

I made the geocoder spit out XML consisting of tags like this:

{% highlight xml %}
<match>
	<feature>
		<type>5</type>
		<id>-2601889</id>
		<name>london</name>
		<cc>UK</cc>
		<ccname>United Kingdom</ccname>
		<adm1>H9</adm1>
		<adm1name>London, City of</adm1name>
		<lat>51.5</lat>
		<long>-0.116667</long>
	</feature>
	<position>7797</position>
	<position>7869</position>
	<position>14587</position>
	<position>18008</position>
	<text>london</text>
</match>
{% endhighlight %}

## Subprocessing

My analysis is primarily running in Python, but the geocoder is in Perl. On top of this, the geocoder has a significant startup time (~5s) as it needs to load multiple gazatteers and other databases into memory. In order to call the geocoder from Python while minimizing overhead, I start the geocoder as a subprocess. The Python code takes text to be geocoded, writes it to a temporary file, and writes that file's name to the geocoder's stdin. The geocoder reads the file, processes it, writes the resulting XML to another temporary file, and writes that file's name to stdout. The Python code (which has been patiently waiting) reads and returns the contents, and deletes the temporary files. Hacky much?

## Results

At this point, we can run the geocoder on plain-text-ified Wikipedia articles and get the latitiude and longitude of every location match, as well as the position in the text of the match itself. These positions are important, as we will need to associate location matches with date matches to get _events_. There is a catch though: The geocoder, as part of its workings, does a significant amount of mangling of the input text before actually finding matches. As such, the reported positions are relative to the _mangled text_. We'll get back to this later.

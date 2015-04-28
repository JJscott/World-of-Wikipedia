---
title:  "Introducing: HorribleMarkup™"
authors: [ben]
tags: mddn442
image:
---

Do _you_ need a markup language that can survive the most arduous text mangling? One that is impervious to losing angle brackets? One that cares not for quote marks? One that eats indentation for breakfast? One that refuses to believe in curly braces? Introducing... HorribleMarkup™!

## Mangling

If you recall from [a while ago](ben-02-geocoding.html), the geocoder mangles its input before processing. The nature of the mangling is that all punctuation is removed or replaced, spacing is normalized, some abbreviations are expanded and casing is fiddled with to suit the internals.

This is an excerpt from [Lincoln Memorial](https://en.wikipedia.org/wiki/Lincoln_Memorial) before mangling:

> The Lincoln Memorial is an American national monument built to honor the 16th President of the United States, Abraham Lincoln. It is located on the western end of the National Mall in Washington, D.C., across from the Washington Monument. The architect was Henry Bacon; the designer of the primary statue – Abraham Lincoln, 1920 – was Daniel Chester French; the Lincoln statue was carved by the Piccirilli Brothers; [2] and the painter of the interior murals was Jules Guerin. Dedicated in 1922, it is one of several monuments built to honor an American president. It has always been a major tourist attraction and since the 1930s has been a symbolic center focused on race relations.

This is the same text after mangling:

> the Lincoln Memorial is an American national monument built to honor the 16th president Of The United States , Abraham Lincoln . It is located on the western end of the National Mall in Washington , District of Columbia , across from the Washington Monument . the architect was Henry Bacon . the designer of the primary statue . . . Abraham Lincoln , 1920 . . . was Daniel Chester French . the Lincoln statue was carved by the Piccirilli Brothers . . 2 . and the painter of the interior murals was Jules Guerin . Dedicated in 1922 , it is one of several monuments built to honor an American president . It has always been a major tourist attraction and since the 1930s has been a symbolic center focused on race relations .

Where am I going with this? I want to extract events. The structure of the wiki article (sections, indentation etc.) will be helpful for this. In order to use it, it is necessary to associate the mangled text with said structure. So, the structure must somehow _pass through_ the geocoder unharmed. However, the nature of the geocoder is such that "ordinary" markup languages (XML and friends) will be completely denatured. This is what HorribleMarkup™ (not really a trademark) is for.

## Markup

The only building blocks that HorribleMarkup™ has to work with are therefore plain alphanumeric strings, and case-insensitive ones too (in practice, the geocoder won't uppercase a string it doesn't recognize, so as long as we use lowercase, we're fine). We therefore need to encode structure as text that won't be misinterpreted as "real" text. We could choose simple tokens, and escape every instance of them in the text, but this disturbs the text proper, which we don't want to do. So, no escape sequences. 

This is an example of (an early version of) some HorribleMarkup™, from another part of the same article:

> 78-year-old Robert Todd Lincoln , was in attendance . . f2886e35d15d6fb3 . . 4574d2eb9f268fef . . f2886e35d15d6fb3 . the Memorial was listed on the National Register Of Historic Places On October 15 , 1966 . . f2886e35d15d6fb3 . . 4574d2eb9f268fef . . f2886e35d15d6fb3 . cecc793ea1625e8c Vandalism f2886e35d15d6fb3 . f2886e35d15d6fb3 . In September 1962 , vandals painted the words . nigger lover . in foot-high pink letters on the rear wall . . f2886e35d15d6fb3 . . 4574d2eb9f268fef . . f2886e35d15d6fb3 . On the morning of July 26 , 2013 , the memorial was shut down after the statue . base and legs were splashed with green paint . It reopened later that day . 58-year-old Chinese national , Jiamei Tian , was later found responsible for the vandalism . He was admitted to St . Elizabeths Hospital , a psychiatric facility , and was later found to be incompetent to stand trial . . f2886e35d15d6fb3 . . 4574d2eb9f268fef . . f2886e35d15d6fb3 . 3a1b5459aeaf87a7 Exterior f2886e35d15d6fb3 . f2886e35d15d6fb3 . the exterior of the Memorial echoes a classic Greek temple and features Yule marble from Colorado . 

That's right: we use random strings as the "keywords" of HorribleMarkup™.

The basic keywords are:

{% highlight python %}

HEADING1 = 'a523d755f80babfb'
HEADING2 = '3a1b5459aeaf87a7'
HEADING3 = 'cecc793ea1625e8c'
HEADING4 = '7f0d292f971b8658'
HEADING5 = 'a82a80f351f92b4d'
HEADING6 = 'bb442fd465ce1d81'
NEWLINE  = 'f2886e35d15d6fb3'
NEWPARA  = '4574d2eb9f268fef'
INDENT   = 'e52f75bdc7d1828f'

{% endhighlight %}

These correspond to some of the basic elements of MediaWiki markup. Indeed, HorribleMarkup™ is produced by substituting elements of the parsed wikitext for HorribleMarkup™ keywords before flattening to plain text.

## Parser

Of course, I had to write a parser for HorribleMarkup™ too. It started out as reasonable code, but grew piecemeal as its requirements changed. It is now rather awful. The parser produces a tree structure, where only the leaves of the tree contain actual text. The leaves know what position in the text they were parsed from, so can be associated with location and date matches.



































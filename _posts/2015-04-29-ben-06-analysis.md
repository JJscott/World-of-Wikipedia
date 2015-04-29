---
title:  "Data Analysis"
authors: [ben]
tags: mddn442 grid
image: https://1.bp.blogspot.com/-EDiyDbUcXW4/UWbcO0dx5vI/AAAAAAAAAQs/MywdJ-IGxD8/s1600/grid-computing.jpg
---

We now have the means to analyse articles and produce a series of events from them. What remains is the logistics of running this analysis on what is a rather large dataset, Wikipedia.

## Batching

First, we need to cut the monolithic dump of all of English Wikipedia into smaller, usable, relevant pieces. I wrote a script that uses a SAX parser to read through the input (the only way to read such a large XML file), and re-writes the articles it encounters into multiple output files. It optionally tests article titles against a supplied regex before outputting them, so we can filter only a desired subset. It writes articles out to a file until a specified file size limit is reached, and then starts a new output file. However, reading through the entire 45GiB input takes quite a long time (hours, if writing out most articles) and is unfortunately a very serial task.

## Analysis

The analysis script itself runs on a batch of articles. It reads through the articles in its input, producing a shared list of all the events from those articles. It also takes the first location match from each article within some limit of the start of the article (2000 characters of marked-up, mangled text), if there was one, and records it as an approximate location for that article. The events list is sorted by date before being written to file. The events file is plain text with one line per event, but it is specially arranged such that each line is the same fixed size in bytes. This is to facilitate random access to, and searching in, events files. The article locations list is written as plain text without anything tricky.

As I forgot about it when doing the article batching, it became the analysis script's job to ignore pages outside the main Wikipedia article namespace (user pages, talk pages etc.).

## Small Dataset

Before going all the way, we analyse a small subset of the articles: those about individual years. Wikipedia has these from now back to at least AD 1 (and there are some for the future too). This subset of articles is only ~16MiB, and does not take very long to process (5-10 minutes). It yields 31,216 events. This dataset is the one we used in our presentation.

Here is an excerpt from the events file:

	174.0	-41.0	1853.61347032	August 12 – New Zealand acquires self-government.	new zealand	 August 12 	1853	____________________________________________________________________________________________________________________________________________________
	4.33333	50.8333	1853.64360731	August 23 – The first true International Meteorological Organization is established in Brussels, Belgium.	brussels	 August 23 	1853	___________________________________________________________________________________________
	-97.6475	31.106	1853.64360731	Death: August 23 – Alexander Calder, first mayor of Beaumont, Texas (b. 1806)	texas	 August 23 	1853	__________________________________________________________________________________________________________________________
	28.5	-29.5	1853.65730594	Birth: August 28 – Franz I, Prince of Liechtenstein,  (d. 1938)	liechtenstein	 August 28 	1853	_____________________________________________________________________________________________________________________________________
	105.0	35.0	1853.71598174	September 19 – Hudson Taylor first leaves for China.	china	 September 19 	1853	_____________________________________________________________________________________________________________________________________________________
	100.0	15.0	1853.71872146	Birth: September 20 – Chulalongkorn, Rama V, king of Thailand (d. 1910)	thailand	 September 20 	1853	_______________________________________________________________________________________________________________________________
	100.0	60.0	1853.75821918	October 4–5 – Crimean War: The Ottoman Empire starts war with Russia.	russia	 October 4 	1853	____________________________________________________________________________________________________________________________________
	-97.0	38.0	1853.75821918	October 4 – On the east coast of the United States, Donald McKay launches the Great Republic, the world's biggest sailing ship, which at 4,500 tons is too large to be successful.	united states	 October 4 	1853	__________________
	135.15	34.1833	1853.78287671	Death: October 13 – Jan Cock Blomhoff, Dutch director of Dejima, Japan (b. 1779)	dejima	 October 13 	1853	______________________________________________________________________________________________________________________
	117.177	39.1422	1853.82945205	October 30 – Taiping Rebellion: The Taiping Northern Expeditionary Force comes within three miles (5 km) of Tianjin.	tianjin	 October 30 	1853	_______________________________________________________________________________
	-6.24889	53.3331	1853.83219178	May 12–October 31 – Great Industrial Exhibition held in Dublin, Ireland.	dublin	 October 31 	1853	__________________________________________________________________________________________________________________________
	-8.0	39.5	1853.8716895	November 15 – Maria II of Portugal is succeeded by her son Pedro.	portugal	 November 15 	1853	________________________________________________________________________________________________________________________________________
	-8.0	39.5	1853.8716895	Death: November 15 – Maria II of Portugal (b. 1819)	portugal	 November 15 	1853	______________________________________________________________________________________________________________________________________________________
	-122.078	47.4626	1853.9303653	Birth: December 6 – Haraprasad Shastri, Indian academic, Sanskrit scholar, archivist and historian of Bengali literature (d. 1931)	indian	 December 6 	1853	___________________________________________________________________
	-97.0	38.0	1853.97694064	Birth: December 23 – William Henry Moody, 35th United States Secretary of the Navy, 45th United States Attorney General (d. 1917)	united states	 December 23 	1853	_________________________________________________________________
	-77.264	40.5773	1854.02191781	January 9 – The Teutonia Männerchor in Pittsburgh, Pennsylvania was founded.	pennsylvania	 January 9 	1854	___________________________________________________________________________________________________________________
	-97.6475	31.106	1854.11894977	February 14 – Texas is linked by telegraph with the rest of the United States, when a connection between New Orleans and Marshall, Texas is completed.	texas	 February 14 	1854	_______________________________________________
	24.0	-29.0	1854.12716895	February 17 – The British recognize the independence of the Orange Free State; its official independence is declared 6 days later.	orange free state	 February 17 	1854	____________________________________________________________
	27.2199	-30.2351	1854.16666667	March 1 – German psychologist Friedrich Eduard Beneke disappears; 2 years later his remains are found in the canal near Charlottenburg.	charlottenburg	 March 1 	1854	________________________________________________________
	150.735	-33.6466	1854.1803653	Death: March 6 – Charles William Vane, 3rd Marquess of Londonderry (b. 1778)	londonderry	 March 6 	1854	_______________________________________________________________________________________________________________________
	-2.0	54.0	1854.19406393	March 11 – A Royal Navy fleet sails from Britain under Vice Admiral Sir Charles Napier.	britain	 March 11 	1854	_____________________________________________________________________________________________________________________
	-81.717	27.8333	1854.21598174	Death: March 19 – William Pope Duval, first civilian governor of Florida Territory (b. 1784)	florida	 March 19 	1854	__________________________________________________________________________________________________________
	-71.0784	42.3493	1854.21872146	March 20 – The Boston Public Library opens to the public.	boston public library	 March 20 	1854	______________________________________________________________________________________________________________________________
	-66.0	8.0	1854.22968037	March 24 – In Venezuela, slavery was abolished	venezuela	 March 24 	1854	____________________________________________________________________________________________________________________________________________________________
	-75.0966	40.9232	1854.23789954	Death: William Bentinck, 4th Duke of Portland, politician (b. 1768)	portland	 March 27	1854	____________________________________________________________________________________________________________________________________
	-95.63	39.7617	1854.29109589	April 16 – The United States packet ship Powhattan is wrecked off the New Jersey shore with more than 200 + victims.	powhattan	 April 16 	1854	_________________________________________________________________________________
	-6.24889	53.3331	1854.37990868	May 18 – The Catholic University of Ireland (forerunner of University College Dublin) is founded.	dublin	 May 18 	1854	_______________________________________________________________________________________________________
	-97.6475	31.106	1854.39634703	Birth: May 24 – John Riley Banister, American law officer and Texas Ranger (d. 1918)	texas	 May 24 	1854	______________________________________________________________________________________________________________________
	-97.0	38.0	1854.40456621	May 27 – Taiping Rebellion: United States diplomatic minister Robert McLane arrives at the Heavenly Capital aboard the American warship USS Susquehanna.	united states	 May 27 	1854	_______________________________________________
	-92.5005	38.2503	1854.41278539	May 30 – The Kansas-Nebraska Act becomes law, replacing the Missouri Compromise (of 1820), thus act creating the Kansas Territory and the Nebraska Territory, west of the State of Missour...	state of missouri	 May 30 	1854	
	-98.2883	41.1289	1854.41278539	The Kansas-Nebraska Act also established that those two new Territories would decide either to allow or disallow slavery depending on balloting by their residents.	nebraska	 May 30 	1854	_____________________________________
	-92.5005	38.2503	1854.41278539	These areas would have been strictly "free territory" under the Missouri Compromise, which allowed slavery in the State of Missouri but disallowed it in any other new state north of the la...	state of missouri	 May 30 	1854	
	-76.483	38.9821	1854.4413242	June 10 – The first class of the United States Naval Academy graduated at Annapolis, Maryland.	united states naval academy	 June 10 	1854	______________________________________________________________________________________
	26.0	64.0	1854.47146119	June 21 – Battle of Bomarsund in the Åland Islands (which later became part of Finland - in 1920:) The Royal Navy seaman's mate Charles D. Lucas throws a live Russian artillery shell overboard by hand ...	finland	 June 21 	1854	
	-95.0	60.0	1854.48515982	Birth: June 26 – Robert Laird Borden, the eighth Prime Minister of Canada (d. 1937)	canada	 June 26 	1854	__________________________________________________________________________________________________________________________
	78.5833	25.4333	1854.5	March - unknown date – India : British East India Company annexes Jhansi using the Doctrine of lapse.	jhansi	 the Year 1854	1854	_____________________________________________________________________________________________________
	-87.6501	41.85	1854.5	June – The Grand Excursion takes prominent Eastern United States inhabitants from Chicago, Illinois to Rock Island, Illinois by railroad, then up the Mississippi River to St. Paul, Minnesota by steam...	chicago	 the Year 1854	1854	
	20.0	52.0	1854.5	Ignacy Lukasiewicz drills the world's first oil well in Poland, in Bóbrka near Krosno County.	poland	 the Year 1854	1854	____________________________________________________________________________________________________________________
	-72.9265	41.3112	1854.5	Professor Benjamin Silliman of Yale University is the first person to fractionate petroleum into its individual components by distillation.	yale university	 the Year 1854	1854	_______________________________________________________
	-76.7183	40.0632	1854.5	Manchester is granted city status.	manchester	 the Year 1854	1854	_____________________________________________________________________________________________________________________________________________________________________
	76.95	43.25	1854.5	A Russian fort is established at the present site of Almaty.	almaty	 the Year 1854	1854	____________________________________________________________________________________________________________________________________________________
	-72.7622	41.5834	1854.5	The Waterbury Clock Company is founded in Waterbury, Connecticut, the  predecessor of Timex Group USA in timepiece manufacturing.	connecticut	 the Year 1854	1854	_____________________________________________________________________
	77.0	20.0	1854.5	Wood's despatch is sent by Charles Wood, 1st Viscount Halifax to Lord Dalhousie, the then Governor General of India.	india	 the Year 1854	1854	_______________________________________________________________________________________________

The lines are tab-separated into columns. The columns are: longitude, latitude, numeric date, event description, location match text, date match text, article title, padding.

## Large Dataset

I cut the full set of articles into ~50MB batches, of which there are 881. Each batch takes about 20 minutes to analyse, which is, approximately, over 12 days of compute time for the whole lot. I didn't have the luxury of that much time, but I _did_ have the luxury of the ECS Grid, which allowed me to use ~100 machines in parallel to perform the analysis. As each batch of articles can be treated separately, the analysis is quite parallelizable and runs well on a grid setup, with a runtime of ~3 hours.

This results in 881 separate events files and location files, which need to be combined with their respective siblings.

Combining the location files can be done simply by concatenating them:

	cat ./events/* > events_all.txt

Combining the events files requires a bit more care, as the files are sorted and the result must be too. The approach I took here was to implement the merge step of merge sort. The input files are read a line at a time all together, those lines are sorted and the first one is writtten out. The file that line came from has another line read and we loop until <s>we</s> all files are exhausted.

The full events file is ~2.8GiB and contains 11,540,724 events.



















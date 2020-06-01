#### Please download the tools by downloading the .py files, not the whole repository!
#### Please don't do anything to the repository without asking me first via telegram!

# rmb
RMB archiving tool for NationStates

You should have a Python interpreter/IDE installed to use this.

This Python program uses the messages shard of the Region API to get messages from a region's RMB and save them in a (somewhat) neat format in a text file. The data saved are the post author, date and time, post ID, sequential post number (first post 1, etc), number and name of likes, whether the post is suppressed, self-deleted or mod deleted, and if suppressed, by whom, and of course the message content.

Steps to use:
1. Download the rmb.py file.
2. Run it by double-clicking, or (preferably) in your IDE.
3. Follow the instructions on the command window. When entering the file name, enter it with full path (using backslashes \ on Windows) and extension (.txt). You can skip entering the path if the file is saved in the same folder as the script (not necessarily the Python folder, please ignore what the script's message says for this).

Running may take some time depending on the size of your RMB. The output screen (console) will print out the number of messages done every 100 messages, so you can keep track. When the program ends, the output window may close on its own. Check your text file to see if the program worked successfully.

## Examples
```
--------------------------------------------------------------------------------
20657581: Post 1665 by vavax on 2016-08-04 at 22:42:33 GMT
Likes: 1(merni)

[quote=united_meme_alliance;20656723]NS logic at its finest[/quote]
Damnit Max Barry
```
where 20657581 is the post ID and 1665 is the sequential number of the post.
```
--------------------------------------------------------------------------------
19893583: Post 1246 by dragosi on 2016-06-21 at 06:54:32 GMT
Likes: 0()
self-deleted
Message deleted by author
```
```
--------------------------------------------------------------------------------
24078428: Post 7532 by please_stay_hydrated on 2017-02-24 at 22:59:44 GMT
Likes: 2(federal_southern_cities:calapsia)
moderator deleted
Message suppressed by a moderator
```
```
--------------------------------------------------------------------------------
26640002: Post 11630 by calapsia on 2017-08-04 at 23:03:49 GMT
Likes: 1(new_cheeseland)
suppressed by vavax
[quote=vavax;26631431]Which means I therefore also have positive 0 power.To be fair, this is a real thing that happened.[/quote]
HA. Got you there, dad! Negative zero doesn't exist, therefore neither does your power! :D
```

## Errors
If the script stops with an error (starting with "Traceback (most recent call last)" etc on the first line) and the last line of the error contains "invalid token" or something like that, please note the last post ID saved to the text file, start up the script again, enable advanced options, and enter a starting post ID about 100 or 1000 more than that one. (Post IDs are not sequential in a region, so you probably will not miss any posts or maybe a few at most. You may need to advance by a lot if your RMB was inactive at the time of that post.) This error may be caused due to an invalid (control) character in a certain post.

If the output contains ? or weird symbols in unexpected places, please just live with it. This and the above error are caused by inconsistent encoding in the API messages shard.

If you get any other error, or if these fixes don't work, please contact me via TG.


# endo
Simple endorsement checker for NationStates

This is just a simple Python script to check who isn't endorsing a delegate. It supports command-line arguments, so can be automated. It uses just 4 API queries, regardless of the size of the region. You can redirect the output to a text file using the command line, if you want.

syntax for command-line arguments:

    usage: endo.py [-h] [-r REGION] [-u USERAGENT]
    
    optional arguments:
      -h, --help            show this help message and exit
      -r REGION, --region REGION
                            Region name
      -u USERAGENT, --useragent USERAGENT
                            User agent

The script asks for input when run without sufficient CL arguments, as follows:
```
C:\Users\Admin>py .\Appdata\Local\Programs\Python\Python36\endo.py
Your useragent should have your email/NS name, as well as the purpose of this program (endo check). The mods need this info.
Enter your useragent : Merni : endo check
Enter your region name : The Labyrinth
```
Sample output:
```
C:\Users\Admin>py .\Appdata\Local\Programs\Python\Python36\endo.py -r "The Labyrinth" -u "Merni endo check"
Querying nations in region...
Querying WA members...
Finding intersection...
Querying delegate...
Querying delegate endorsements...
Finding difference...




===============WA Delegate endorsement report===============
Generated (begin) on:            2020-05-01 at 09:15:32 UTC
Region:                          The Labyrinth
WA Delegate:                     greater_victora
Nations:                         239
WA nations:                      67
WA Delegate endorsements:        38
WA nations not endorsing:        28
% of WA nations endorsing:       56.71641791044776
% of WA nations not endorsing:   41.7910447761194
Note: WA delegate not included in calculations
============================List============================
1       the_boris_isles
2       the_aro_homeland
3       darcov
4       doctriniumn
5       marj_al-hamam
6       drewask
7       wadiya_aladeen_the_third
8       con_ins_lallakerscak
9       shane_dawson_and_the_theorist_community
10      crusaders789
11      le_epico
12      veen_republic
13      antonieo
14      the_europea_commonwealth
15      borlotins
16      swizzleland
17      mekonn
18      fritzlands
19      nihil-land
20      neo-gallia
21      kiratic_sireion
22      1kish4jk
23      wulfingland
24      montelana
25      wheres_my_uncle
26      manchoo
27      limingia
28      anglands
Press Enter to close...

C:\Users\Admin>
```
# Todo
1. Add CL argument support to the RMB tool
2. Make exe files for both tools?

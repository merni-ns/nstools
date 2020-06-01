# endocheck
Simple endorsement checker for NationStates

This is just a simple Python script to check who isn't endorsing a delegate. It supports command-line arguments, so can be automated. It uses just 4 API queries, regardless of the size of the region.

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

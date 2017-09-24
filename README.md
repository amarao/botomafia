# botomafia
Simulator for automatic strategies for Mafia club game

# How to run
```
python botomafia/base.py
```
or
```
python botomafia/base.py 10
```

# Strategy guide
There are few types of strategies, which are distinct by
amount of information used.
* _0-strategies_ are allowed to use information available due to
their role (mafia know mafia members, sheriff knows players
it has checked, doctor knew if some player was healed and didn't
died at previos nigh). Every player takes it decision independently.
Normal citizens knew nothing except for turn, player list and number
of mafia/special roles left. Strategy is not allowed to have any kind of constants for selecting targets. Example of disallowed strategies: 'vote for first player', 'vote for last player'.
The single exception is mafia, which allowed to vote for the same person
at night (only!). To speedup simulation mafioso allowed to listen to 
`night_say` from other mafia, but that 'say' should be random too.
* _constant strategies_ allows to have constants in the algorithms.
Example: 'vote for the odd player', 'vote for the fist player', 'vote for the
last player'. Their are not allowed to count other players votes, listen
to talks and store history of players death.
* _1-strategies_ are allowed to count votes at each turn. No 'vote history' is
allowed, as well as players is not allowed to listen to each other (except
for mafia which is allowed to listen to select victim at mafia night turn.
Fist mafia may use day vote to made a decsigion, but not discussion is allowed
and other mafia is permitted just to follow first mafia decision).
* _vote-strategies_ are allowed to store vote history. All other limitation
is the same as for 1-strategy.
* _7-strategies_ are allowed to listen to other players. They are permitted
to store up to 7 facts on each player. Each fact is:
1) record of activity (if this record contains turn number, that is counted as 2 facts). Example: vote, death at specific turn, 'say' part. If 'say' part
contains some information about other player, that is counted as 'fact' for player been told about, and if source of information is preserved, this is
counted as additional fact.
2) 'color' (likehood of been some role), if there are few metrics to count,
each metric is separate fact. Those metrics may be constructed in any way,
but 'packing' is not allowed. Example of packing: instead of saving votes for
each turn, save a long integer, where bits are corresponding to vote at a given turn. (This is not allowed). Metric should be calcucated in such a way that it is not used as few facts later.
* local strategies allow to store unlimited amount of information but disallow
computations which are 'simulations' of other players
* global strategies allow this

## Communication restrictions
* For strageies up to 7-strategies it's not allowed to establish any kind of
private communications between players (except for mafia night talk) by
means of encryption, etc.
* Starting from 7 strategies this is allowed but it should happen through public
communication channel and other player are allowed to intercept encrypted message.

## Pre-run constants
All pre-run and algorithms in the code for Citizens and Citizens special roles (Sheriff, Doctor, etc) are available to mafia.

All pre-run constants and algorithms of mafia is available to citizens.

(The difference between them is that mafia can use night talk to modify them
without letting know them to citizens).

# Commits
If you sending pull requests to this projects or comminting you
licence those commits under the same licence as this project.

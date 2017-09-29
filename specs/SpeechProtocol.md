Speak
=====

Every role may 'say'.

When role 'say' it should return list of messages. Every message is
instance of one of the subclass of Message class (messages.py)


Listen
======
There are three ways to listen to other players speeches.

1. `listen (speech)`. Speech is instance of 'Say' subclass.
2. `listen_Say*(player_id, messages)`. Allow to react to all messages at
   specific moment. Examples: `listen_DaySay`, `listen_DayDefence`, `listen_NightMafiaSay` (only mafia will receive last one)
3. `listen_Message*(speech, message)`. Allow to listen to specific
   message types. `speech` allows to see `speech.speaker_id` and
   `speech.__class__`. It called for each message from speech. Examples:
   `listen_MyRole`, `listen_Trust`, `listen_Distrust`, `listen_KnowPlayerSide`,
   `listen_VoteAgainst`, `listen_WantToKill` (last one is reserved for mafia night
     negotiations, Civils and daily mafia should use 'VoteAgainst').

When speech is processed, it is sent only to one method. `listen` has highest
priority, then `listen_Say*`, then `listen_Message`. If no suitable methods
found, speech is discarded.


Message Structure
=================
Each message has own structure (attributes). Check `messages.py` for details.

class Message(object):
    pass


class MyRole(Message):
    'Announce my own role (specific or generic, like SpecialCivilRole)'
    def __init__(self, role):
        self.role = role


class Trust(Message):
    'Announce list of players whom I trust'
    def __init__(self, trust_list):
        self.trust_list = trust_list


class Distrust(Message):
    "Announce list of players whom I don't trust"
    def __init__(self, distrust_list):
        self.distrust_list = distrust_list


class KnowPlayersSide(Message):
    '''
        Announce list of players whom I knew their side.
        This message normally should be send by sheriff
        or anyone else trying to be sheriff.

        Under some conditions Doctor my have 100% reliable
        information on some civil players too
    '''
    def __init__(self, player_list, side):
        self.mafia_list = player_list
        self.side = side


class KnowRole(Message):
    '''
        Announce someone else's role.
    '''
    def __init__(self, player_id, role):
        self.player_id = player_id
        self.role = role


class VoteAgainst(Message):
    '''Declaration of future day voting'''
    def __init__(self, player_id):
        self.player_id = player_id


class WantToKill(Message):
    '''
        Declaration of intention to kill.
        Reserved for mafia night talk
    '''
    def __init__(self, player_id):
        self.player_id = player_id


class Event(object):
    pass


class NewDayNotice(Event):
    pass


class KillNotice(Event):
    'Notification on players been killed (at day & night)'
    def __init__(self, killing_side, kill_list):
        self.killing_side = killing_side
        self.kill_list = kill_list


class CheckResultNotice(Event):
    'Special Notice for Sheriff, results of night check'
    def __init__(self, player_id, side):
        self.player_id = player_id
        self.side = side


class DayVoteNotice(Event):
    'Both players vote and revote'
    def __init__(self, voter_id, victim_id):
        self.voter_id = voter_id
        self.victim_id = victim_id


class VoteResultNotice(Event):
    'Preliminary vote results (revoting is possible)'
    pass


class AutocatastropheVoteNotice(Event):
    'Results of votes on autocatastrophe'
    pass


class MafiaGreetingNotice(Event):
    '''
        special event send at the game start only to mafia
        members. Contain list of other mafia members
    '''
    def __init__(self, mafia_list):
        self.mafia = mafia_list


class Say(object):
    def __init__(self, speaker_id, messages):
        self.speaker_id = speaker_id
        self.messages = messages

    def __str__(self):
        return "%s %s %s" (
            self.speaker_id,
            self.__name__.lower(),
            ", ".join(self.messages)
        )


class DaySay(Say):
    pass


class DayDefence(Say):
    pass


class MafiaNightSay(Say):
    pass


class Notification(Say):
    def __init__(self, event):
        self.speaker_id = None
        self.messages = [event]

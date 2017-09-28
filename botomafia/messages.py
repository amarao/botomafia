class Message(object):
    pass


class MyRole(Message):
    def __init__(self, role):
        self.role = role


class Trust(Message):
    def __init__(self, trust_list):
        self.trust_list = trust_list


class Distrust(Message):
    def __init__(self, distrust_list):
        self.distrust_list = distrust_list


class KnowPlayersSide(Message):
    def __init__(self, player_list, side):
        self.mafia_list = player_list
        self.side = side


class KnowRole(Message):
    def __init__(self, player_id, role):
        self.player_id = player_id
        self.role = role


class VoteAgainst(Message):
    def __init__(self, player_id):
        self.player_id = player_id


class Kill(Message):
    def __init__(self, player_id):
        self.player_id = player_id


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

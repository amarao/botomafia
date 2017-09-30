import random


class Strategy(object):
    '''
        This strategy defines minimally playable
        bot behavior without intent to win,
        it just provides a minimal working protocol
    '''
    level = "none"

    def configure_role(self):
        pass

    def listen_NewDayNotice(self, speech, message):
        pass

    def day_say(self):
        pass

    def day_vote(self):
        pass

    def day_defence(self):
        pass

    def move_vote(self, player_id):
        return None

    def kill_many_players(self, kill_list):
        return random.choice([True, False])

    def get_kill_notice(self, initiator, player_id, role_type):
        pass

    def night_say(self):
        raise Exception("impossible")

    def night_vote(self):
        pass

    def check_player(self):
        pass

    def get_check_result(self, player, status):
        pass

    def heal(self):
        pass


class CivilStrategy(Strategy):
    pass


class SheriffStrategy(Strategy):
    pass


class DoctorStrategy(Strategy):
    pass


class MafiaStrategy(Strategy):
    pass

import random
import copy
import messages
from . import Strategy, MafiaStrategy, CivilStrategy
from . import DoctorStrategy, SheriffStrategy


class DefaultCivilStrategy(Strategy):
    pass


class MafiaZeroStrategy(MafiaStrategy):
    level = "zero"

    def configure_role(self):
        self.night_kill = None

    def day_vote(self):
        return random.choice(self.game.list_players(skip=self.mafia))

    def listen_MafiaGreetingNotice(self, speech, message):
        self.mafia = copy.copy(message.mafia)

    def night_say(self):
        if not self.night_kill:
            self.night_kill = random.choice(
                 self.game.list_players(skip=self.mafia)
            )
        assert type(self.night_kill) is str
        return [messages.WantToKill(self.night_kill)]

    def listen_WantToKill(self, speech, message):
        assert type(message.player_id) is str
        self.night_kill = message.player_id

    def night_vote(self):
        assert type(self.night_kill) is str
        return self.night_kill

    def listen_NewDayNotice(self, speech, message):
        self.night_kill = None


class CivilZeroStrategy(CivilStrategy):
    level = "zero"

    def day_vote(self):
        return random.choice(self.game.list_players(skip=self.name))


class SheriffZeroStrategy(SheriffStrategy):
    level = "zero"

    def configure_role(self):
        self.trusted = [self.name]
        self.known_mafia = []

    def check_player(self):
        candidates = self.game.list_players(
            skip=self.trusted + self.known_mafia
        )
        if not candidates:
            candidate = self.name
        else:
            candidate = random.choice(candidates)
        return candidate

    def get_kill_notice(self, player_id, initiator, role_type):
        if player_id in self.known_mafia:
            self.known_mafia.remove(player_id)

    def day_vote(self):
        if self.known_mafia:
            return random.choice(self.known_mafia)
        return random.choice(self.game.list_players(skip=self.trusted))

    def get_check_result(self, player_id, status):
        if status == self.game.Civil:
            self.trusted.append(player_id)
        elif status == self.game.Mafia:
            self.known_mafia.append(player_id)

    def kill_many_players(self, kill_list):
        for mafia in self.known_mafia:
            if mafia in kill_list:
                return True
        for player in kill_list:
            if player not in self.trusted:
                break
        else:
            return False
        return random.choice([True, False])


class DoctorZeroStrategy(DoctorStrategy):
    level = "zero"

    def configure_role(self):
        self.healed = False
        self.night_heal = None
        self.trusted = [self.name]

    def heal(self):
        status = self.game.get_status()
        candidates = []
        if status['turn'] == 1:
            candidates = self.game.list_players(skip=self.trusted)
        elif (status['alive'] - status['mafia']) <= len(self.trusted):
            candidates = copy.copy(self.trusted)
        else:
            candidates = self.game.list_players()
        if self.healed:
            candidates.remove(self.name)
        candidate = random.choice(candidates)
        if candidate == self.name:
            self.healed = True
        else:
            self.night_heal = candidate
        return candidate

    def day_vote(self):
        return random.choice(self.game.list_players(skip=self.trusted))

    def get_kill_notice(self, player_id, initiator, role_type):
        if player_id in self.trusted:
            self.trusted.remove(player_id)
        if (initiator is self.game.Mafia):
            if not player_id and self.night_heal:
                if self.night_heal not in self.trusted:
                    self.trusted.append(self.night_heal)
            self.night_heal = None

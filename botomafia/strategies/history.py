import strategies.default
import strategies.one
import copy
import messages
import random
import collections


class HistoryStrategy(strategies.default.CivilZeroStrategy):
    def listen_NewDayNotice(self, speech, message):
        start_trust_level = round(float(self.game.civil_count)/(self.game.total_players-1), 2)
        self.voting_history = {}
        for player in self.game.list_players(skip=[self.name]):
            if player not in self.trust_list.keys():
                self.trust_list[player] = start_trust_level
        print(self.trust_list)

    def day_vote(self):
        vote_list = []
        trust_level = 1
        for player in self.game.list_players(skip=self.trusted):
            if self.trust_list[player] < trust_level:
                vote_list = [player]
                trust_level = self.trust_list[player]
            elif self.trust_list[player] == trust_level:
                vote_list.append(player)
        return random.choice(vote_list)

    def listen_DayVoteNotice(self, voter, notice):
        trust_level = round(1.0/(self.game.total_players-1), 2)
        if notice.victim_id == self.name:
            self.trust_list[notice.voter_id] -= trust_level
        self.voting_history[notice.victim_id] = self.voting_history.get(notice.victim_id, []) + [notice.voter_id]


class CivilHistoryStrategy(HistoryStrategy, strategies.one.CivilOneStrategy):
    def configure_role(self):
        self.voting_history = {}
        self.trust_list = {}
        self.trusted = [self.name]

    def get_kill_notice(self, player_id, initiator, role_type):
        trust_level = -1 * round(1.0/(self.game.total_players-1), 2)
        if role_type is self.game.Mafia:
            trust_level *= -1
        if player_id and player_id in self.voting_history.keys():
            for player in self.voting_history.get(player_id):
                if player in self.trust_list.keys():
                    self.trust_list[player] += trust_level
        if player_id in self.trust_list.keys():
            self.trust_list.pop(player_id)


class SheriffHistoryStrategy(HistoryStrategy, strategies.one.SheriffOneStrategy):
    def configure_role(self):
        self.trusted = [self.name]
        self.known_mafia = []
        self.trust_list = {}
        self.voting_history = {}

    def get_kill_notice(self, player_id, initiator, role_type):
        trust_level = -1 * round(1.0/(self.game.total_players-1), 2)
        if role_type is self.game.Mafia:
            trust_level *= -1
        if player_id and player_id in self.voting_history.keys():
            for player in self.voting_history.get(player_id):
                if player in self.trust_list.keys():
                    self.trust_list[player] += trust_level
        if player_id in self.trust_list.keys():
            self.trust_list.pop(player_id)
        if player_id in self.known_mafia:
            self.known_mafia.remove(player_id)

    def day_vote(self):
        if self.known_mafia:
            return random.choice(self.known_mafia)
        vote_list = []
        trust_level = 1
        for player in self.game.list_players(skip=self.trusted):
            if self.trust_list[player] < trust_level:
                vote_list = [player]
                trust_level = self.trust_list[player]
            elif self.trust_list[player] == trust_level:
                vote_list.append(player)
        return random.choice(vote_list)

    def check_player(self):
        candidates = []
        trust_level = 1
        for player in self.game.list_players(skip=self.trusted + self.known_mafia):
            if self.trust_list[player] < trust_level:
                candidates = [player]
                trust_level = self.trust_list[player]
            elif self.trust_list[player] == trust_level:
                candidates.append(player)
        if not candidates:
            candidate = self.name
        else:
            candidate = random.choice(candidates)
        return candidate


class DoctorHistoryStrategy(HistoryStrategy, strategies.one.DoctorOneStrategy):
    def configure_role(self):
        self.healed = False
        self.night_heal = None
        self.trusted = [self.name]
        self.trust_list = {}
        self.voting_history = {}

    def get_kill_notice(self, player_id, initiator, role_type):
        if player_id in self.trusted:
            self.trusted.remove(player_id)
        if (initiator is self.game.Mafia):
            if not player_id and self.night_heal:
                if self.night_heal not in self.trusted:
                    self.trusted.append(self.night_heal)
            self.night_heal = None
        trust_level = -1 * round(1.0/(self.game.total_players-1), 2)
        if role_type is self.game.Mafia:
            trust_level *= -1
        if player_id and player_id in self.voting_history.keys():
            for player in self.voting_history.get(player_id):
                if player in self.trust_list.keys():
                    self.trust_list[player] += trust_level
        if player_id in self.trust_list.keys():
            self.trust_list.pop(player_id)


class MafiaHistoryStrategy(strategies.one.MafiaOneStrategy):
    pass

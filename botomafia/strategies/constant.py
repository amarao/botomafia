from strategies.default import ZeroStrategy
import random
import copy


class CivilLiftStrategy(ZeroStrategy):
    def day_vote(self):
        return random.choice(self.game.list_players(skip=self.name))

    def kill_many_players(self, kill_list):
        return True


class SheriffLiftStrategy(ZeroStrategy):
    def kill_many_players(self, kill_list):
        for player in kill_list:
            if player not in self.trusted:
                break
        else:
            return False
        return True

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


class DoctorLiftStrategy(ZeroStrategy):
    def kill_many_players(self, kill_list):
        for player in kill_list:
            if player not in self.trusted:
                break
        else:
            return False
        return True

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

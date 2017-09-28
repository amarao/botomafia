from strategies.default import ZeroStrategy
import random
import copy
import messages


class CivilOneStrategy(ZeroStrategy):
    def configure_role(self):
        self.first_vote = None

    # def listen(self, speech_type, speaker_id, target_id, speech):
    #     if speech_type == "day_vote" and self.first_vote == None:
    #         self.first_vote = target_id

    def day_vote(self):
        if self.first_vote and self.first_vote != self.name:
            return self.first_vote
        else:
            return random.choice(self.game.list_players(skip=self.name))

    def new_day_notice(self):
        self.first_vote = None

    def kill_many_players(self, kill_list):
        return True


class SheriffOneStrategy(ZeroStrategy):
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
        self.first_vote = None

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
        elif self.first_vote and self.first_vote not in self.trusted:
            return self.first_vote
        return random.choice(self.game.list_players(skip=self.trusted))

    def get_check_result(self, player_id, status):
        if status == self.game.Civil:
            self.trusted.append(player_id)
        elif status == self.game.Mafia:
            self.known_mafia.append(player_id)

    def new_day_notice(self):
        self.first_vote = None

    # def listen(self, speech_type, speaker_id, target_id, speech):
    #     if speech_type == "day_vote" and self.first_vote == None:
    #         self.first_vote = target_id


class DoctorOneStrategy(ZeroStrategy):
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
        self.first_vote = None

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
        if (
            self.first_vote and
            self.first_vote != self.name and
            self.first_vote not in self.trusted
        ):
            return self.first_vote
        return random.choice(self.game.list_players(skip=self.trusted))

    def get_kill_notice(self, player_id, initiator, role_type):
        if player_id in self.trusted:
            self.trusted.remove(player_id)
        if (initiator is self.game.Mafia):
            if not player_id and self.night_heal:
                if self.night_heal not in self.trusted:
                    self.trusted.append(self.night_heal)
            self.night_heal = None

    def new_day_notice(self):
        self.first_vote = None

    # def listen(self, speech_type, speaker_id, target_id, speech):
    #     if speech_type == "day_vote" and self.first_vote == None:
    #         self.first_vote = target_id


class MafiaOneStrategy(ZeroStrategy):
    def configure_role(self):
        self.night_kill = None
        self.first_vote = None

    def day_vote(self):
        if self.first_vote and self.first_vote != self.name:
            return self.first_vote
        return random.choice(self.game.list_players(skip=self.mafia))

    def mafia_night_meet(self, mafia):
        self.mafia = [m.name for m in mafia]

    def night_say(self):
        if not self.night_kill:
            self.night_kill = random.choice(
                 self.game.list_players(skip=self.mafia)
            )
        return messages.Kill(self.night_kill)

    def listen(self, speech):
        if type(speech) is messages.MafiaNightSay:
            if speech.messages.player_id:
                self.night_kill = speech.messages.player_id
    #     if speech_type == "day_vote" and self.first_vote == None:
    #         self.first_vote = target_id

    def listen_Kill(self, speech, message):
        self.game.log.info("Kill!!!!!")
        self.night_kill = message.player_id

    def night_vote(self):
        return self.night_kill

    def new_day_notice(self):
        self.night_kill = None
        self.first_vote = None

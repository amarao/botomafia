from strategies.default import CivilZeroStrategy, SheriffZeroStrategy
from strategies.default import DoctorZeroStrategy

class CivilLiftStrategy(CivilZeroStrategy):
    def kill_many_players(self, kill_list):
        return True

class SheriffLiftStrategy(SheriffZeroStrategy):
    def kill_many_players(self, kill_list):
        for player in kill_list:
            if player not in self.trusted:
                break
        else:
            return False
        return True

class DoctorLiftStrategy(DoctorZeroStrategy):
    def kill_many_players(self, kill_list):
        for player in kill_list:
            if player not in self.trusted:
                break
        else:
            return False
        return True

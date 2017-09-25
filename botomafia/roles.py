from strategies.default import DefaultStrategy
import types


class Role(object):

    def __init__(self, name, game, strategies=[]):
        self.name = name
        self.game = game
        self.stategy = None
        if not strategies:
            self.strategies = [DefaultStrategy]
        else:
            self.strategies = strategies
        self.strategy = self._switch_strategy(strategies[0])
        self.configure_role()

    def _switch_strategy(self, NewStrategy):

        if NewStrategy != DefaultStrategy:
            self._switch_strategy(DefaultStrategy)  # cleanup old functions

        for method_name in dir(NewStrategy):
            if method_name.startswith('_'):
                    continue
            function = getattr(NewStrategy, method_name).__func__
            setattr(self, method_name, types.MethodType(function, self))
        return NewStrategy

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s [%s]" % (self.name, self.role)


class Civil(Role):
    side = "Civil"
    role = "Citizen"


class Sheriff(Civil):
    role = "Sheriff"


class Doctor(Civil):
    role = "Doctor"


class Mafia(Role):
    side = "Mafia"
    role = "Mafia"

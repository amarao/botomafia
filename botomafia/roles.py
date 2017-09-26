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
        self.first_strategy = self.strategy
        self.initial_constants = {}
        self.configure_role()

    def _switch_strategy(self, NewStrategy):
        for method_name in dir(self):
            if not method_name.startswith('_'):
                delattr(self, method_name)
        for method_name in dir(NewStrategy):
            if not method_name.startswith('_'):
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


class SpecialRole(Civil):
    side = "Civil"
    role = "Some role"


class Sheriff(SpecialRole):
    role = "Sheriff"


class Doctor(SpecialRole):
    role = "Doctor"


class Mafia(Role):
    side = "Mafia"
    role = "Mafia"

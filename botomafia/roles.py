from strategies.default import DefaultCivilStrategy
import types


class Role(object):

    def __init__(self, name, game, strategies=[]):
        self.name = name
        self.game = game
        self.stategy = None
        if not strategies:
            self.strategies = [DefaultCivilStrategy]
        else:
            self.strategies = strategies
        self.strategy = self._switch_strategy(strategies[0])
        self.first_strategy = self.strategy
        self.initial_constants = {}
        self.configure_role()

    def _switch_strategy(self, NewStrategy):
        save = ['role', 'side', 'name', 'game']
        for method_name in dir(self):
            if not method_name.startswith('_') and method_name not in save:
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

    def _listen(self, speech):
        if not speech.messages:
            return
        if 'listen' in dir(self):
            return self.listen(speech)
        say_listen_method_name = 'listen_' + speech.__class__.__name__
        if say_listen_method_name in dir(self):
            say_listen_method = getattr(self, say_listen_method_name)
            return say_listen_method(speech.speaker_id, speech.messages)
        for message in speech.messages:
            message_listen_method_name = 'listen_' + message.__class__.__name__
            if message_listen_method_name in dir(self):
                message_listen_method = getattr(
                    self, message_listen_method_name)
                message_listen_method(speech, message)


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

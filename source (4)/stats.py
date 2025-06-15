#Matsvei Tonki
class TeamStats:
    def __init__(self):
        self.players = []
        self.goals = []
        self.cards = []
        self.substitutions = []

    def get_players(self):
        if not self.players:
            return "NO INFO AVAILABLE!"
        return "PLAYERS:\n" + '\n'.join(self.players) + '\n'

    def get_goals(self):
        if not self.goals:
            return "GOALS:"
        goals_info = "GOALS:\n"
        for minute, player in self.goals:
            goals_info += "{}' {}\n".format(minute, player)
        return goals_info

    def get_score(self):
        return len(self.goals)

    def get_cards(self):
        if not self.cards:
            return "CARDS:"
        cards_info = "CARDS:\n"
        for minute, color, player in self.cards:
            cards_info += "{}' {} {}\n".format(minute, player, color[0].upper())
        return cards_info

    def get_subs(self):
        if not self.substitutions:
            return "SUBS:"
        subs_info = "SUBS:\n"
        for minute, out_player, in_player in self.substitutions:
            subs_info += "{}' {} for {}\n".format(minute, in_player, out_player)
        return subs_info

    def print_summary(self):
        print self.get_players().strip()
        print self.get_goals().strip()
        print self.get_cards().strip()
        print self.get_subs().strip()
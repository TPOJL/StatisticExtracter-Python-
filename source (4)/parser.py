# Matsvei Tonki
import re

class GameParser:
    def __init__(self, TeamStats_home, TeamStats_visit):
        self.TeamStats_home = TeamStats_home
        self.TeamStats_visit = TeamStats_visit
        self.Team_Home = None
        self.Team_Came = None
        self.Venue = None
        self.Date = None


    def parse(self, raport):
        lines = raport.split('\n')
        header = None
        lineups = {}
        current_team = None
        game = False

        for line in lines:
            line = line.strip()
            if re.match(r'(.+) (vs|v\.) (.+) (@|at|venue) (.+) (on) (.+)', line, re.IGNORECASE):
                header = line
            elif re.match(r'lineup', line, re.IGNORECASE):
                parts = line.split(' ')
                current_team = ' '.join(parts[1:])
                lineups[current_team] = []
            elif re.match(r'\d+ ', line) and current_team:
                parts = line.split(' ')
                Name = ' '.join(parts[1:]).strip()
                lineups[current_team].append(Name)
            elif re.match(r'(game)', line, re.IGNORECASE):
                game = True
                continue

        match = re.match(r'(.+) (vs|v\.) (.+) (@|at|venue) (.+) (on) (.+)', header, re.IGNORECASE)
        home_team = match.group(1)
        away_team = match.group(3)
        self.Venue = match.group(5)
        self.Date = match.group(7)
        self.Team_Home = home_team
        self.Team_Came = away_team

        for team, players in lineups.items():
            if team == home_team:
                self.TeamStats_home.players = players
            elif team == away_team:
                self.TeamStats_visit.players = players

        for line in lines:
            line = line.strip()
            if re.match(r'^game', line, re.IGNORECASE):
                game = True
                continue
            if game:
                if re.match(r'(\d+)(m|\'|min)\s+g+o+a+l+\s+((?:(?!(?:\bog\b)).)+)', line, re.IGNORECASE):
                    goal_match = re.match(r'(\d+)(m|\'|min)\s+G+o+a+l+\s+((?:(?!(?:\bog\b)).)+)(?:(?:\s+\(og\))|$)',
                                          line, re.IGNORECASE)
                    minute = goal_match.group(1)
                    player = goal_match.group(3).strip()
                    player_found = False
                    for team, team_players in lineups.items():
                        if player in team_players:
                            player_found = True
                            if "(og)" in line.lower():
                                player += " (OG)"
                                if team == home_team:
                                    self.TeamStats_visit.goals.append((minute, player))
                                else:
                                    self.TeamStats_home.goals.append((minute, player))
                            else:
                                if team == home_team:
                                    self.TeamStats_home.goals.append((minute, player))
                                else:
                                    self.TeamStats_visit.goals.append((minute, player))
                    if not player_found:
                        self.TeamStats_visit.goals.append((minute, player))


                elif re.search(r'card', line, re.IGNORECASE):
                    minute, color, player = self.extract_card(line)
                    assigned = False
                    for team, team_players in lineups.items():
                        if player in team_players:
                            if team == home_team:
                                self.TeamStats_home.cards.append((minute, color, player))
                            elif team == away_team:
                                self.TeamStats_visit.cards.append((minute, color, player))
                            assigned = True
                    if not assigned:
                        self.TeamStats_home.cards.append((minute, color, player))
                elif re.search(r'(sub|substitution)', line, re.IGNORECASE):
                    minute, out_player, in_player = self.extract_substitution(line)
                    for team, team_players in lineups.items():
                        if out_player in team_players or in_player in team_players:
                            if team == home_team:
                                self.TeamStats_home.substitutions.append((minute, out_player, in_player))
                            elif team == away_team:
                                self.TeamStats_visit.substitutions.append((minute, out_player, in_player))

    def extract_card(self, event):
        match = re.match(r'(\d+)(m|\'|min)\s+card\s+(\w+)\s+(.+)', event, re.IGNORECASE)
        if match:
            minute = match.group(1)
            color = match.group(3)
            player = match.group(4)
            return minute, color, player

    def extract_substitution(self, event):
        match = re.match(r'(\d+)(m|\'|min)\s+(sub|substitution)\s+(off|out)\s+(.+)\s+(in|on)\s+(.+)(?:\.|$)', event,re.IGNORECASE)
        if match:
            minute = match.group(1)
            out_player = match.group(5).strip()
            in_player = match.group(7).strip()
            return minute, out_player, in_player

    def print_summary(self):
        if self.Team_Home is None or self.Team_Came is None or self.Venue is None or self.Date is None:
            print "NO INFO AVAILABLE!"
            return

        print "HOME:", self.Team_Home
        print "AWAY:", self.Team_Came
        print "SCORE:", str(len(self.TeamStats_home.goals)) + ":" + str(len(self.TeamStats_visit.goals))
        print "VENUE:", self.Venue
        print "DATE:", self.Date
        print

        print "TEAM " + self.Team_Home
        self.TeamStats_home.print_summary()
        print

        print "TEAM " + self.Team_Came
        self.TeamStats_visit.print_summary()

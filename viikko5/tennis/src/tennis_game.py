POINTS = ["Love", "Fifteen", "Thirty", "Forty"]

class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score += 1
        else:
            self.player2_score += 1

    def get_score(self):
        if self.player1_score == self.player2_score:
            return self.even()
        if self.player1_score >= 4 or self.player2_score >= 4:
            return self.advantage_or_win()
        else:
            return f"{POINTS[self.player1_score]}-{POINTS[self.player2_score]}"

    def even(self):
        if self.player1_score < 3:
            return f"{POINTS[self.player1_score]}-All"
        return "Deuce"
    
    def advantage_or_win(self):
        diff = self.player1_score - self. player2_score
        if diff == 1:
            return f"Advantage {self.player1_name}"
        elif diff == -1:
            return f"Advantage {self.player2_name}"
        elif diff >= 2:
            return f"Win for {self.player1_name}"
        return f"Win for {self.player2_name}"

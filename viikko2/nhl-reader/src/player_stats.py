from player_reader import PlayerReader

class PlayerStats:
    def __init__(self, reader):
        self._reader = reader
        self._players = reader.get_players()
    

    def top_scorers_by_nationality(self, nat):
        players_by_nationality = list(filter(lambda player: player.nationality == nat, self._players))

        def sort_by_points(player):
            return player.points
    
        sorted_players = sorted(players_by_nationality, reverse=True, key=sort_by_points)
        return sorted_players
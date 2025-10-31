import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_player_search(self):
      player = self.stats.search("Kurri")
      self.assertEqual(player.name, "Kurri")


    def test_search_nonexisting(self):
        player = self.stats.search("Selanne")
        self.assertEqual(player, None)
    
    def test_team_search(self):
        players = self.stats.team("DET")
        self.assertEqual(1, len(players))
        player = players[0]
        self.assertEqual(player.name, "Yzerman")




    

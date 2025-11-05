from player import Player
from player_reader import PlayerReader
from player_stats import PlayerStats
from rich.console import Console
from rich.table import Table



def tulosta():
    seasons=[]
    for i in range(18,26):
        seasons.append(f"20{i}-{i+1}")
    display_seasons = " / ".join(seasons)
    nats=["USA", "FIN", "CAN", "SWE", "CZE", "RUS", "SLO", "FRA", "GBR", "SVK", 
          "DEN", "NED", "AUT", "BLR", "GER", "SUI", "NOR", "UZB", "LAT", "AUS"]
    display_nats = " / ".join(nats)
    console = Console()
    
    season = console.input(f"Season {display_seasons}")
    nat = console.input(f"Nationality {display_nats}")
    table = Table(title=f"Season {season} players from {nat}")


def main():
    seasons=[]
    for i in range(23,26):
        seasons.append(f"20{i}-{i+1}")
    display_seasons = " / ".join(seasons)
    nats=["USA", "FIN", "CAN", "SWE", "CZE", "RUS", "SLO", "FRA", "GBR", "SVK", 
          "DEN", "NED", "AUT", "BLR", "GER", "SUI", "NOR", "UZB", "LAT", "AUS"]
    display_nats = " / ".join(nats)
    console = Console()
    
    season = console.input(f"Season: {display_seasons} ")
    while True:
        if season in seasons:
            break
        else:
            season = console.input(f"Invalid. Pick season: {display_seasons} ")
    
    #url = "https://studies.cs.helsinki.fi/nhlstats/2023-24/players"
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
   # response = requests.get(url).json()

    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    while True:
        nat = console.input(f"Nationality: {display_nats} ")
        if nat.lower()=='exit':
            break
        while True:
            if nat in nats:
                break
            else:
                nat = console.input(f"Invalid. Choose nationality {display_nats} ")

        players= stats.top_scorers_by_nationality(nat)
        table = Table(title=f"Season {season} players from {nat}")
        table.add_column("Player", style="cyan", no_wrap=True)
        table.add_column("teams", style="magenta")
        table.add_column("goals", style="green")
        table.add_column("assists", style="green")
        table.add_column("points", style="green")
    
    
    
        for player in players:
            #print(player)
            table.add_row(player.name, player.team, f"{player.goals}",f"{player.assists}", f"{player.points}")
        console.print(table)


if __name__ == "__main__":
    main()

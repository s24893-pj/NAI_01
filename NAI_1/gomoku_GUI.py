from easyAI import TwoPlayerGame
from easyAI.Player import Human_Player
from rich.console import Console
from rich.table import Table
from easyAI import AI_Player, Negamax


class Gomoku(TwoPlayerGame):
    """
    https://www.kurnik.pl/gomoku/zasady.phtml
    Autorzy:
    Andrzej Ebertowski s25222
    Mateusz Wiśniewski s24893
    Przygotowanie środowiska:
    pip install easyai
    pip install rich
    Gra powinna być rozgrywana z poziomu wiersza poleceń (CMD) (python gomoku_GUI.py)
    Gra rozgrywa się na planszy 8x8
    Pola numerowane są od 1 do 64
    Warunkiem zwycięstwa jest postawienie 5 znaków w linii poziomej / pionowej / ukośnej
    """

    def __init__(self, players):
        self.players = players
        self.board = [0 for i in range(64)]
        self.current_player = 1

    def possible_moves(self):
        """
        Zwraca listę możliwych ruchów na planszy

        Returns:
            list[int]: Lista wolnych pozycji (1-64), na które można wykonać ruch
        """
        return [i + 1 for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move):
        """
        Wykonuje ruch, ustawiając symbol gracza na wybranym polu.

        Parameters:
            move (int):

        Returns:
            None
        """
        self.board[int(move) - 1] = self.current_player

    def unmake_move(self, move):
        """
        Funkcja EasyAI która pozwala przyspieszyć szybkość AI

        Parameters:
            move (int):

        Returns:
            None
        """
        self.board[int(move) - 1] = 0

    def lose(self):
        """
        funckja tworzy listę linii które definiują warunek zwycięstwa
        (5 pod rząd w linii poziomej / pionowej / ukośnej)
        W kolejności:
        Linie poziome
        Linie pionowe
        Linie ukośne (od lewej góry do prawego dołu)
        Linie ukośne od lewego dołu do prawej góry

        Returns:
            bool: występuje linia definiująca zwycięstwo
         """
        lines: list[list[int]] = []

        for row in range(8):
            for col in range(4):
                lines.append([row * 8 + col + i + 1 for i in range(5)])

        for col in range(8):
            for row in range(4):
                lines.append([(row + i) * 8 + col + 1 for i in range(5)])

        for row in range(4):
            for col in range(4):
                lines.append([(row + i) * 8 + col + i + 1 for i in range(5)])

        for row in range(4, 8):
            for col in range(4):
                lines.append([(row - i) * 8 + col + i + 1 for i in range(5)])

        return any(
            all(self.board[c - 1] == self.opponent_index for c in line) for line in lines
        )

    def is_over(self):
        """
        Sprawdza czy gra się zakończyła

        Returns:
            bool: zwraca koniec gry definiowany porażką
        """
        return self.lose()

    def show(self):
        """
        Wyświetla aktualny stan planszy w formie tabeli
        Symbole:
            ▪: Puste pole
            O: Ruch gracza 1 (zielony kolor)
            X: Ruch gracza 2 (czerwony kolor)

        Returns:
            None
        """
        table = Table(show_header=False, show_lines=True)

        for _ in range(8):
            table.add_column(justify="center", style="bold")

        for j in range(8):
            row_symbols = [
                ["▪", "[green]O[/green]", "[red]X[/red]"][self.board[8 * j + i]] for i in range(8)
            ]
            table.add_row(*row_symbols)

        console = Console()
        console.print("\n")
        console.rule("[purple]NAI s24893 | s25222 [/purple]")
        console.print("\n ", table, justify="center")

    def scoring(self):
        """
        Zwraca wartość punktową dla bieżącego stanu gry.
        -1, jeśli gracz przegrał, w przeciwnym razie 0.

        Returns:
            int: Wartość punktowa
        """
        return -1 if self.lose() else 0

    def start(self):
        """
        Uruchamia rozgrywkę z maksymalnie 64 ruchami.
        Po zakończeniu gry wyświetla się informacja o zwycięzcy.

        Returns:
            None
        """
        self.play(nmoves=64)
        print(f"player {self.opponent_index} wins!")


if __name__ == "__main__":
    ai_algo = Negamax(4)
    game = Gomoku([Human_Player(), AI_Player(ai_algo)])

    game.start()

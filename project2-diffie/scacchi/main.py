import sys

from rich import print

from scacchi.boundary.BoundaryHelp import Help
from scacchi.control.InizioC import InizioC


class UI:
    """Defines the configuration of the game's UI."""

    def __init__(self):
        """Initialize the game's UI with default settings."""
        self._ACCENT_COLOR: str = "red"

    def set_accent_color(self, accent_color: str):
        """Set the accent color for the game's UI.

        List of valid colors supported by the Rich library:
            - `black`
            - `red`
            - `green`
            - `yellow`
            - `blue`
            - `magenta`
            - `cyan`
            - `white`
            - `bright_black`
            - `bright_red`
            - `bright_green`
            - `bright_yellow`
            - `bright_blue`
            - `bright_magenta`
            - `bright_cyan`
            - `bright_white`

        Args:
            accent_color (str): the accent color to be used in the game's UI

        Raises:
            ValueError: if the accent color is not supported by the Rich library

        """
        RICH_COLORS: set[str] = {
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
            "bright_black",
            "bright_red",
            "bright_green",
            "bright_yellow",
            "bright_blue",
            "bright_magenta",
            "bright_cyan",
            "bright_white",
        }

        # If the user provides an accent color, then use it
        if accent_color in RICH_COLORS:
            self._ACCENT_COLOR = accent_color
        else:
            raise ValueError(
                f"Invalid accent color '{self._ACCENT_COLOR}'. "
                "Please choose a color supported by the Rich library."
            )

    def get_accent_color(self) -> str:
        """Get the accent color for the game's UI.

        Returns:
            accent color

        """
        return self._ACCENT_COLOR


def main():
    """Run the Scacchi game and activate the GH workflows."""
    if len(sys.argv)>1 and sys.argv[1] not in ("--help", "-h"):
        print("[ERRORE] Parametro non valido. Usa --help o -h.")
        sys.exit(1)
    else:
        if len(sys.argv)>1 and sys.argv[1] in ("--help", "-h"):
            Help.print_help()
    ui = UI()
    ui.set_accent_color("blue")

    print(
        "[yellow]per vedere in maniera chiara la scacchiera usare il "
        "terminale con sfondo chiaro[/yellow]"
    )

    name = input("Benvenuto in Scacchi! Inserisci il tuo nome: ")
    print(
        f"Ciao [bold {ui.get_accent_color()}]{name}[/bold {ui.get_accent_color()}]! "
        "Iniziamo a giocare a [bold]scacchi[/bold]!"
    )

    m = InizioC(name)
    m.run()


if __name__ == "__main__":
    main()

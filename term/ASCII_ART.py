from PIL import Image
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import logging
import sys
import os

# ─────────────────────────── Configuration ────────────────────────────

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

CHAR_SETS: dict[str, str] = {
    "standard": "@%#*+=-:. ",
    "detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    "simple":   "@#*+=-:. ",
    "blocks":   "█▓▒░ ",
    "minimal":  "#. ",
    "braille":  "⣿⣷⣯⣟⡿⢿⣻⣽ ",
}

BORDER_STYLES: dict[str, tuple[str, ...]] = {
    "single":  ("┌", "┐", "└", "┘", "─", "│"),
    "double":  ("╔", "╗", "╚", "╝", "═", "║"),
    "rounded": ("╭", "╮", "╰", "╯", "─", "│"),
    "thick":   ("┏", "┓", "┗", "┛", "━", "┃"),
    "ascii":   ("+", "+", "+", "+", "-",  "|"),
    "dashed":  ("┌", "┐", "└", "┘", "╌", "╎"),
    "heavy":   ("▛", "▜", "▙", "▟", "▀",  "█"),
}

FONT_MAP: dict[str, dict[str, list[str]]] = {
    "A": ["  A  ", " A A ", "AAAAA", "A   A", "A   A"],
    "B": ["BBBB ", "B   B", "BBBB ", "B   B", "BBBB "],
    "C": [" CCC ", "C   C", "C    ", "C   C", " CCC "],
    "D": ["DDDD ", "D   D", "D   D", "D   D", "DDDD "],
    "E": ["EEEEE", "E    ", "EEEE ", "E    ", "EEEEE"],
    "F": ["FFFFF", "F    ", "FFFF ", "F    ", "F    "],
    "G": [" GGG ", "G    ", "G  GG", "G   G", " GGG "],
    "H": ["H   H", "H   H", "HHHHH", "H   H", "H   H"],
    "I": ["IIIII", "  I  ", "  I  ", "  I  ", "IIIII"],
    "J": ["JJJJJ", "    J", "    J", "J   J", " JJJ "],
    "K": ["K   K", "K  K ", "KKK  ", "K  K ", "K   K"],
    "L": ["L    ", "L    ", "L    ", "L    ", "LLLLL"],
    "M": ["M   M", "MM MM", "M M M", "M   M", "M   M"],
    "N": ["N   N", "NN  N", "N N N", "N  NN", "N   N"],
    "O": [" OOO ", "O   O", "O   O", "O   O", " OOO "],
    "P": ["PPPP ", "P   P", "PPPP ", "P    ", "P    "],
    "Q": [" QQQ ", "Q   Q", "Q   Q", "Q  Q ", " QQ Q"],
    "R": ["RRRR ", "R   R", "RRRR ", "R  R ", "R   R"],
    "S": [" SSSS", "S    ", " SSS ", "    S", "SSSS "],
    "T": ["TTTTT", "  T  ", "  T  ", "  T  ", "  T  "],
    "U": ["U   U", "U   U", "U   U", "U   U", " UUU "],
    "V": ["V   V", "V   V", "V   V", " V V ", "  V  "],
    "W": ["W   W", "W   W", "W W W", "WW WW", "W   W"],
    "X": ["X   X", " X X ", "  X  ", " X X ", "X   X"],
    "Y": ["Y   Y", " Y Y ", "  Y  ", "  Y  ", "  Y  "],
    "Z": ["ZZZZZ", "   Z ", "  Z  ", " Z   ", "ZZZZZ"],
    "0": [" 000 ", "0  00", "0 0 0", "00  0", " 000 "],
    "1": ["  1  ", " 11  ", "  1  ", "  1  ", "11111"],
    "2": [" 222 ", "2   2", "   2 ", "  2  ", "22222"],
    "3": ["3333 ", "    3", " 333 ", "    3", "3333 "],
    "4": ["4   4", "4   4", "44444", "    4", "    4"],
    "5": ["55555", "5    ", "5555 ", "    5", "5555 "],
    "6": [" 666 ", "6    ", "6666 ", "6   6", " 666 "],
    "7": ["77777", "    7", "   7 ", "  7  ", " 7   "],
    "8": [" 888 ", "8   8", " 888 ", "8   8", " 888 "],
    "9": [" 999 ", "9   9", " 9999", "    9", " 999 "],
    "!": ["  !  ", "  !  ", "  !  ", "     ", "  !  "],
    "?": [" ??? ", "?   ?", "   ? ", "     ", "  ?  "],
    ".": ["     ", "     ", "     ", " ..  ", " ..  "],
    ",": ["     ", "     ", "     ", " ,,  ", ",    "],
    " ": ["     ", "     ", "     ", "     ", "     "],
}

# ─────────────────────────── Data Classes ─────────────────────────────

@dataclass
class ImageConfig:
    width:  int            = 100
    height: Optional[int]  = None
    invert: bool           = False
    contrast: float        = 1.0      # 0.5 = low, 2.0 = high
    aspect_correction: float = 0.55   # compensates for terminal char height

@dataclass
class AsciiArt:
    """Holds the generated ASCII art and its metadata."""
    content:  str
    source:   str = ""
    char_set: str = "standard"

    def __str__(self) -> str:
        return self.content

    def with_border(self, style: str = "single") -> "AsciiArt":
        bordered = BorderRenderer.render(self.content, style)
        return AsciiArt(bordered, self.source, self.char_set)

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.write_text(self.content, encoding="utf-8")
        logger.info("Saved to %s", path)
        return path

    def preview(self, max_lines: int = 40) -> str:
        lines = self.content.splitlines()
        if len(lines) <= max_lines:
            return self.content
        half = max_lines // 2
        omitted = len(lines) - max_lines
        return (
            "\n".join(lines[:half])
            + f"\n... [{omitted} lines omitted] ...\n"
            + "\n".join(lines[-half:])
        )

# ─────────────────────────── Renderers ────────────────────────────────

class ImageRenderer:
    """Converts raster images to ASCII art."""

    def __init__(self, chars: str) -> None:
        if not chars:
            raise ValueError("Character set must not be empty.")
        self.chars = chars

    def render(self, path: str | Path, config: ImageConfig) -> AsciiArt:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")

        img = Image.open(path)
        width, height = self._calculate_dimensions(img, config)
        img = self._preprocess(img, width, height, config)
        content = self._pixels_to_ascii(img, width, config.invert)

        return AsciiArt(content, source=str(path), char_set=self.chars)

    # ── helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _calculate_dimensions(
        img: Image.Image, config: ImageConfig
    ) -> tuple[int, int]:
        w = config.width
        h = config.height or int(w * img.height / img.width * config.aspect_correction)
        return max(1, w), max(1, h)

    @staticmethod
    def _preprocess(
        img: Image.Image, width: int, height: int, config: ImageConfig
    ) -> Image.Image:
        img = img.resize((width, height), Image.LANCZOS).convert("L")
        if config.contrast != 1.0:
            from PIL import ImageEnhance
            img = ImageEnhance.Contrast(img).enhance(config.contrast)
        return img

    def _pixels_to_ascii(
        self, img: Image.Image, width: int, invert: bool
    ) -> str:
        n      = len(self.chars)
        pixels = list(img.getdata())
        rows   = []

        for row_start in range(0, len(pixels), width):
            row = pixels[row_start : row_start + width]
            chars_in_row = []
            for p in row:
                if invert:
                    p = 255 - p
                index = min(p * n // 256, n - 1)
                chars_in_row.append(self.chars[index])
            rows.append("".join(chars_in_row))

        return "\n".join(rows)


class TextRenderer:
    """Renders text using bitmap fonts."""

    ROWS = 5

    def render_standard(self, text: str) -> AsciiArt:
        rows = [""] * self.ROWS
        for ch in text.upper():
            glyph = FONT_MAP.get(ch, FONT_MAP[" "])
            for i, line in enumerate(glyph):
                rows[i] += line + "  "
        return AsciiArt("\n".join(r.rstrip() for r in rows), source=text)

    def render_banner(self, text: str) -> AsciiArt:
        bar  = "═" * (len(text) + 2)
        art  = f"╔{bar}╗\n║ {text} ║\n╚{bar}╝"
        return AsciiArt(art, source=text)

    def render_block(self, text: str) -> AsciiArt:
        art = " ".join(f"[{c}]" if c != " " else "   " for c in text)
        return AsciiArt(art, source=text)

    def render(self, text: str, font: str = "standard") -> AsciiArt:
        dispatch = {
            "standard": self.render_standard,
            "banner":   self.render_banner,
            "block":    self.render_block,
        }
        renderer = dispatch.get(font)
        if renderer is None:
            raise ValueError(
                f"Unknown font '{font}'. Choose from: {', '.join(dispatch)}"
            )
        return renderer(text)


class ShapeRenderer:
    """Generates geometric ASCII shapes."""

    def render(self, shape: str, size: int = 5) -> AsciiArt:
        method = getattr(self, f"_draw_{shape}", None)
        if method is None:
            available = self._available()
            raise ValueError(
                f"Unknown shape '{shape}'. Choose from: {', '.join(available)}"
            )
        return AsciiArt(method(size), source=shape)

    @staticmethod
    def _available() -> list[str]:
        return ["triangle", "square", "diamond", "circle", "heart", "star", "pyramid"]

    # ── shapes ───────────────────────────────────────────────────────

    @staticmethod
    def _draw_triangle(h: int) -> str:
        rows = []
        for i in range(1, h + 1):
            padding = " " * (h - i)
            stars   = "*" * (2 * i - 1)
            rows.append(padding + stars)
        return "\n".join(rows)

    @staticmethod
    def _draw_square(s: int) -> str:
        if s < 2:
            return "*"
        top_bottom = "*" * s
        middle     = "*" + " " * (s - 2) + "*"
        rows = [top_bottom] + [middle] * (s - 2) + [top_bottom]
        return "\n".join(rows)

    @staticmethod
    def _draw_diamond(h: int) -> str:
        top = [" " * (h - i) + "*" * (2 * i - 1) for i in range(1, h + 1)]
        return "\n".join(top + top[-2::-1])

    @staticmethod
    def _draw_circle(r: int) -> str:
        rows = []
        for y in range(-r, r + 1):
            row = "".join(
                "*" if x * x + y * y <= r * r else " "
                for x in range(-r, r + 1)
            )
            rows.append(row)
        return "\n".join(rows)

    @staticmethod
    def _draw_heart(s: int) -> str:
        rows = []
        for y in range(s, -s, -1):
            row = "".join(
                "♥ " if (x * x + y * y - s * s) ** 3 - x * x * y * y * y <= 0 else "  "
                for x in range(-s, s + 1)
            )
            rows.append(row)
        return "\n".join(rows)

    @staticmethod
    def _draw_star(_size: int = 5) -> str:
        return "\n".join([
            "    ★    ",
            "   ***   ",
            "  *****  ",
            " ******* ",
            "*********",
            " *** *** ",
            " **   ** ",
            " *     * ",
        ])

    @staticmethod
    def _draw_pyramid(h: int) -> str:
        rows = []
        for i in range(1, h + 1):
            padding = " " * (h - i)
            layer   = ("* " * i).rstrip()
            rows.append(padding + layer)
        return "\n".join(rows)


class BorderRenderer:
    """Wraps content in a decorative border."""

    @staticmethod
    def render(text: str, style: str = "single") -> str:
        chars = BORDER_STYLES.get(style)
        if chars is None:
            raise ValueError(
                f"Unknown border style '{style}'. "
                f"Choose from: {', '.join(BORDER_STYLES)}"
            )
        tl, tr, bl, br, h, v = chars
        lines     = text.splitlines()
        max_width = max((len(l) for l in lines), default=0)

        top    = tl + h * (max_width + 2) + tr
        bottom = bl + h * (max_width + 2) + br
        middle = [f"{v} {line.ljust(max_width)} {v}" for line in lines]

        return "\n".join([top, *middle, bottom])

# ─────────────────────────── Main Facade ──────────────────────────────

class ASCIIArtGenerator:
    """
    High-level facade that coordinates all renderers.

    Usage
    -----
    >>> gen = ASCIIArtGenerator("blocks")
    >>> art = gen.from_image("photo.jpg", width=80)
    >>> print(art)
    """

    def __init__(self, char_set: str = "standard") -> None:
        self.set_char_set(char_set)
        self._text   = TextRenderer()
        self._shape  = ShapeRenderer()

    # ── public API ────────────────────────────────────────────────────

    def set_char_set(self, name: str) -> None:
        if name not in CHAR_SETS:
            raise ValueError(
                f"Unknown character set '{name}'. "
                f"Choose from: {', '.join(CHAR_SETS)}"
            )
        self._char_set = name
        self._image    = ImageRenderer(CHAR_SETS[name])

    def from_image(self, path: str | Path, config: Optional[ImageConfig] = None) -> AsciiArt:
        return self._image.render(path, config or ImageConfig())

    def from_text(self, text: str, font: str = "standard") -> AsciiArt:
        return self._text.render(text, font)

    def shape(self, shape_type: str, size: int = 5) -> AsciiArt:
        return self._shape.render(shape_type, size)

    @property
    def available_char_sets(self) -> list[str]:
        return list(CHAR_SETS)

    @property
    def available_shapes(self) -> list[str]:
        return ShapeRenderer._available()

    @property
    def available_borders(self) -> list[str]:
        return list(BORDER_STYLES)

    @property
    def available_fonts(self) -> list[str]:
        return ["standard", "banner", "block"]

# ──────────────────────────── CLI ─────────────────────────────────────

class CLI:
    """Interactive command-line interface for the ASCII Art Generator."""

    DIVIDER = "─" * 50

    def __init__(self) -> None:
        self.gen = ASCIIArtGenerator()

    # ── entry point ───────────────────────────────────────────────────

    def run(self) -> None:
        print("\n🎨 ASCII Art Generator")
        while True:
            try:
                self._main_loop()
            except KeyboardInterrupt:
                print("\n\n[Interrupted]")
                if self._confirm("Exit?"):
                    break

    # ── menu ──────────────────────────────────────────────────────────

    def _main_menu(self) -> None:
        options = [
            "1. Image → ASCII",
            "2. Text  → ASCII",
            "3. Create Shape",
            "4. Create Border",
            "5. Change Char Set",
            "6. Exit",
        ]
        print(f"\n{self.DIVIDER}")
        print("\n".join(options))
        print(self.DIVIDER)

    def _main_loop(self) -> None:
        self._main_menu()
        choice = input("\nChoice (1-6): ").strip()

        handlers = {
            "1": self._handle_image,
            "2": self._handle_text,
            "3": self._handle_shape,
            "4": self._handle_border,
            "5": self._handle_char_set,
            "6": self._handle_exit,
        }

        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("⚠ Invalid choice. Please enter 1–6.")

    # ── handlers ──────────────────────────────────────────────────────

    def _handle_image(self) -> None:
        path = self._prompt("Image path")
        if not path:
            return

        config = ImageConfig(
            width    = self._prompt_int("Width", default=100, min_val=10, max_val=300),
            invert   = self._confirm("Invert colours?"),
            contrast = self._prompt_float("Contrast (0.5–2.0)", default=1.0),
        )

        try:
            art = self.gen.from_image(path, config)
        except (FileNotFoundError, OSError) as exc:
            print(f"✗ {exc}")
            return

        print(f"\n{art.preview()}")
        self._offer_border(art)
        self._offer_save(art)

    def _handle_text(self) -> None:
        text = self._prompt("Text")
        if not text:
            return

        font = self._prompt_choice(
            "Font", self.gen.available_fonts, default="standard"
        )
        try:
            art = self.gen.from_text(text, font)
        except ValueError as exc:
            print(f"✗ {exc}")
            return

        print(f"\n{art}")
        self._offer_border(art)
        self._offer_save(art)

    def _handle_shape(self) -> None:
        shape = self._prompt_choice("Shape", self.gen.available_shapes)
        size  = self._prompt_int("Size", default=5, min_val=2, max_val=40)

        try:
            art = self.gen.shape(shape, size)
        except ValueError as exc:
            print(f"✗ {exc}")
            return

        print(f"\n{art}")
        self._offer_border(art)
        self._offer_save(art)

    def _handle_border(self) -> None:
        text  = self._prompt("Text (use \\n for new lines)")
        if not text:
            return
        text  = text.replace("\\n", "\n")
        style = self._prompt_choice(
            "Border style", self.gen.available_borders, default="single"
        )
        try:
            result = BorderRenderer.render(text, style)
        except ValueError as exc:
            print(f"✗ {exc}")
            return

        art = AsciiArt(result)
        print(f"\n{art}")
        self._offer_save(art)

    def _handle_char_set(self) -> None:
        name = self._prompt_choice(
            "Character set", self.gen.available_char_sets, default="standard"
        )
        try:
            self.gen.set_char_set(name)
            print(f"✓ Character set: {CHAR_SETS[name]!r}")
        except ValueError as exc:
            print(f"✗ {exc}")

    def _handle_exit(self) -> None:
        print("\n👋 Goodbye!\n")
        sys.exit(0)

    # ── shared helpers ────────────────────────────────────────────────

    def _offer_border(self, art: AsciiArt) -> None:
        if self._confirm("Add border?"):
            style = self._prompt_choice(
                "Border style", self.gen.available_borders, default="single"
            )
            try:
                bordered = art.with_border(style)
                print(f"\n{bordered}")
            except ValueError as exc:
                print(f"✗ {exc}")

    def _offer_save(self, art: AsciiArt) -> None:
        if self._confirm("Save to file?"):
            filename = self._prompt("Filename (e.g. output.txt)")
            if filename:
                try:
                    saved_path = art.save(filename)
                    print(f"✓ Saved to: {saved_path}")
                except OSError as exc:
                    print(f"✗ Could not save: {exc}")

    # ── input utilities ───────────────────────────────────────────────

    @staticmethod
    def _prompt(label: str, default: str = "") -> str:
        suffix   = f" [{default}]" if default else ""
        response = input(f"{label}{suffix}: ").strip()
        return response or default

    @staticmethod
    def _confirm(question: str) -> bool:
        return input(f"{question} (y/n): ").strip().lower() == "y"

    @staticmethod
    def _prompt_int(
        label: str,
        default: int   = 0,
        min_val: int   = 1,
        max_val: int   = 9999,
    ) -> int:
        while True:
            raw = input(f"{label} [{default}]: ").strip()
            if not raw:
                return default
            try:
                value = int(raw)
                if min_val <= value <= max_val:
                    return value
                print(f"  ⚠ Enter a value between {min_val} and {max_val}.")
            except ValueError:
                print("  ⚠ Please enter a whole number.")

    @staticmethod
    def _prompt_float(label: str, default: float = 1.0) -> float:
        while True:
            raw = input(f"{label} [{default}]: ").strip()
            if not raw:
                return default
            try:
                return float(raw)
            except ValueError:
                print("  ⚠ Please enter a number (e.g. 1.5).")

    @staticmethod
    def _prompt_choice(
        label: str,
        choices: list[str],
        default: str = "",
    ) -> str:
        options_str = ", ".join(choices)
        while True:
            raw = input(f"{label} [{options_str}] (default={default}): ").strip()
            value = raw or default
            if value in choices:
                return value
            print(f"  ⚠ Choose one of: {options_str}")


# ─────────────────────────── Entry Point ──────────────────────────────

if __name__ == "__main__":
    CLI().run()

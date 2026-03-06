import os
from PIL import Image
import sys

class ASCIIArtGenerator:
    """A comprehensive ASCII art generator."""
    
    # Character sets (from dark to light)
    CHAR_SETS = {
        'standard': "@%#*+=-:. ",
        'detailed': "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
        'simple': "@#*+=-:. ",
        'blocks': "█▓▒░ ",
        'minimal': "#. "
    }
    
    def __init__(self, char_set='standard'):
        """Initialize with a character set."""
        self.chars = self.CHAR_SETS.get(char_set, self.CHAR_SETS['standard'])
    
    def image_to_ascii(self, image_path, width=100, height=None, invert=False):
        """
        Convert an image to ASCII art.
        
        Args:
            image_path: Path to the image file
            width: Output width in characters
            height: Output height (auto-calculated if None)
            invert: Invert the brightness
        """
        try:
            # Open and process image
            img = Image.open(image_path)
            
            # Calculate height maintaining aspect ratio
            if height is None:
                aspect_ratio = img.height / img.width
                height = int(width * aspect_ratio * 0.55)  # 0.55 compensates for character aspect ratio
            
            # Resize image
            img = img.resize((width, height))
            
            # Convert to grayscale
            img = img.convert('L')
            
            # Get pixel data
            pixels = img.getdata()
            
            # Convert pixels to ASCII
            ascii_str = ""
            for pixel in pixels:
                if invert:
                    pixel = 255 - pixel
                char_index = pixel * len(self.chars) // 256
                char_index = min(char_index, len(self.chars) - 1)
                ascii_str += self.chars[char_index]
            
            # Split into lines
            ascii_lines = [ascii_str[i:i + width] for i in range(0, len(ascii_str), width)]
            return '\n'.join(ascii_lines)
            
        except FileNotFoundError:
            return f"Error: Image file '{image_path}' not found."
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    def text_to_ascii(self, text, font='standard'):
        """Convert text to ASCII art using built-in fonts."""
        fonts = {
            'standard': self._standard_font,
            'big': self._big_font,
            'banner': self._banner_font,
            'block': self._block_font
        }
        
        font_func = fonts.get(font, self._standard_font)
        return font_func(text)
    
    def _standard_font(self, text):
        """Standard ASCII font."""
        letter_map = {
            'A': ["  A  ", " A A ", "AAAAA", "A   A", "A   A"],
            'B': ["BBBB ", "B   B", "BBBB ", "B   B", "BBBB "],
            'C': [" CCC ", "C   C", "C    ", "C   C", " CCC "],
            'D': ["DDDD ", "D   D", "D   D", "D   D", "DDDD "],
            'E': ["EEEEE", "E    ", "EEEE ", "E    ", "EEEEE"],
            'F': ["FFFFF", "F    ", "FFFF ", "F    ", "F    "],
            'G': [" GGG ", "G    ", "G  GG", "G   G", " GGG "],
            'H': ["H   H", "H   H", "HHHHH", "H   H", "H   H"],
            'I': ["IIIII", "  I  ", "  I  ", "  I  ", "IIIII"],
            'J': ["JJJJJ", "    J", "    J", "J   J", " JJJ "],
            'K': ["K   K", "K  K ", "KKK  ", "K  K ", "K   K"],
            'L': ["L    ", "L    ", "L    ", "L    ", "LLLLL"],
            'M': ["M   M", "MM MM", "M M M", "M   M", "M   M"],
            'N': ["N   N", "NN  N", "N N N", "N  NN", "N   N"],
            'O': [" OOO ", "O   O", "O   O", "O   O", " OOO "],
            'P': ["PPPP ", "P   P", "PPPP ", "P    ", "P    "],
            'Q': [" QQQ ", "Q   Q", "Q   Q", "Q  Q ", " QQ Q"],
            'R': ["RRRR ", "R   R", "RRRR ", "R  R ", "R   R"],
            'S': [" SSSS", "S    ", " SSS ", "    S", "SSSS "],
            'T': ["TTTTT", "  T  ", "  T  ", "  T  ", "  T  "],
            'U': ["U   U", "U   U", "U   U", "U   U", " UUU "],
            'V': ["V   V", "V   V", "V   V", " V V ", "  V  "],
            'W': ["W   W", "W   W", "W W W", "WW WW", "W   W"],
            'X': ["X   X", " X X ", "  X  ", " X X ", "X   X"],
            'Y': ["Y   Y", " Y Y ", "  Y  ", "  Y  ", "  Y  "],
            'Z': ["ZZZZZ", "   Z ", "  Z  ", " Z   ", "ZZZZZ"],
            ' ': ["     ", "     ", "     ", "     ", "     "],
            '!': ["  !  ", "  !  ", "  !  ", "     ", "  !  "],
            '?': [" ??? ", "?   ?", "   ? ", "     ", "  ?  "],
            '0': [" 000 ", "0   0", "0   0", "0   0", " 000 "],
            '1': ["  1  ", " 11  ", "  1  ", "  1  ", "11111"],
            '2': [" 222 ", "2   2", "   2 ", "  2  ", "22222"],
            '3': ["3333 ", "    3", " 333 ", "    3", "3333 "],
            '4': ["4   4", "4   4", "44444", "    4", "    4"],
            '5': ["55555", "5    ", "5555 ", "    5", "5555 "],
            '6': [" 666 ", "6    ", "6666 ", "6   6", " 666 "],
            '7': ["77777", "    7", "   7 ", "  7  ", " 7   "],
            '8': [" 888 ", "8   8", " 888 ", "8   8", " 888 "],
            '9': [" 999 ", "9   9", " 9999", "    9", " 999 "],
        }
        
        text = text.upper()
        lines = [''] * 5
        
        for char in text:
            if char in letter_map:
                for i in range(5):
                    lines[i] += letter_map[char][i] + "  "
            else:
                for i in range(5):
                    lines[i] += "     "
        
        return '\n'.join(lines)
    
    def _big_font(self, text):
        """Big block font."""
        letter_map = {
            'A': [
                "   AAA   ",
                "  A   A  ",
                " A     A ",
                "AAAAAAAAA",
                "A       A"
            ],
            'B': [
                "BBBBBBBB ",
                "B       B",
                "BBBBBBBB ",
                "B       B",
                "BBBBBBBB "
            ],
            # Add more letters as needed
        }
        text = text.upper()
        lines = [''] * 5
        
        for char in text:
            if char in letter_map:
                for i in range(5):
                    lines[i] += letter_map[char][i] + "  "
            elif char == ' ':
                for i in range(5):
                    lines[i] += "    "
            else:
                # Use standard font for missing chars
                return self._standard_font(text)
        
        return '\n'.join(lines)
    
    def _banner_font(self, text):
        """Banner style font."""
        return f"""
╔{'═' * (len(text) + 2)}╗
║ {text} ║
╚{'═' * (len(text) + 2)}╝
"""
    
    def _block_font(self, text):
        """Simple block font."""
        result = ""
        for char in text:
            if char == ' ':
                result += "   "
            else:
                result += f"[{char}]"
        return result
    
    def create_shape(self, shape_type, size=5):
        """Create geometric ASCII shapes."""
        shapes = {
            'triangle': self._draw_triangle,
            'square': self._draw_square,
            'diamond': self._draw_diamond,
            'circle': self._draw_circle,
            'heart': self._draw_heart,
            'star': self._draw_star
        }
        
        shape_func = shapes.get(shape_type)
        if shape_func:
            return shape_func(size)
        else:
            return f"Unknown shape: {shape_type}"
    
    def _draw_triangle(self, height):
        """Draw a triangle."""
        lines = []
        for i in range(1, height + 1):
            spaces = ' ' * (height - i)
            stars = '*' * (2 * i - 1)
            lines.append(f"{spaces}{stars}")
        return '\n'.join(lines)
    
    def _draw_square(self, size):
        """Draw a square."""
        lines = []
        for i in range(size):
            if i == 0 or i == size - 1:
                lines.append('*' * size)
            else:
                lines.append('*' + ' ' * (size - 2) + '*')
        return '\n'.join(lines)
    
    def _draw_diamond(self, height):
        """Draw a diamond."""
        lines = []
        # Top half
        for i in range(1, height + 1):
            spaces = ' ' * (height - i)
            stars = '*' * (2 * i - 1)
            lines.append(f"{spaces}{stars}")
        # Bottom half
        for i in range(height - 1, 0, -1):
            spaces = ' ' * (height - i)
            stars = '*' * (2 * i - 1)
            lines.append(f"{spaces}{stars}")
        return '\n'.join(lines)
    
    def _draw_circle(self, radius):
        """Draw a circle."""
        lines = []
        for y in range(-radius, radius + 1):
            line = ""
            for x in range(-radius, radius + 1):
                if abs(x*x + y*y - radius*radius) < radius:
                    line += "*"
                else:
                    line += " "
            lines.append(line)
        return '\n'.join(lines)
    
    def _draw_heart(self, size=6):
        """Draw a heart."""
        lines = []
        for y in range(size, -size, -1):
            line = ""
            for x in range(-size, size + 1):
                if (x * x + y * y - size * size) ** 3 - x * x * y * y * y <= 0:
                    line += "❤ "
                else:
                    line += "  "
            lines.append(line)
        return '\n'.join(lines)
    
    def _draw_star(self, size=5):
        """Draw a star."""
        star_pattern = [
            "    *    ",
            "   ***   ",
            "  *****  ",
            " ******* ",
            "*********",
            " *** *** ",
            " **   ** ",
            " *     * "
        ]
        
        if size <= 5:
            return '\n'.join(star_pattern[:size])
        else:
            return '\n'.join(star_pattern)
    
    def create_border(self, text, style='single'):
        """Create a border around text."""
        borders = {
            'single': {'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘', 'h': '─', 'v': '│'},
            'double': {'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝', 'h': '═', 'v': '║'},
            'rounded': {'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯', 'h': '─', 'v': '│'},
            'thick': {'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛', 'h': '━', 'v': '┃'},
            'ascii': {'tl': '+', 'tr': '+', 'bl': '+', 'br': '+', 'h': '-', 'v': '|'},
        }
        
        b = borders.get(style, borders['single'])
        lines = text.split('\n')
        max_len = max(len(line) for line in lines)
        
        result = []
        result.append(b['tl'] + b['h'] * (max_len + 2) + b['tr'])
        for line in lines:
            result.append(b['v'] + ' ' + line.ljust(max_len) + ' ' + b['v'])
        result.append(b['bl'] + b['h'] * (max_len + 2) + b['br'])
        
        return '\n'.join(result)
    
    def gradient_text(self, text, width=80):
        """Create gradient effect with characters."""
        chars = self.chars[::-1]  # Reverse for light to dark
        result = []
        
        for line in text.split('\n'):
            gradient_line = ""
            for i, char in enumerate(line):
                if char != ' ':
                    char_index = int((i / len(line)) * (len(chars) - 1))
                    gradient_line += chars[char_index]
                else:
                    gradient_line += ' '
            result.append(gradient_line)
        
        return '\n'.join(result)
    
    def save_to_file(self, ascii_art, filename):
        """Save ASCII art to a file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(ascii_art)
            return f"Saved to {filename}"
        except Exception as e:
            return f"Error saving file: {str(e)}"


def interactive_menu():
    """Interactive menu for ASCII art generation."""
    generator = ASCIIArtGenerator()
    
    while True:
        print("\n" + "="*50)
        print("ASCII ART GENERATOR")
        print("="*50)
        print("\n1. Image to ASCII")
        print("2. Text to ASCII")
        print("3. Create Shape")
        print("4. Create Border")
        print("5. Change Character Set")
        print("6. Exit")
        print("\n" + "="*50)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            image_path = input("Enter image path: ").strip()
            width = input("Enter width (default 100): ").strip()
            width = int(width) if width else 100
            invert = input("Invert colors? (y/n): ").strip().lower() == 'y'
            
            print("\nGenerating ASCII art...")
            ascii_art = generator.image_to_ascii(image_path, width=width, invert=invert)
            print("\n" + ascii_art)
            
            save = input("\nSave to file? (y/n): ").strip().lower()
            if save == 'y':
                filename = input("Enter filename: ").strip()
                print(generator.save_to_file(ascii_art, filename))
        
        elif choice == '2':
            text = input("Enter text: ").strip()
            print("\nAvailable fonts: standard, big, banner, block")
            font = input("Choose font (default: standard): ").strip() or 'standard'
            
            ascii_art = generator.text_to_ascii(text, font)
            print("\n" + ascii_art)
            
            border = input("\nAdd border? (y/n): ").strip().lower()
            if border == 'y':
                print("Border styles: single, double, rounded, thick, ascii")
                style = input("Choose style (default: single): ").strip() or 'single'
                ascii_art = generator.create_border(ascii_art, style)
                print("\n" + ascii_art)
            
            save = input("\nSave to file? (y/n): ").strip().lower()
            if save == 'y':
                filename = input("Enter filename: ").strip()
                print(generator.save_to_file(ascii_art, filename))
        
        elif choice == '3':
            print("\nAvailable shapes: triangle, square, diamond, circle, heart, star")
            shape = input("Choose shape: ").strip().lower()
            size = input("Enter size (default 5): ").strip()
            size = int(size) if size else 5
            
            ascii_art = generator.create_shape(shape, size)
            print("\n" + ascii_art)
        
        elif choice == '4':
            text = input("Enter text to border: ").strip()
            print("Border styles: single, double, rounded, thick, ascii")
            style = input("Choose style (default: single): ").strip() or 'single'
            
            bordered = generator.create_border(text, style)
            print("\n" + bordered)
        
        elif choice == '5':
            print("\nAvailable character sets:")
            for name in generator.CHAR_SETS.keys():
                print(f"  - {name}")
            charset = input("Choose character set: ").strip()
            generator = ASCIIArtGenerator(charset)
            print(f"Character set changed to: {charset}")
        
        elif choice == '6':
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")


# Example usage
if __name__ == "__main__":
    # Run interactive menu
    interactive_menu()
    
    # Or use directly:
    # gen = ASCIIArtGenerator()
    # print(gen.text_to_ascii("HELLO", "standard"))
    # print(gen.create_shape("heart", 6))
    # print(gen.image_to_ascii("photo.jpg", width=80))
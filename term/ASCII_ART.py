from PIL import Image

CHARS = {
    'standard': "@%#*+=-:. ",
    'detailed': "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    'simple': "@#*+=-:. ",
    'blocks': "█▓▒░ ",
    'minimal': "#. "
}

class ASCIIArtGenerator:
    def __init__(self, char_set='standard'):
        self.chars = CHARS.get(char_set, CHARS['standard'])

    def image_to_ascii(self, image_path, width=100, height=None, invert=False):
        try:
            img = Image.open(image_path)
            if height is None:
                height = int(width * img.height / img.width * 0.55)
            img = img.resize((width, height)).convert('L')
            pixels = list(img.getdata())
            ascii_str = ''
            for p in pixels:
                if invert: p = 255 - p
                ascii_str += self.chars[min(p * len(self.chars) // 256, len(self.chars) - 1)]
            return '\n'.join(ascii_str[i:i+width] for i in range(0, len(ascii_str), width))
        except FileNotFoundError:
            return f"File not found: {image_path}"
        except Exception as e:
            return f"Error: {e}"

    def text_to_ascii(self, text, font='standard'):
        fonts = {'standard': self._standard_font, 'banner': self._banner_font, 'block': self._block_font}
        return fonts.get(font, self._standard_font)(text)

    _L = {
        'A':["  A  "," A A ","AAAAA","A   A","A   A"],'B':["BBBB ","B   B","BBBB ","B   B","BBBB "],
        'C':[" CCC ","C   C","C    ","C   C"," CCC "],'D':["DDDD ","D   D","D   D","D   D","DDDD "],
        'E':["EEEEE","E    ","EEEE ","E    ","EEEEE"],'F':["FFFFF","F    ","FFFF ","F    ","F    "],
        'G':[" GGG ","G    ","G  GG","G   G"," GGG "],'H':["H   H","H   H","HHHHH","H   H","H   H"],
        'I':["IIIII","  I  ","  I  ","  I  ","IIIII"],'J':["JJJJJ","    J","    J","J   J"," JJJ "],
        'K':["K   K","K  K ","KKK  ","K  K ","K   K"],'L':["L    ","L    ","L    ","L    ","LLLLL"],
        'M':["M   M","MM MM","M M M","M   M","M   M"],'N':["N   N","NN  N","N N N","N  NN","N   N"],
        'O':[" OOO ","O   O","O   O","O   O"," OOO "],'P':["PPPP ","P   P","PPPP ","P    ","P    "],
        'Q':[" QQQ ","Q   Q","Q   Q","Q  Q "," QQ Q"],'R':["RRRR ","R   R","RRRR ","R  R ","R   R"],
        'S':[" SSSS","S    "," SSS ","    S","SSSS "],'T':["TTTTT","  T  ","  T  ","  T  ","  T  "],
        'U':["U   U","U   U","U   U","U   U"," UUU "],'V':["V   V","V   V","V   V"," V V ","  V  "],
        'W':["W   W","W   W","W W W","WW WW","W   W"],'X':["X   X"," X X ","  X  "," X X ","X   X"],
        'Y':["Y   Y"," Y Y ","  Y  ","  Y  ","  Y  "],'Z':["ZZZZZ","   Z ","  Z  "," Z   ","ZZZZZ"],
        '0':[" 000 ","0   0","0   0","0   0"," 000 "],'1':["  1  "," 11  ","  1  ","  1  ","11111"],
        '2':[" 222 ","2   2","   2 ","  2  ","22222"],'3':["3333 ","    3"," 333 ","    3","3333 "],
        '4':["4   4","4   4","44444","    4","    4"],'5':["55555","5    ","5555 ","    5","5555 "],
        '6':[" 666 ","6    ","6666 ","6   6"," 666 "],'7':["77777","    7","   7 ","  7  "," 7   "],
        '8':[" 888 ","8   8"," 888 ","8   8"," 888 "],'9':[" 999 ","9   9"," 9999","    9"," 999 "],
        '!':["  !  ","  !  ","  !  ","     ","  !  "],'?':[" ??? ","?   ?","   ? ","     ","  ?  "],
    }

    def _standard_font(self, text):
        lines = [''] * 5
        for ch in text.upper():
            if ch in self._L:
                for i in range(5): lines[i] += self._L[ch][i] + '  '
            else:
                for i in range(5): lines[i] += '     '
        return '\n'.join(lines)

    def _banner_font(self, text):
        return f"\n╔═{'═'*len(text)}╗\n║ {text} ║\n╚═{'═'*len(text)}╝\n"

    def _block_font(self, text):
        return ' '.join(f'[{c}]' if c != ' ' else ' ' for c in text)

    def create_shape(self, shape_type, size=5):
        return getattr(self, f'_draw_{shape_type}', lambda s: f"Unknown: {shape_type}")(size)

    def _draw_triangle(self, h):
        return '\n'.join(' '*(h-i) + '*'*(2*i-1) for i in range(1, h+1))

    def _draw_square(self, s):
        return '\n'.join('*'*s if i in(0,s-1) else '*' + ' '*(s-2) + '*' for i in range(s))

    def _draw_diamond(self, h):
        top = [' '*(h-i) + '*'*(2*i-1) for i in range(1, h+1)]
        return '\n'.join(top + top[-2::-1])

    def _draw_circle(self, r):
        return '\n'.join(''.join('*' if x*x+y*y <= r*r else ' ' for x in range(-r, r+1)) for y in range(-r, r+1))

    def _draw_heart(self, s):
        return '\n'.join(''.join('* ' if (x*x+y*y-s*s)**3 - x*x*y*y*y <= 0 else '  ' for x in range(-s, s+1)) for y in range(s, -s, -1))

    def _draw_star(self, _=5):
        return '\n'.join(["    *    ","   ***   ","  *****  "," ******* ","*********"," *** *** "," **   ** "," *     * "])

    def create_border(self, text, style='single'):
        b = {'single':('┌','┐','└','┘','─','│'),'double':('╔','╗','╚','╝','═','║'),
             'rounded':('╭','╮','╰','╯','─','│'),'thick':('┏','┓','┗','┛','━','┃'),
             'ascii':('+','+','+','+','-','|')}.get(style, ('┌','┐','└','┘','─','│'))
        tl,tr,bl,br,h,v = b
        lines = text.split('\n')
        m = max(len(l) for l in lines)
        r = [tl + h*(m+2) + tr]
        for l in lines: r.append(v + ' ' + l.ljust(m) + ' ' + v)
        r.append(bl + h*(m+2) + br)
        return '\n'.join(r)

    def save(self, art, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f: f.write(art)
            return f"Saved: {filename}"
        except Exception as e: return f"Error: {e}"

def interactive_menu():
    gen = ASCIIArtGenerator()
    while True:
        print("\n"+"="*50+"\nASCII ART GENERATOR\n"+"="*50)
        print("\n1. Image to ASCII\n2. Text to ASCII\n3. Create Shape\n4. Create Border\n5. Change Char Set\n6. Exit\n"+"="*50)
        c = input("\nChoice (1-6): ").strip()
        if c == '1':
            p = input("Image path: ").strip()
            w = int(input("Width [100]: ").strip() or "100")
            inv = input("Invert? (y/n): ").strip().lower() == 'y'
            print("\n"+gen.image_to_ascii(p, w, invert=inv))
            if input("Save? (y/n): ").strip().lower() == 'y':
                print(gen.save(gen.image_to_ascii(p, w, invert=inv), input("Filename: ").strip()))
        elif c == '2':
            t = input("Text: ").strip()
            f = input("Font [standard, banner, block]: ").strip() or 'standard'
            a = gen.text_to_ascii(t, f)
            print(f"\n{a}")
            if input("Add border? (y/n): ").strip().lower() == 'y':
                s = input("Style [single, double, rounded, thick, ascii]: ").strip() or 'single'
                a = gen.create_border(a, s)
                print(f"\n{a}")
            if input("Save? (y/n): ").strip().lower() == 'y':
                print(gen.save(a, input("Filename: ").strip()))
        elif c == '3':
            s = input("Shape [triangle, square, diamond, circle, heart, star]: ").strip()
            sz = int(input("Size [5]: ").strip() or "5")
            print("\n"+gen.create_shape(s, sz))
        elif c == '4':
            t = input("Text: ").strip()
            s = input("Style [single, double, rounded, thick, ascii]: ").strip() or 'single'
            print("\n"+gen.create_border(t, s))
        elif c == '5':
            print("\nSets:", ', '.join(CHARS.keys()))
            gen = ASCIIArtGenerator(input("Choose: ").strip())
            print(f"Set to: {gen.chars}")
        elif c == '6':
            print("\nBye!\n"); break

if __name__ == "__main__":
    interactive_menu()


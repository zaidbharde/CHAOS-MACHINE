#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║                    🌀 CHAOS MACHINE 🌀                       ║
║                                                               ║
║  A collection of chaotic, fun, and mesmerizing generators     ║
║  featuring fractals, cellular automata, ASCII art, glitch     ║
║  text, strange attractors, and more!                          ║
║                                                               ║
║  No dependencies required - pure Python chaos!                ║
╚═══════════════════════════════════════════════════════════════╝
"""

import random
import math
import time
import os
import sys
import hashlib
import colorsys
from itertools import count
from collections import defaultdict

# ─────────────────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────────────────

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def rainbow_text(text):
    """Return text with ANSI rainbow colors."""
    colors = [
        '\033[91m', '\033[93m', '\033[92m',
        '\033[96m', '\033[94m', '\033[95m'
    ]
    result = ''
    for i, char in enumerate(text):
        if char == ' ' or char == '\n':
            result += char
        else:
            result += colors[i % len(colors)] + char
    return result + '\033[0m'

def ansi_color(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

def ansi_bg(r, g, b):
    return f'\033[48;2;{r};{g};{b}m'

RESET = '\033[0m'

# ─────────────────────────────────────────────────────────────
# 1. MANDELBROT SET (ASCII)
# ─────────────────────────────────────────────────────────────

def mandelbrot(width=120, height=40, max_iter=50,
               x_min=-2.5, x_max=1.0, y_min=-1.2, y_max=1.2,
               colorize=True):
    """Render the Mandelbrot set in ASCII with optional true-color."""
    chars = ' .:-=+*#%@█'
    
    print("\n" + rainbow_text("═══ 🌀 MANDELBROT SET ═══"))
    print(f"  Region: [{x_min}, {x_max}] x [{y_min}, {y_max}]")
    print(f"  Max iterations: {max_iter}\n")
    
    for row in range(height):
        line = ''
        for col in range(width):
            x0 = x_min + (x_max - x_min) * col / width
            y0 = y_min + (y_max - y_min) * row / height
            
            x, y = 0.0, 0.0
            iteration = 0
            
            while x*x + y*y <= 4.0 and iteration < max_iter:
                x_new = x*x - y*y + x0
                y = 2*x*y + y0
                x = x_new
                iteration += 1
            
            if colorize:
                if iteration == max_iter:
                    line += ansi_color(0, 0, 0) + ' '
                else:
                    hue = (iteration / max_iter) * 360
                    r, g, b = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
                    r, g, b = int(r * 255), int(g * 255), int(b * 255)
                    char_idx = int(iteration / max_iter * (len(chars) - 1))
                    line += ansi_color(r, g, b) + chars[char_idx]
            else:
                char_idx = int(iteration / max_iter * (len(chars) - 1))
                line += chars[char_idx]
        
        print(line + RESET)

# ─────────────────────────────────────────────────────────────
# 2. RULE-BASED CELLULAR AUTOMATON (1D)
# ─────────────────────────────────────────────────────────────

def cellular_automaton(rule=30, width=120, generations=50, random_init=False):
    """Run a 1D cellular automaton with a given rule number (0–255)."""
    print("\n" + rainbow_text(f"═══ 🔬 CELLULAR AUTOMATON (Rule {rule}) ═══"))
    
    rule_bin = format(rule, '08b')
    ruleset = {format(7 - i, '03b'): int(rule_bin[i]) for i in range(8)}
    
    if random_init:
        state = [random.randint(0, 1) for _ in range(width)]
    else:
        state = [0] * width
        state[width // 2] = 1
    
    alive = '█'
    dead = ' '
    
    colors = [
        ansi_color(255, 50, 50),
        ansi_color(255, 150, 0),
        ansi_color(255, 255, 0),
        ansi_color(0, 255, 100),
        ansi_color(0, 150, 255),
        ansi_color(150, 0, 255),
    ]
    
    for gen in range(generations):
        color = colors[gen % len(colors)]
        line = color
        for cell in state:
            line += alive if cell else dead
        print(line + RESET)
        
        new_state = []
        for i in range(width):
            left = state[(i - 1) % width]
            center = state[i]
            right = state[(i + 1) % width]
            pattern = f'{left}{center}{right}'
            new_state.append(ruleset[pattern])
        state = new_state

# ─────────────────────────────────────────────────────────────
# 3. GLITCH TEXT GENERATOR
# ─────────────────────────────────────────────────────────────

def glitch_text(text="CHAOS MACHINE", intensity=5, lines=15):
    """Generate glitchy, zalgo-style text."""
    print("\n" + rainbow_text("═══ 👾 GLITCH TEXT GENERATOR ═══\n"))
    
    zalgo_up = [chr(i) for i in range(0x0300, 0x0340)]
    zalgo_mid = [chr(i) for i in range(0x0340, 0x0370)]
    zalgo_down = [chr(i) for i in range(0x0316, 0x0340)]
    
    glitch_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`░▒▓█▄▀■□▪▫●○◐◑◒◓'
    
    for line_num in range(lines):
        glitched = ''
        current_intensity = random.randint(1, intensity)
        
        for char in text:
            if random.random() < 0.15:
                char = random.choice(glitch_chars)
            
            glitched += char
            
            for _ in range(random.randint(0, current_intensity)):
                glitched += random.choice(zalgo_up)
            for _ in range(random.randint(0, current_intensity // 2)):
                glitched += random.choice(zalgo_mid)
            for _ in range(random.randint(0, current_intensity)):
                glitched += random.choice(zalgo_down)
        
        r = random.randint(100, 255)
        g = random.randint(0, 100)
        b = random.randint(100, 255)
        
        padding = ' ' * random.randint(0, 20)
        print(f"{ansi_color(r, g, b)}{padding}{glitched}{RESET}")

# ─────────────────────────────────────────────────────────────
# 4. CHAOS GAME FRACTAL (Sierpiński Triangle)
# ─────────────────────────────────────────────────────────────

def chaos_game(width=120, height=55, points=8000, n_vertices=3, ratio=0.5):
    """
    Play the chaos game to generate fractals.
    - 3 vertices, ratio 0.5 → Sierpiński triangle
    - 4 vertices, ratio 0.5, skip same vertex → Vicsek fractal
    - 5 vertices, ratio ~0.618 → Pentagonal fractal
    """
    print("\n" + rainbow_text(f"═══ 🎲 CHAOS GAME ({n_vertices} vertices, ratio={ratio}) ═══\n"))
    
    canvas = [[' ' for _ in range(width)] for _ in range(height)]
    
    vertices = []
    for i in range(n_vertices):
        angle = (2 * math.pi * i / n_vertices) - math.pi / 2
        vx = int((math.cos(angle) * 0.45 + 0.5) * (width - 1))
        vy = int((math.sin(angle) * 0.45 + 0.5) * (height - 1))
        vertices.append((vx, vy))
    
    x, y = random.random() * width, random.random() * height
    
    for i in range(points):
        vertex = random.choice(vertices)
        x = x + (vertex[0] - x) * ratio
        y = y + (vertex[1] - y) * ratio
        
        px, py = int(x), int(y)
        if 0 <= px < width and 0 <= py < height:
            canvas[py][px] = '•'
    
    for v in vertices:
        vx, vy = v
        if 0 <= vx < width and 0 <= vy < height:
            canvas[vy][vx] = '◆'
    
    gradient = [
        ansi_color(50, 0, 80),
        ansi_color(100, 0, 150),
        ansi_color(150, 50, 200),
        ansi_color(200, 100, 255),
        ansi_color(255, 150, 255),
    ]
    
    for row_idx, row in enumerate(canvas):
        color = gradient[row_idx * len(gradient) // height]
        print(color + ''.join(row) + RESET)

# ─────────────────────────────────────────────────────────────
# 5. GAME OF LIFE
# ─────────────────────────────────────────────────────────────

def game_of_life(width=80, height=30, generations=100, fill_rate=0.3, delay=0.1):
    """Conway's Game of Life with colorful rendering."""
    print("\n" + rainbow_text("═══ 🧬 CONWAY'S GAME OF LIFE ═══"))
    print("  Press Ctrl+C to stop\n")
    time.sleep(1)
    
    grid = [[random.random() < fill_rate for _ in range(width)] for _ in range(height)]
    
    age = [[0] * width for _ in range(height)]
    
    try:
        for gen in range(generations):
            clear_screen()
            
            alive_count = sum(sum(row) for row in grid)
            header = f"  Generation: {gen} | Alive: {alive_count} | Density: {alive_count/(width*height)*100:.1f}%"
            print(rainbow_text("═══ 🧬 GAME OF LIFE ═══"))
            print(header)
            
            for y in range(height):
                line = ''
                for x in range(width):
                    if grid[y][x]:
                        a = min(age[y][x], 10)
                        hue = (a * 30) % 360
                        r, g, b = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
                        r, g, b = int(r * 255), int(g * 255), int(b * 255)
                        line += ansi_color(r, g, b) + '█'
                    else:
                        line += ansi_color(20, 20, 30) + '·'
                print(line + RESET)
            
            new_grid = [[False] * width for _ in range(height)]
            for y in range(height):
                for x in range(width):
                    neighbors = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:
                                continue
                            ny, nx = (y + dy) % height, (x + dx) % width
                            if grid[ny][nx]:
                                neighbors += 1
                    
                    if grid[y][x]:
                        new_grid[y][x] = neighbors in (2, 3)
                    else:
                        new_grid[y][x] = neighbors == 3
                    
                    if new_grid[y][x]:
                        age[y][x] = age[y][x] + 1 if grid[y][x] else 0
                    else:
                        age[y][x] = 0
            
            grid = new_grid
            time.sleep(delay)
            
    except KeyboardInterrupt:
        print(f"\n{RESET}Simulation stopped at generation {gen}.")

# ─────────────────────────────────────────────────────────────
# 6. STRANGE ATTRACTOR (Lorenz)
# ─────────────────────────────────────────────────────────────

def lorenz_attractor(width=120, height=50, steps=15000,
                     sigma=10.0, rho=28.0, beta=8.0/3.0, dt=0.005):
    """Render the Lorenz strange attractor projected to 2D ASCII."""
    print("\n" + rainbow_text("═══ 🌪️ LORENZ STRANGE ATTRACTOR ═══"))
    print(f"  σ={sigma}, ρ={rho}, β={beta:.4f}\n")
    
    x, y, z = 0.1, 0.0, 0.0
    
    points = []
    for _ in range(steps):
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        x += dx * dt
        y += dy * dt
        z += dz * dt
        points.append((x, z, y))  # project x,z
    
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    
    canvas = [[0 for _ in range(width)] for _ in range(height)]
    point_time = [[0 for _ in range(width)] for _ in range(height)]
    
    for i, (px, py, _) in enumerate(points):
        col = int((px - x_min) / (x_max - x_min + 1e-10) * (width - 1))
        row = int((py - y_min) / (y_max - y_min + 1e-10) * (height - 1))
        col = max(0, min(width - 1, col))
        row = max(0, min(height - 1, row))
        canvas[row][col] += 1
        point_time[row][col] = i
    
    density_chars = ' ·∙•●◉⬤█'
    
    for row_idx in range(height):
        line = ''
        for col_idx in range(width):
            density = canvas[row_idx][col_idx]
            if density == 0:
                line += ' '
            else:
                t = point_time[row_idx][col_idx] / steps
                hue = t * 0.8
                r, g, b = colorsys.hsv_to_rgb(hue, 1.0, min(1.0, 0.3 + density * 0.15))
                r, g, b = int(r * 255), int(g * 255), int(b * 255)
                char_idx = min(len(density_chars) - 1, density)
                line += ansi_color(r, g, b) + density_chars[char_idx]
        print(line + RESET)

# ─────────────────────────────────────────────────────────────
# 7. MATRIX RAIN
# ─────────────────────────────────────────────────────────────

def matrix_rain(width=80, height=30, duration=200, delay=0.05):
    """The classic Matrix digital rain effect."""
    print("\n" + rainbow_text("═══ 💊 MATRIX RAIN ═══"))
    print("  Press Ctrl+C to stop\n")
    time.sleep(1)
    
    chars = 'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEF'
    
    columns = [{'y': random.randint(-height, 0), 
                'speed': random.randint(1, 3),
                'length': random.randint(5, 20)} 
               for _ in range(width)]
    
    try:
        for frame in range(duration):
            clear_screen()
            screen = [[(' ', 0) for _ in range(width)] for _ in range(height)]
            
            for col_idx, col in enumerate(columns):
                head_y = col['y']
                
                for i in range(col['length']):
                    y = head_y - i
                    if 0 <= y < height:
                        char = random.choice(chars)
                        if i == 0:
                            screen[y][col_idx] = (char, 3)  # bright head
                        elif i < 3:
                            screen[y][col_idx] = (char, 2)  # bright
                        else:
                            screen[y][col_idx] = (char, 1)  # dim
                
                col['y'] += col['speed']
                
                if col['y'] - col['length'] > height:
                    col['y'] = random.randint(-20, -1)
                    col['speed'] = random.randint(1, 3)
                    col['length'] = random.randint(5, 20)
            
            for row in screen:
                line = ''
                for char, brightness in row:
                    if brightness == 0:
                        line += ansi_color(0, 20, 0) + '·'
                    elif brightness == 1:
                        line += ansi_color(0, 100, 0) + char
                    elif brightness == 2:
                        line += ansi_color(0, 200, 0) + char
                    else:
                        line += ansi_color(200, 255, 200) + char
                print(line + RESET)
            
            time.sleep(delay)
    
    except KeyboardInterrupt:
        print(f"\n{RESET}Unplugged from the Matrix.")

# ─────────────────────────────────────────────────────────────
# 8. PLASMA EFFECT
# ─────────────────────────────────────────────────────────────

def plasma_effect(width=80, height=30, frames=150, delay=0.05):
    """Animated plasma effect using sine waves and true color."""
    print("\n" + rainbow_text("═══ 🌈 PLASMA EFFECT ═══"))
    print("  Press Ctrl+C to stop\n")
    time.sleep(1)
    
    chars = ' ░▒▓█▓▒░'
    
    try:
        for frame in range(frames):
            clear_screen()
            t = frame * 0.1
            
            for y in range(height):
                line = ''
                for x in range(width):
                    v1 = math.sin(x * 0.05 + t)
                    v2 = math.sin(y * 0.08 + t * 0.7)
                    v3 = math.sin((x * 0.05 + y * 0.08) + t * 0.5)
                    v4 = math.sin(math.sqrt((x - width/2)**2 + (y - height/2)**2) * 0.1 + t)
                    
                    v = (v1 + v2 + v3 + v4) / 4.0
                    
                    hue = (v + 1) / 2.0
                    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                    r, g, b = int(r * 255), int(g * 255), int(b * 255)
                    
                    char_idx = int((v + 1) / 2 * (len(chars) - 1))
                    line += ansi_bg(r, g, b) + ansi_color(255-r, 255-g, 255-b) + chars[char_idx]
                
                print(line + RESET)
            
            time.sleep(delay)
    
    except KeyboardInterrupt:
        print(f"\n{RESET}Plasma cooled down.")

# ─────────────────────────────────────────────────────────────
# 9. RANDOM WALK ART
# ─────────────────────────────────────────────────────────────

def random_walk_art(width=100, height=40, walkers=5, steps=5000):
    """Multiple random walkers painting on a canvas."""
    print("\n" + rainbow_text("═══ 🎨 RANDOM WALK ART ═══\n"))
    
    canvas = [[0 for _ in range(width)] for _ in range(height)]
    walker_id = [[0 for _ in range(width)] for _ in range(height)]
    
    positions = [(width // 2, height // 2) for _ in range(walkers)]
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for step in range(steps):
        for w in range(walkers):
            x, y = positions[w]
            dx, dy = random.choice(directions)
            
            # Drunk walk with momentum
            if random.random() < 0.3:
                dx, dy = random.choice(directions)
            
            x = max(0, min(width - 1, x + dx))
            y = max(0, min(height - 1, y + dy))
            positions[w] = (x, y)
            canvas[y][x] += 1
            walker_id[y][x] = w + 1
    
    paint = ' ·∙•●◉⬤█'
    walker_hues = [i / walkers for i in range(walkers)]
    
    for y in range(height):
        line = ''
        for x in range(width):
            density = canvas[y][x]
            if density == 0:
                line += ' '
            else:
                w = walker_id[y][x] - 1
                hue = walker_hues[w]
                brightness = min(1.0, 0.3 + density * 0.1)
                r, g, b = colorsys.hsv_to_rgb(hue, 0.8, brightness)
                r, g, b = int(r * 255), int(g * 255), int(b * 255)
                char_idx = min(len(paint) - 1, density)
                line += ansi_color(r, g, b) + paint[char_idx]
        print(line + RESET)

# ─────────────────────────────────────────────────────────────
# 10. LANGTON'S ANT
# ─────────────────────────────────────────────────────────────

def langtons_ant(width=100, height=45, steps=12000):
    """Simulate Langton's Ant — order from chaos!"""
    print("\n" + rainbow_text("═══ 🐜 LANGTON'S ANT ═══"))
    print(f"  Steps: {steps}\n")
    
    grid = [[False] * width for _ in range(height)]
    visit_time = [[0] * width for _ in range(height)]
    
    x, y = width // 2, height // 2
    direction = 0  # 0=up, 1=right, 2=down, 3=left
    dx_map = [0, 1, 0, -1]
    dy_map = [-1, 0, 1, 0]
    
    for step in range(steps):
        if 0 <= x < width and 0 <= y < height:
            if grid[y][x]:  # white → turn right
                direction = (direction + 1) % 4
            else:  # black → turn left
                direction = (direction - 1) % 4
            
            grid[y][x] = not grid[y][x]
            visit_time[y][x] = step
            
            x += dx_map[direction]
            y += dy_map[direction]
        else:
            break
    
    for row_idx in range(height):
        line = ''
        for col_idx in range(width):
            if grid[row_idx][col_idx]:
                t = visit_time[row_idx][col_idx] / steps
                hue = t * 0.7
                r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
                r, g, b = int(r * 255), int(g * 255), int(b * 255)
                line += ansi_color(r, g, b) + '█'
            else:
                if visit_time[row_idx][col_idx] > 0:
                    line += ansi_color(40, 40, 50) + '░'
                else:
                    line += ' '
        print(line + RESET)
    
    print(f"\n  Ant final position: ({x}, {y}), facing: {['↑','→','↓','←'][direction]}")

# ─────────────────────────────────────────────────────────────
# 11. HASH ART
# ─────────────────────────────────────────────────────────────

def hash_art(seed="chaos", width=80, height=30):
    """Generate deterministic art from a hash seed."""
    print("\n" + rainbow_text(f'═══ 🔑 HASH ART (seed: "{seed}") ═══\n'))
    
    blocks = '░▒▓█▀▄▌▐■□▪▫●○◐◑◒◓╱╲╳'
    
    for y in range(height):
        line = ''
        for x in range(width):
            data = f"{seed}:{x}:{y}"
            h = hashlib.sha256(data.encode()).hexdigest()
            
            val = int(h[:2], 16)
            char_idx = val % len(blocks)
            
            r = int(h[2:4], 16)
            g = int(h[4:6], 16)
            b = int(h[6:8], 16)
            
            # Make colors more vivid
            r = min(255, r + 50)
            g = min(255, g + 50)
            b = min(255, b + 50)
            
            line += ansi_color(r, g, b) + blocks[char_idx]
        print(line + RESET)

# ─────────────────────────────────────────────────────────────
# 12. FIBONACCI SPIRAL (ASCII)
# ─────────────────────────────────────────────────────────────

def fibonacci_spiral(width=100, height=45, max_points=2000):
    """Plot a Fibonacci/golden spiral."""
    print("\n" + rainbow_text("═══ 🐚 FIBONACCI SPIRAL ═══\n"))
    
    canvas = [[' ' for _ in range(width)] for _ in range(height)]
    
    golden_angle = 137.508  # degrees
    
    for i in range(max_points):
        r = math.sqrt(i) * 1.5
        theta = math.radians(i * golden_angle)
        
        x = int(r * math.cos(theta) + width / 2)
        y = int(r * math.sin(theta) * 0.5 + height / 2)
        
        if 0 <= x < width and 0 <= y < height:
            canvas[y][x] = '•'
    
    for row_idx, row in enumerate(canvas):
        line = ''
        for col_idx, char in enumerate(row):
            if char != ' ':
                dist = math.sqrt((col_idx - width/2)**2 + (row_idx - height/2)**2)
                hue = (dist * 0.02) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                r, g, b = int(r * 255), int(g * 255), int(b * 255)
                line += ansi_color(r, g, b) + char
            else:
                line += ' '
        print(line + RESET)

# ─────────────────────────────────────────────────────────────
# 13. BIFURCATION DIAGRAM (Logistic Map)
# ─────────────────────────────────────────────────────────────

def bifurcation_diagram(width=120, height=45, r_min=2.5, r_max=4.0, 
                         warmup=200, iterations=100):
    """Plot the bifurcation diagram of the logistic map."""
    print("\n" + rainbow_text("═══ 📊 BIFURCATION DIAGRAM (Logistic Map) ═══"))
    print(f"  r ∈ [{r_min}, {r_max}], x(n+1) = r·x(n)·(1-x(n))\n")
    
    canvas = [[0 for _ in range(width)] for _ in range(height)]
    
    for col in range(width):
        r = r_min + (r_max - r_min) * col / width
        x = 0.5
        
        for _ in range(warmup):
            x = r * x * (1 - x)
        
        for _ in range(iterations):
            x = r * x * (1 - x)
            row = int((1 - x) * (height - 1))
            row = max(0, min(height - 1, row))
            canvas[row][col] += 1
    
    for row_idx in range(height):
        line = ''
        for col_idx in range(width):
            density = canvas[row_idx][col_idx]
            if density == 0:
                line += ' '
            else:
                intensity = min(1.0, density * 0.15)
                r_val = r_min + (r_max - r_min) * col_idx / width
                hue = (r_val - r_min) / (r_max - r_min) * 0.8
                r, g, b = colorsys.hsv_to_rgb(hue, 1.0, intensity)
                r, g, b = int(r * 255), int(g * 255), int(b * 255)
                line += ansi_color(r, g, b) + '●'
        print(line + RESET)
    
    # X-axis labels
    label_line = ''
    for i in range(0, width, width // 6):
        r = r_min + (r_max - r_min) * i / width
        label = f'{r:.2f}'
        label_line += label + ' ' * (width // 6 - len(label))
    print(f"  r: {label_line}")

# ─────────────────────────────────────────────────────────────
# 14. FORTUNE COOKIE OF CHAOS
# ─────────────────────────────────────────────────────────────

def fortune_cookie():
    """Dispense chaotic wisdom."""
    fortunes = [
        "The butterfly you didn't notice just caused a hurricane in your codebase.",
        "In the fractal of life, you are both the Mandelbrot set and the divergent point.",
        "Entropy is not a bug — it's the universe's most consistent feature.",
        "Your code doesn't have bugs. It has emergent behavior.",
        "The logistic map says: between order and chaos, there's a beautiful mess.",
        "Every deterministic system is just chaos that hasn't been given enough time.",
        "The universe is under no obligation to make sense to you. Neither is this code.",
        "You are the strange attractor in someone's phase space.",
        "Rule 30 proves the universe can generate complexity from simplicity. So can you.",
        "In Conway's Game of Life, a glider once traveled forever. Be that glider.",
        "Chaos isn't randomness. It's sensitivity to initial conditions. Choose your start wisely.",
        "The Lorenz attractor never repeats. Neither should your excuses.",
        "Langton's Ant walked for 10,000 steps in chaos before finding its highway. Keep walking.",
        "Your pull request is like a cellular automaton: one small change cascades everywhere.",
        "Bifurcation point reached. Choose wisely. Or don't. Chaos doesn't judge.",
        "The golden ratio is everywhere. Including the ratio of your bugs to features.",
        "Sierpiński's triangle: proof that removing things can create beauty.",
        "You are one initial condition away from a completely different life trajectory.",
        "The Matrix rain is just the universe's console.log().",
        "Fractals: because God liked copy-paste but with style.",
    ]
    
    fortune = random.choice(fortunes)
    
    print("\n" + rainbow_text("═══ 🥠 FORTUNE COOKIE OF CHAOS ═══\n"))
    
    # Draw cookie
    cookie = [
        "       ╭─────────────────────────────────────────────╮",
        "      ╱                                               ╲",
        "     │                                                 │",
        "     │   {fortune_line_1:^49s}   │",
        "     │   {fortune_line_2:^49s}   │",
        "     │   {fortune_line_3:^49s}   │",
        "     │                                                 │",
        "      ╲                                               ╱",
        "       ╰─────────────────────────────────────────────╯",
    ]
    
    # Word wrap fortune
    words = fortune.split()
    lines = []
    current = ''
    for word in words:
        if len(current) + len(word) + 1 <= 45:
            current = current + ' ' + word if current else word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    
    while len(lines) < 3:
        lines.append('')
    
    for line in cookie:
        formatted = line.format(
            fortune_line_1=lines[0] if len(lines) > 0 else '',
            fortune_line_2=lines[1] if len(lines) > 1 else '',
            fortune_line_3=lines[2] if len(lines) > 2 else '',
        )
        print(ansi_color(255, 200, 50) + formatted + RESET)
    
    print()

# ─────────────────────────────────────────────────────────────
# 15. DNA HELIX
# ─────────────────────────────────────────────────────────────

def dna_helix(length=40, width=40):
    """Draw a colorful ASCII DNA double helix."""
    print("\n" + rainbow_text("═══ 🧬 DNA HELIX ═══\n"))
    
    pairs = [('A', 'T'), ('T', 'A'), ('G', 'C'), ('C', 'G')]
    pair_colors = {
        'A': ansi_color(255, 100, 100),
        'T': ansi_color(100, 100, 255),
        'G': ansi_color(100, 255, 100),
        'C': ansi_color(255, 255, 100),
    }
    
    center = width // 2
    amplitude = width // 4
    
    for i in range(length):
        pos1 = int(center + amplitude * math.sin(i * 0.3))
        pos2 = int(center - amplitude * math.sin(i * 0.3))
        
        left = min(pos1, pos2)
        right = max(pos1, pos2)
        
        pair = random.choice(pairs)
        
        line = [' '] * (width + 1)
        
        # Draw connecting bonds
        if abs(right - left) > 2:
            for j in range(left + 1, right):
                line[j] = ansi_color(80, 80, 80) + '─' + RESET
        
        # Draw nucleotides
        line[left] = pair_colors[pair[0]] + pair[0] + RESET
        line[right] = pair_colors[pair[1]] + pair[1] + RESET
        
        print(''.join(line))

# ─────────────────────────────────────────────────────────────
# 16. CHAOS STATISTICS
# ─────────────────────────────────────────────────────────────

def chaos_statistics():
    """Show fun random statistics about your chaos session."""
    print("\n" + rainbow_text("═══ 📈 CHAOS STATISTICS ═══\n"))
    
    entropy = random.uniform(0, 100)
    chaos_level = random.choice(['MILD', 'MODERATE', 'SEVERE', 'CRITICAL', 'TRANSCENDENT'])
    butterflies = random.randint(1, 10**6)
    parallel_universes = random.randint(1, 10**15)
    bugs_created = random.randint(0, 999)
    fractals_found = random.uniform(1.0, 3.0)
    meaning_of_life = random.choice([42, 'undefined', 'NaN', '∞', 'segfault', '¯\\_(ツ)_/¯'])
    
    stats = [
        f"  🌡️  Entropy Level:          {entropy:.2f}%",
        f"  🌀  Chaos Classification:   {chaos_level}",
        f"  🦋  Butterflies Disturbed:  {butterflies:,}",
        f"  🌌  Parallel Universes:     {parallel_universes:,}",
        f"  🐛  Bugs Created:           {bugs_created}",
        f"  📐  Fractal Dimension:      {fractals_found:.6f}",
        f"  🤔  Meaning of Life:        {meaning_of_life}",
        f"  ⏰  Time Until Heat Death:  {random.uniform(1, 10):.2e} × 10^100 years",
        f"  🎲  Lucky Number:           {random.randint(-999, 999)}",
        f"  🔮  Today's Prophecy:       {'Good' if random.random() > 0.5 else 'Doomed'}",
    ]
    
    for stat in stats:
        r = random.randint(150, 255)
        g = random.randint(150, 255)
        b = random.randint(150, 255)
        print(ansi_color(r, g, b) + stat + RESET)
        time.sleep(0.15)

# ─────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────

def print_banner():
    banner = r"""
   ██████╗██╗  ██╗ █████╗  ██████╗ ███████╗
  ██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔════╝
  ██║     ███████║███████║██║   ██║███████╗
  ██║     ██╔══██║██╔══██║██║   ██║╚════██║
  ╚██████╗██║  ██║██║  ██║╚██████╔╝███████║
   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
  ███╗   ███╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗███████╗
  ████╗ ████║██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝
  ██╔████╔██║███████║██║     ███████║██║██╔██╗ ██║█████╗
  ██║╚██╔╝██║██╔══██║██║     ██╔══██║██║██║╚██╗██║██╔══╝
  ██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║██║ ╚████║███████╗
  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
    """
    print(rainbow_text(banner))

def main():
    while True:
        clear_screen()
        print_banner()
        
        menu_items = [
            ("1", "🌀 Mandelbrot Set", "Fractal beauty in ASCII"),
            ("2", "🔬 Cellular Automaton", "1D automata (Rule 30, 90, 110...)"),
            ("3", "👾 Glitch Text", "Zalgo-style text corruption"),
            ("4", "🎲 Chaos Game", "Sierpiński triangle & more"),
            ("5", "🧬 Game of Life", "Conway's classic (animated)"),
            ("6", "🌪️  Lorenz Attractor", "Strange attractor visualization"),
            ("7", "💊 Matrix Rain", "Digital rain animation"),
            ("8", "🌈 Plasma Effect", "Animated plasma waves"),
            ("9", "🎨 Random Walk Art", "Drunk walkers painting"),
            ("10", "🐜 Langton's Ant", "Order from chaos"),
            ("11", "🔑 Hash Art", "Deterministic art from text"),
            ("12", "🐚 Fibonacci Spiral", "Golden angle phyllotaxis"),
            ("13", "📊 Bifurcation Diagram", "Logistic map chaos"),
            ("14", "🥠 Fortune Cookie", "Chaotic wisdom"),
            ("15", "🧬 DNA Helix", "Double helix art"),
            ("16", "📈 Chaos Stats", "Your chaos metrics"),
            ("A",  "🌟 RUN ALL (static)", "Run all non-animated demos"),
            ("Q",  "🚪 Quit", "Return to boring reality"),
        ]
        
        for item in menu_items:
            num, title, desc = item
            color = ansi_color(100, 200, 255) if num.isdigit() else ansi_color(255, 200, 100)
            print(f"  {color}[{num:>2}]{RESET}  {title:<28s} {ansi_color(150,150,150)}{desc}{RESET}")
        
        print()
        choice = input(f"  {ansi_color(255,255,100)}Choose your chaos ▶ {RESET}").strip().upper()
        
        actions = {
            '1': lambda: mandelbrot(),
            '2': lambda: (
                cellular_automaton(rule=int(input("  Rule number (0-255) [30]: ").strip() or "30"))
            ),
            '3': lambda: glitch_text(
                text=input("  Text to glitch [CHAOS MACHINE]: ").strip() or "CHAOS MACHINE",
                intensity=int(input("  Intensity (1-10) [5]: ").strip() or "5")
            ),
            '4': lambda: chaos_game(
                n_vertices=int(input("  Number of vertices (3-6) [3]: ").strip() or "3"),
                ratio=float(input("  Jump ratio (0.1-0.9) [0.5]: ").strip() or "0.5")
            ),
            '5': lambda: game_of_life(),
            '6': lambda: lorenz_attractor(),
            '7': lambda: matrix_rain(),
            '8': lambda: plasma_effect(),
            '9': lambda: random_walk_art(),
            '10': lambda: langtons_ant(),
            '11': lambda: hash_art(
                seed=input("  Seed text [chaos]: ").strip() or "chaos"
            ),
            '12': lambda: fibonacci_spiral(),
            '13': lambda: bifurcation_diagram(),
            '14': lambda: fortune_cookie(),
            '15': lambda: dna_helix(),
            '16': lambda: chaos_statistics(),
        }
        
        if choice == 'Q':
            clear_screen()
            print(rainbow_text("\n  Thanks for embracing the chaos! 🌀\n"))
            fortune_cookie()
            break
        elif choice == 'A':
            # Run all static (non-animated) demos
            static_demos = ['1', '2', '3', '4', '6', '9', '10', '11', '12', '13', '14', '15', '16']
            for key in static_demos:
                actions[key]()
                print(f"\n{'─' * 60}\n")
            input("\n  Press Enter to continue...")
        elif choice in actions:
            try:
                actions[choice]()
            except Exception as e:
                print(f"\n  {ansi_color(255,50,50)}Chaos error: {e}{RESET}")
            input("\n  Press Enter to continue...")
        else:
            print(f"\n  {ansi_color(255,50,50)}Invalid choice. Chaos demands valid input!{RESET}")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RESET}Chaos interrupted. The universe continues without you.\n")
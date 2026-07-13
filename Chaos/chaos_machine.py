import random, math, time, os, sys, hashlib, colorsys

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def ac(r, g, b): return f'\033[38;2;{r};{g};{b}m'
R = '\033[0m'

def rt(text):
    c = ['\033[91m','\033[93m','\033[92m','\033[96m','\033[94m','\033[95m']
    return ''.join(c[i%len(c)]+ch if ch not in ' \n' else ch for i,ch in enumerate(text))+R

def mandelbrot(w=120, h=40, mi=50):
    print(rt("\nMANDELBROT SET\n"))
    ch = ' .:-=+*#%@█'
    for row in range(h):
        line = ''
        for col in range(w):
            x0 = -2.5 + 3.5*col/w; y0 = -1.2 + 2.4*row/h
            x=y=0.0; it=0
            while x*x+y*y<=4 and it<mi:
                x,y = x*x-y*y+x0, 2*x*y+y0; it+=1
            if it==mi: line += ' '
            else:
                r,g,b = [int(c*255) for c in colorsys.hsv_to_rgb(it/mi,1,1)]
                line += ac(r,g,b)+ch[it*(len(ch)-1)//mi]
        print(line+R)

def cellauto(rule=30, w=120, g=50):
    print(rt(f"CELLULAR AUTOMATON (Rule {rule})"))
    rb = format(rule,'08b')
    rs = {format(7-i,'03b'):int(rb[i]) for i in range(8)}
    s = [0]*w; s[w//2]=1
    cs = [ac(255,50,50),ac(255,150,0),ac(255,255,0),ac(0,255,100),ac(0,150,255),ac(150,0,255)]
    for gen in range(g):
        print(cs[gen%len(cs)]+''.join('█' if c else ' ' for c in s)+R)
        s = [rs[f'{s[(i-1)%w]}{s[i]}{s[(i+1)%w]}'] for i in range(w)]

def glitch(t="CHAOS MACHINE", n=5, l=15):
    print(rt("\nGLITCH TEXT\n"))
    zu = [chr(i) for i in range(0x0300,0x0340)]
    zd = [chr(i) for i in range(0x0316,0x0340)]
    gc = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'
    for _ in range(l):
        gl = ''
        ni = random.randint(1,n)
        for ch in t:
            if random.random()<0.15: ch=random.choice(gc)
            gl+=ch
            for _ in range(random.randint(0,ni)): gl+=random.choice(zu)
            for _ in range(random.randint(0,ni//2)): gl+=random.choice(zd)
        print(ac(random.randint(100,255),random.randint(0,100),random.randint(100,255))+' '*random.randint(0,20)+gl+R)

def chaos_game(n=3, r=0.5, w=120, h=55, pts=8000):
    print(rt(f"\nCHAOS GAME ({n} verts, r={r})\n"))
    c = [[' ']*w for _ in range(h)]
    verts = [(int((math.cos(2*math.pi*i/n-math.pi/2)*0.45+0.5)*(w-1)),
              int((math.sin(2*math.pi*i/n-math.pi/2)*0.45+0.5)*(h-1))) for i in range(n)]
    x,y = random.random()*w, random.random()*h
    for _ in range(pts):
        vx,vy = random.choice(verts)
        x += (vx-x)*r; y += (vy-y)*r
        px,py = int(x),int(y)
        if 0<=px<w and 0<=py<h: c[py][px]='•'
    for vx,vy in verts:
        if 0<=vx<w and 0<=vy<h: c[vy][vx]='◆'
    g = [ac(50,0,80),ac(100,0,150),ac(150,50,200),ac(200,100,255),ac(255,150,255)]
    for i,row in enumerate(c): print(g[i*len(g)//h]+''.join(row)+R)

def gol(w=80, h=30, g=100, d=0.1):
    print(rt("\nGAME OF LIFE\n")); time.sleep(1)
    grid = [[random.random()<0.3 for _ in range(w)] for _ in range(h)]
    age = [[0]*w for _ in range(h)]
    try:
        for gen in range(g):
            clear()
            print(rt("GAME OF LIFE"))
            print(f"  Gen {gen} | Alive {sum(sum(r) for r in grid)}")
            for y in range(h):
                line = ''
                for x in range(w):
                    if grid[y][x]:
                        a = min(age[y][x],10)
                        rv,gv,bv = [int(c*255) for c in colorsys.hsv_to_rgb((a*30)%360/360,1,1)]
                        line += ac(rv,gv,bv)+'█'
                    else: line += ac(20,20,30)+'·'
                print(line+R)
            ng = [[False]*w for _ in range(h)]
            for y in range(h):
                for x in range(w):
                    n = sum(grid[(y+dy)%h][(x+dx)%w] for dy in(-1,0,1) for dx in(-1,0,1) if dy or dx)
                    ng[y][x] = n==3 or (grid[y][x] and n==2)
                    age[y][x] = age[y][x]+1 if ng[y][x] and grid[y][x] else 0 if not ng[y][x] else 0
            grid = ng; time.sleep(d)
    except KeyboardInterrupt: pass

def lorenz(w=120, h=50, s=15000):
    print(rt("\nLORENZ ATTRACTOR\n"))
    x,y,z=0.1,0.0,0.0; pts=[]
    for _ in range(s):
        x+=10*(y-x)*0.005; y+=x*(28-z)*0.005-y*0.005; z+=x*y*0.005-8/3*z*0.005
        pts.append((x,z))
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    xm,xM=min(xs),max(xs); ym,yM=min(ys),max(ys)
    cv=[[0]*w for _ in range(h)]; pt=[[0]*w for _ in range(h)]
    ch=' ·∙•●◉⬤█'
    for i,(px,py) in enumerate(pts):
        c = int((px-xm)/(xM-xm+1e-10)*(w-1))
        r = int((py-ym)/(yM-ym+1e-10)*(h-1))
        c=max(0,min(w-1,c)); r=max(0,min(h-1,r))
        cv[r][c]+=1; pt[r][c]=i
    for ri in range(h):
        line=''
        for ci in range(w):
            d=cv[ri][ci]
            if not d: line+=' '
            else:
                t=pt[ri][ci]/s
                rv,gv,bv=[int(c*255) for c in colorsys.hsv_to_rgb(t*0.8,1,min(1,0.3+d*0.15))]
                line+=ac(rv,gv,bv)+ch[min(len(ch)-1,d)]
        print(line+R)

def matrix(w=80, h=30, dur=200, d=0.05):
    print(rt("\nMATRIX RAIN\n")); time.sleep(1)
    cc = 'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEF'
    cols = [{'y':random.randint(-h,0),'sp':random.randint(1,3),'ln':random.randint(5,20)} for _ in range(w)]
    try:
        for _ in range(dur):
            clear()
            sc = [[(' ',0) for _ in range(w)] for _ in range(h)]
            for ci,co in enumerate(cols):
                for i in range(co['ln']):
                    y = co['y']-i
                    if 0<=y<h: sc[y][ci] = (random.choice(cc), 3 if i==0 else 2 if i<3 else 1)
                co['y']+=co['sp']
                if co['y']-co['ln']>h:
                    co['y']=random.randint(-20,-1); co['sp']=random.randint(1,3); co['ln']=random.randint(5,20)
            for row in sc:
                print(''.join(ac(0,20,0)+'·' if b==0 else ac(0,100,0)+ch if b==1 else ac(0,200,0)+ch if b==2 else ac(200,255,200)+ch for ch,b in row)+R)
            time.sleep(d)
    except KeyboardInterrupt: pass

def plasma(w=80, h=30, f=150, d=0.05):
    print(rt("\nPLASMA\n")); time.sleep(1)
    ch=' ░▒▓█▓▒░'
    try:
        for frame in range(f):
            clear(); t=frame*0.1
            for y in range(h):
                line=''
                for x in range(w):
                    v = (math.sin(x*0.05+t)+math.sin(y*0.08+t*0.7)+math.sin((x*0.05+y*0.08)+t*0.5)+math.sin(math.hypot(x-w/2,y-h/2)*0.1+t))/4
                    rv,gv,bv = [int(c*255) for c in colorsys.hsv_to_rgb((v+1)/2,1,1)]
                    line += f'\033[48;2;{rv};{gv};{bv}m'+ac(255-rv,255-gv,255-bv)+ch[int((v+1)/2*(len(ch)-1))]
                print(line+R)
            time.sleep(d)
    except KeyboardInterrupt: pass

def walk_art(w=100, h=40, wk=5, st=5000):
    print(rt("\nRANDOM WALK ART\n"))
    cv=[[0]*w for _ in range(h)]; wid=[[0]*w for _ in range(h)]
    pos=[(w//2,h//2) for _ in range(wk)]
    dirs=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    for _ in range(st):
        for wi in range(wk):
            x,y=pos[wi]
            if random.random()<0.3: dx,dy=random.choice(dirs)
            else: dx,dy=random.choice(dirs)
            x=max(0,min(w-1,x+dx)); y=max(0,min(h-1,y+dy))
            pos[wi]=(x,y); cv[y][x]+=1; wid[y][x]=wi+1
    pt=' ·∙•●◉⬤█'
    wh=[i/wk for i in range(wk)]
    for y in range(h):
        print(''.join(' ' if cv[y][x]==0 else ac(*[int(c*255) for c in colorsys.hsv_to_rgb(wh[wid[y][x]-1],0.8,min(1,0.3+cv[y][x]*0.1))])+pt[min(len(pt)-1,cv[y][x])] for x in range(w))+R)

def ant(w=100, h=45, st=12000):
    print(rt("\nLANGTON'S ANT\n"))
    g=[[False]*w for _ in range(h)]; vt=[[0]*w for _ in range(h)]
    x,y=w//2,h//2; d=0
    dm=[(0,-1),(1,0),(0,1),(-1,0)]
    for s in range(st):
        if 0<=x<w and 0<=y<h:
            d=(d+1)%4 if g[y][x] else (d-1)%4
            g[y][x]=not g[y][x]; vt[y][x]=s
            x+=dm[d][0]; y+=dm[d][1]
        else: break
    for ri in range(h):
        line=''
        for ci in range(w):
            if g[ri][ci]:
                rv,gv,bv=[int(c*255) for c in colorsys.hsv_to_rgb(vt[ri][ci]/st*0.7,0.9,0.9)]
                line+=ac(rv,gv,bv)+'█'
            else: line+=ac(40,40,50)+'░' if vt[ri][ci]>0 else ' '
        print(line+R)
    print(f"\n  Pos: ({x},{y}) facing: {['↑','→','↓','←'][d]}")

def hash_art(seed="chaos", w=80, h=30):
    print(rt(f"\nHASH ART (seed: {seed})\n"))
    bl='░▒▓█▀▄▌▐■□▪▫●○◐◑◒◓╱╲╳'
    for y in range(h):
        line=''
        for x in range(w):
            hx=hashlib.sha256(f"{seed}:{x}:{y}".encode()).hexdigest()
            line+=ac(*[min(255,int(hx[i:i+2],16)+50) for i in(2,4,6)])+bl[int(hx[:2],16)%len(bl)]
        print(line+R)

def fib_spiral(w=100, h=45, mp=2000):
    print(rt("\nFIBONACCI SPIRAL\n"))
    c=[[' ']*w for _ in range(h)]
    for i in range(mp):
        r=math.sqrt(i)*1.5; th=math.radians(i*137.508)
        x=int(r*math.cos(th)+w//2); y=int(r*math.sin(th)*0.5+h//2)
        if 0<=x<w and 0<=y<h: c[y][x]='•'
    for ri,row in enumerate(c):
        print(''.join(' ' if ch==' ' else ac(*[int(c*255) for c in colorsys.hsv_to_rgb(math.hypot(ci-w/2,ri-h/2)*0.02%1,1,1)])+ch for ci,ch in enumerate(row))+R)

def bifurcation(w=120, h=45, rm=2.5, rM=4.0):
    print(rt("\nBIFURCATION DIAGRAM\n"))
    cv=[[0]*w for _ in range(h)]
    for col in range(w):
        r=rm+(rM-rm)*col/w; x=0.5
        for _ in range(200): x=r*x*(1-x)
        for _ in range(100):
            x=r*x*(1-x)
            row=int((1-x)*(h-1)); row=max(0,min(h-1,row)); cv[row][col]+=1
    for ri in range(h):
        line=''
        for ci in range(w):
            d=cv[ri][ci]
            if not d: line+=' '
            else:
                hue=(rm+(rM-rm)*ci/w-rm)/(rM-rm)*0.8
                rv,gv,bv=[int(c*255) for c in colorsys.hsv_to_rgb(hue,1,min(1,d*0.15))]
                line+=ac(rv,gv,bv)+'●'
        print(line+R)
    ls=''.join(f'{rm+(rM-rm)*i/w:.2f}'.ljust(w//6) for i in range(0,w,w//6))
    print(f"  r: {ls}")

def fortune():
    f = [
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
        "Bifurcation point reached. Choose wisely. Or don't. Chaos doesn't judge.",
        "The golden ratio is everywhere. Including the ratio of your bugs to features.",
        "Sierpiński's triangle: proof that removing things can create beauty.",
        "You are one initial condition away from a completely different life trajectory.",
        "The Matrix rain is just the universe's console.log().",
        "Fractals: because God liked copy-paste but with style.",
    ]
    print(rt("\nFORTUNE COOKIE\n"))
    txt = random.choice(f)
    print(ac(255,200,50)+f"""
       ╭─────────────────────────────────────────────╮
      ╱                                               ╲
     │                                                 │
     │   {txt:^49s}   │
     │                                                 │
      ╲                                               ╱
       ╰─────────────────────────────────────────────╯
{RESET}""")

def dna(l=40, w=40):
    print(rt("\nDNA HELIX\n"))
    pc={'A':ac(255,100,100),'T':ac(100,100,255),'G':ac(100,255,100),'C':ac(255,255,100)}
    ctr=w//2; amp=w//4
    for i in range(l):
        p1=int(ctr+amp*math.sin(i*0.3)); p2=int(ctr-amp*math.sin(i*0.3))
        lft=min(p1,p2); rgt=max(p1,p2)
        pair=random.choice(['AT','TA','GC','CG'])
        line=[' ']*(w+1)
        for j in range(lft+1,rgt): line[j]=ac(80,80,80)+'─'+R
        line[lft]=pc[pair[0]]+pair[0]+R; line[rgt]=pc[pair[1]]+pair[1]+R
        print(''.join(line))

def stat():
    print(rt("\nCHAOS STATS\n"))
    for s in [
        f"  Entropy:          {random.uniform(0,100):.2f}%",
        f"  Chaos:           {random.choice(['MILD','MODERATE','SEVERE','CRITICAL','TRANSCENDENT'])}",
        f"  Butterflies:     {random.randint(1,10**6):,}",
        f"  Universes:       {random.randint(1,10**15):,}",
        f"  Bugs Created:    {random.randint(0,999)}",
        f"  Fractal Dim:     {random.uniform(1,3):.6f}",
        f"  Meaning of Life: {random.choice([42,'undefined','NaN','∞','segfault','¯\\_(ツ)_/¯'])}",
    ]:
        print(ac(random.randint(150,255),random.randint(150,255),random.randint(150,255))+s+R)
        time.sleep(0.15)

def banner():
    print(rt("""
  ╔══ CHAOS MACHINE ══╗
  ║ Fractals. Glitch. ║
  ║  Automata. Magic. ║
  ╚═══════════════════╝
"""))

def main():
    while True:
        clear(); banner()
        items = [
            ('1','Mandelbrot Set'), ('2','Cellular Automaton'), ('3','Glitch Text'),
            ('4','Chaos Game'), ('5','Game of Life'), ('6','Lorenz Attractor'),
            ('7','Matrix Rain'), ('8','Plasma Effect'), ('9','Random Walk Art'),
            ('10',"Langton's Ant"), ('11','Hash Art'), ('12','Fibonacci Spiral'),
            ('13','Bifurcation Diagram'), ('14','Fortune Cookie'), ('15','DNA Helix'),
            ('16','Chaos Stats'), ('A','Run All (static)'), ('Q','Quit'),
        ]
        for k,v in items:
            print(f"  {ac(100,200,255)}{k:>2}{R}  {v}")
        c = input(f"\n  {ac(255,255,100)}Choose ▶ {R}").strip().upper()
        if c=='Q': clear(); print(rt("\nThanks for the chaos! 🌀\n")); fortune(); break
        acts = {'1':lambda:mandelbrot(),'2':lambda:cellauto(int(input("Rule [30]: ").strip()or"30")),
                '3':lambda:glitch(input("Text [CHAOS]: ").strip()or"CHAOS",int(input("Intensity [5]: ").strip()or"5")),
                '4':lambda:chaos_game(int(input("Verts [3]: ").strip()or"3"),float(input("Ratio [0.5]: ").strip()or"0.5")),
                '5':gol,'6':lorenz,'7':matrix,'8':plasma,'9':walk_art,'10':ant,
                '11':lambda:hash_art(input("Seed [chaos]: ").strip()or"chaos"),
                '12':fib_spiral,'13':bifurcation,'14':fortune,'15':dna,'16':stat}
        if c=='A':
            for k in '12346910111213141516': acts[k](); print(f'\n{"─"*50}\n')
            input("\nEnter to continue...")
        elif c in acts:
            try: acts[c]()
            except Exception as e: print(f"\n{ac(255,50,50)}Error: {e}{R}")
            input("\nEnter to continue...")

if __name__=='__main__':
    try: main()
    except KeyboardInterrupt: print(f"\n{R}Chaos interrupted.\n")

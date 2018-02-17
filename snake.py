import curses
import random


def joc(scr):
    curses.curs_set(0)
    scr.attron(curses.A_BOLD)
    scr.clear()

    LINES = scr.getmaxyx()[0]
    COLS = scr.getmaxyx()[1]
    velocitat = 125

    class node_serp():
        def __init__(self, y = None, x = None):
            self.y = y
            self.x = x
            self.anterior = None
    class serp(object):
        def __init__(self, y, x):
            self.primer = node_serp(y, x + 1)
            self.ultim = node_serp(y, x)
            self.ultim.anterior = self.primer
            scr.addch(y, x, '#')
            scr.addch(y, x+1, '#')
            scr.refresh()
        def moure(self, dire):
            scr.addch(self.ultim.y, self.ultim.x, ' ')
            self.ultim = self.ultim.anterior
            nou_node = node_serp(self.primer.y, self.primer.x)
            if dire == 'RIGHT':
                nou_node.x += 1
            elif dire == 'LEFT':
                nou_node.x -= 1
            elif dire == 'TOP':
                nou_node.y -= 1
            else:
                nou_node.y += 1
            self.primer.anterior = nou_node
            self.primer = nou_node
            scr.addch(nou_node.y, nou_node.x, '#')
            scr.refresh()
        def comprovar(self, dire):
            xx = 0
            yy = 0
            if dire == 'RIGHT':
                yy = self.primer.y
                xx = self.primer.x + 1
            elif dire == 'LEFT':
                yy = self.primer.y
                xx = self.primer.x - 1
            elif dire == 'TOP':
                yy = self.primer.y - 1
                xx = self.primer.x
            else:
                yy = self.primer.y + 1
                xx = self.primer.x
            if yy < 1 or xx < 1 or yy >= LINES-1 or xx >= COLS-1:
                return False
            if (scr.inch(yy, xx) & curses.A_CHARTEXT) == ord('#'):
                return False
            return True
        def trobaFruita(self, dire):
            xx = 0
            yy = 0
            if dire == 'RIGHT':
                yy = self.primer.y
                xx = self.primer.x + 1
            elif dire == 'LEFT':
                yy = self.primer.y
                xx = self.primer.x - 1
            elif dire == 'TOP':
                yy = self.primer.y - 1
                xx = self.primer.x
            else:
                yy = self.primer.y + 1
                xx = self.primer.x
            if (scr.inch(yy, xx) & curses.A_CHARTEXT) == ord('@'):
                return True
            return False
        def menja(self, dire):
            nou_node = node_serp(self.primer.y, self.primer.x)
            if dire == 'RIGHT':
                nou_node.x += 1
            elif dire == 'LEFT':
                nou_node.x -= 1
            elif dire == 'TOP':
                nou_node.y -= 1
            else:
                nou_node.y += 1
            self.primer.anterior = nou_node
            self.primer = nou_node
            scr.addch(nou_node.y, nou_node.x, '#')
            scr.refresh()

    def gen_fruita():
        ch = ord('#')
        x = 5
        y = 5
        while ch == ord('#'):
            y = random.randint(1, LINES-2)
            x = random.randint(1,  COLS-2)
            ch = scr.inch(y, x) & curses.A_CHARTEXT
        scr.addch(y, x, '@')
    def ajustar_v():
        scr.timeout(-1)
        scr.clear()
        scr.addstr(int(LINES/2), int(COLS/2 -22), 'JOC CLASSIC: PREM UN NUMERO DEL 1 AL 8 (8 es el mes lent)')
        while True:
            ch = scr.getch()
            if ch == ord('1'):
                return 25
            elif ch == ord('2'):
                return 50
            elif ch == ord('3'):
                return 75
            elif ch == ord('4'):
                return 100
            elif ch == ord('5'):
                return 125
            elif ch == ord('6'):
                return 150
            elif ch == ord('7'):
                return 175
            elif ch == ord('8'):
                return 200
    def jugar():
        scr.clear()
        scr.addstr(int(LINES/2 -1), int(COLS/2 -10), 'EN QUALSEVOL MOMENT POTS CLICAR [q] PER TORNAR AL MENU')
        scr.refresh()
        curses.napms(1000)
        scr.clear()
        scr.box(0, 0)
        direccio = 'RIGHT'
        s = serp(2, 2)
        gen_fruita()

        scr.timeout(velocitat)
        ch = ''
        while ch != ord('q'):
            ch = scr.getch()
            if ch == curses.KEY_UP and direccio != 'BOTTOM':
                direccio = 'TOP'
            elif ch == curses.KEY_DOWN and direccio != 'TOP':
                direccio = 'BOTTOM'
            elif ch == curses.KEY_RIGHT and direccio != 'LEFT':
                direccio = 'RIGHT'
            elif ch == curses.KEY_LEFT and direccio != 'RIGHT':
                direccio = 'LEFT'
            if not s.comprovar(direccio):
                s.moure(direccio)
                break
            elif s.trobaFruita(direccio):
                s.menja(direccio)
                gen_fruita()
            else: s.moure(direccio)


        scr.timeout(-1)

    scr.addstr(int(LINES/2 -1), int(COLS/2 -8), 'JOC CLASSIC: SERP')
    scr.addstr(int(LINES/2 +1), int(COLS/2 -3), 'TIMTIM')
    scr.refresh()
    curses.napms(1000)

    scr.timeout(-1)
    ch = ''
    while ch != ord('q'):
        scr.addstr(int(LINES/2 -1), int(COLS/2 -11), 'PREM [ENTER] PER JUGAR')
        scr.addstr(int(LINES/2), int(COLS/2 -16), 'PREM [v] PER AJUSTAR LA VELOCITAT')
        scr.addstr(int(LINES/2 +1), int(COLS/2 -7), 'PREM [q] SORTIR')
        scr.refresh()
        ch = scr.getch()
        if ch == ord('v'):
            velocitat = ajustar_v()
            scr.clear()
            continue
        if ch == ord('\n'):
            jugar()

    scr.clear()
    scr.addstr(int(LINES/2 +1), int(COLS/2 -8), 'GRACIES PER JUGAR')
    scr.timeout(1000)
    scr.refresh()
    scr.getch()
    scr.attroff(curses.A_BOLD)

curses.wrapper(joc)

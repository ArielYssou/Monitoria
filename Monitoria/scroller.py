import curses

class Menu():
    def __init__(self, names = [], groups = [], rows = 0):
        self.students = []
        self.students = sorted(
                list(zip(names, ["{:>3}".format(gp) for gp in groups])),
                key = lambda x: (x[1], x[0])
                )
        # Groups are made into left-paded strings with 3 chars so sort will place 10 after 9 correctly. Finally sorts by group and then by name
        self.freqs = {}
        self.colors = {}
        self.light = 230
        self.dark = 230
        self.hname = ""
        self.hgroup = ""
        self.groups = [ "{}".format(num) + letter
            for num in range(1,12)
            for letter in ['A', 'B']] 

        for name, group in self.students:
            self.freqs[name] = '-'
            self.colors[name] = self.dark

        self.rows = rows
        self.middle = int(self.rows/2)

        self.empty =  ''
        self.freq = ''

    def initialize(self):
        '''
        Manually inserts empty lines to list to centerize it.
        Creates freq,group and colors for the sake of consistency
        albeit not doing so would not have any effects AFAIK
        '''
        self.freqs[self.empty] = self.empty
        self.colors[self.empty] = self.dark

        for index in range(self.middle):
            self.students.insert(0, (self.empty, self.empty))

        self.hname = self.students[self.middle][0]
        self.hgroup = self.students[self.middle][1]

    def up(self):
        if self.students[self.middle - 1][0] == self.empty:
            pass
        else:
            var = self.students.pop()
            self.students.insert(0, var)
        self.hname = self.students[self.middle][0]
        self.hgroup = self.students[self.middle][1]
        self.freq = ''

    def down(self):
        if self.students[self.middle + 1][0] == self.empty:
            pass
        else:
            var = self.students.pop(0)
            self.students.append(var)
        self.hname = self.students[self.middle][0]
        self.hgroup = self.students[self.middle][1]
        self.freq = ''

    def show(self, screen):
        '''
        Prints the menu in curses window
        '''
        # print doesn't work with curses, use addstr instead

        screen.refresh()
        screen.clear()
        for index in range(self.rows):
            name = self.students[index][0]
            group = self.students[index][1]
            line = ''
            clr = 0
            if index == self.middle:
                clr = 1
                line += "> "
                line += "{:30.25}".format(name)
                if self.freq == '':
                    line += "{:.3}".format(self.freqs[name])
                else:
                    line += "{:.3}".format(self.freq)
            else:
                clr = 2
                line += "{:30.25}".format(name)
                line += "{:3}".format(self.freqs[name])
            screen.addstr(index, 1, line, curses.color_pair(clr))
        screen.addstr(self.middle, 40, self.freq)
        screen.addstr(self.middle+1, 40, 
                self.freqs[self.students[self.middle][0]])

#        screen.addstr(20, 50,"Debug:") 
#        screen.addstr(21, 50,"menu freq: " + '-' + self.freq + '-') 
#        screen.addstr(22, 50, "Current freq:" + self.freqs[self.students[self.middle][0]])


    def __str__(self):
        print("\033[H\033[J",end = '')
        for index in range(self.rows):
            name = self.students[index][0]
            group = self.students[index][1]
            line = ''
            if index == self.middle:
                line += "\033[32;1m> "
                line += "{:30.25}".format(name)
                if self.freq == '':
                    line += "{:.3}\033[0m".format(self.freqs[name])
                else:
                    line += "{:.3}\033[0m".format(self.freq)
            else:
                line += f"\033[38;5;{self.colors[name]}m"
                line += "{:30.25}".format(name)
                line += "{:3}\033[0m".format(self.freqs[name])
            print(line)

class Keyboard():
    # Numeric keys: 97 - 122
    # Number keys:   48 - 57
    # Ctrl + up: 566 / Ctr + dn: 525
    # Enter key: 10
    # Esc Key: 27
    # Home: 262 End: 360
    def __init__(self):
        self.numeric = list(range(48,57))
        self.letters = list(range(97, 122))
        self.alphanumerical = self.numeric + self.letters
        self.enter = 10
        self.directions = [
                curses.KEY_RIGHT,
                curses.KEY_UP,
                curses.KEY_LEFT,
                curses.KEY_DOWN
                ]
        self.esc = 27
        self.home = 262
        self.end = 360

def frequency(names = [], groups = [], nusps = []):
    global sceren
    screen = curses.initscr() #initialize curses window
    rows, cols = screen.getmaxyx()

    curses.noecho() # Dont print pressed keys
    curses.cbreak() # respond to keys immediately (don't wait for enter)
    curses.start_color()
    if curses.has_colors() == True:
        curses.use_default_colors()
    screen.keypad(True) # map arrow keys to special values

    curses.init_pair(1, 2, -1)
    curses.init_pair(2, 255, -1)

    menu = Menu(names, groups, rows)
    menu.initialize()
    menu.show(screen)

    keyboard = Keyboard()
    try:
        while True:
            char = screen.getch()
            if char == keyboard.esc:
                curses.nocbreak(); screen.keypad(0); curses.echo()
                curses.endwin()
                break
            elif char == ord('0'):
                menu.freqs[menu.hname] = '0'
                menu.down()
            elif char in keyboard.alphanumerical:
                if char == ord('q'):
                    menu.freq = ''
                else:
                    menu.freq += chr(char)
            elif char == curses.KEY_UP:
                menu.up()
                menu.freq = ''
            elif char == curses.KEY_DOWN:
                menu.down()
                menu.freq = ''
            elif char == keyboard.enter:
                if menu.freq == '':
                    menu.freqs[menu.hname] = menu.hgroup
                    menu.down()
                else:
                    if menu.freq.upper() in menu.groups:
                        menu.freqs[menu.hname] = menu.freq.upper()
                        menu.down()
                    else:
                        menu.freqs[menu.hname] = '-'
                    menu.freq = ''
            else:
                menu.freq = ''
            menu.show(screen)

            if '-' not in menu.freqs.values():
                curses.nocbreak(); screen.keypad(0); curses.echo()
                curses.endwin()
                break
    finally:
        # shut down cleanly
        menu.show(screen)
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()
        print(menu.freqs)

if __name__ == '__main__':
    from modules.dummy_class import dummy_class

    names = []
    groups = []
    students = 30
    for name, group in dummy_class(students):
        names.append(name)
        groups.append(group)

    frequency(names, groups)
    exit(0)

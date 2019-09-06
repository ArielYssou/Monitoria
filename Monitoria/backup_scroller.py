import curses

class Menu():
    def __init__(self, names = [], nusps = [], groups = [], rows = 0):
        self.students = []
        self.students = sorted(
                list(zip(names, ["{:>3}".format(gp) for gp in groups])),
                key = lambda x: (x[1], x[0])
                )
        # Groups are made into left-paded strings with 3 chars so the 'sort' funtion will place 10 after 9 correctly and A groups before B. Finally sorts by group and then by name
        self.nusps = {}
        for name, nusp in list(zip(names, nusps)):
            self.nusps[name] = nusp
        self.freqs = {}

        # Defining colros
        self.hilight =  1
        curses.init_pair(self.hilight, 2, -1)
        self.present_A = 2
        curses.init_pair(self.present_A, 255, -1)
        self.present_B = 3
        curses.init_pair(self.present_B, 250, -1)
        self.absent_A = 4
        curses.init_pair(self.absent_A, 245, -1)
        self.absent_B = 5
        curses.init_pair(self.absent_B, 240, -1)

        # Geometry of the menu
        self.rows = rows
        self.middle = int(self.rows/2)

        self.empty =  ''
        self.freqs[self.empty] = self.empty

        self.groups = [ "{}".format(num) + letter
            for num in range(1,13)
            for letter in ['A', 'B']] 

        for name, group in self.students:
            self.freqs[name] = '-'

        # In order to always show the current student in the middle
        # we insert empty lines to 'fill' the screen. With the use 
        # of the 'curses' module this could be avoided, but it would
        # require some structural changes.
        for index in range(self.middle):
            self.students.insert(0, (self.empty, self.empty))
        for index in range(self.middle + len(names), self.rows):
            self.students.append((self.empty, self.empty))

        self.hname = ""
        self.hgroup = ""
        self.hname = self.students[self.middle][0]
        self.hgroup = self.students[self.middle][1]

        self.freq = ''

    def up(self):
        '''
        Moves the menu up by rearranging the array
        '''
        if self.students[self.middle - 1][0] == self.empty:
            pass
        else:
            var = self.students.pop()
            self.students.insert(0, var)
        self.hname = self.students[self.middle][0]
        self.hgroup = self.students[self.middle][1]
        self.freq = ''
    
    def rewind(self):
        while True:
            if self.students[self.middle - 1][0] == self.empty:
                break
            else:
                self.up()

    def down(self):
        '''
        Moves the menu down by rearranging the array
        '''
        if self.students[self.middle + 1][0] == self.empty:
            self.rewind()
            pass
        else:
            var = self.students.pop(0)
            self.students.append(var)
        self.hname = self.students[self.middle][0]
        self.hgroup = self.students[self.middle][1]
        self.freq = ''

    def tail(self):
        '''
        Moves the menu down to the next unacconted attedence.
        '''
        while self.freqs[self.hname] != '-':
            self.down()
            if '-' not in self.freqs.values():
                break
            #elif self.students[self.middle + 1][0] == self.empty:
                #break
            else:
                pass

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
                clr = self.hilight
                line += "> "
                line += "{:30.25}".format(name)
                if self.freq == '':
                    line += "{:.3}".format(self.freqs[name])
                else:
                    line += "{:.3}".format(self.freq)
            else:
                if self.freqs[name] == '-':
                    if 'A' in group:
                        clr = self.absent_A
                    else:
                        clr = self.absent_B
                else:
                    if 'A' in group:
                        clr = self.present_A
                    else:
                        clr = self.present_B

                line += "{:30.25}".format(name)
                line += "{:>3}".format(self.freqs[name])
            screen.addstr(index, 1, line, curses.color_pair(clr))

#        screen.addstr(20, 50,"Debug:") 
#        screen.addstr(21, 50,"menu freq: " + '-' + self.freq + '-') 
#        screen.addstr(22, 50, "Current freq:" + self.freqs[self.students[self.middle][0]])


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

def frequency(turma, aula = 0):
    names = []
    nusps = []
    groups = []
    for name, nusp, group in turma:
        names.append(name)
        nusps.append(nusp)
        groups.append(group)

    screen = curses.initscr() #initialize curses window
    rows, cols = screen.getmaxyx()

    curses.noecho() # Dont print pressed keys
    curses.cbreak() # respond to keys immediately (don't wait for enter)
    curses.start_color()
    if curses.has_colors() == True:
        curses.use_default_colors()
    screen.keypad(True) # map arrow keys to special values

    menu = Menu(names, nusps, groups, rows)
    menu.show(screen)

    keyboard = Keyboard()
    try:
        while True:
            char = screen.getch()
            if char == keyboard.esc:
                break
            elif char == ord('0'):
                menu.freqs[menu.hname] = '0'
                #menu.down()
                menu.tail()
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
                    #menu.down()
                    menu.tail()
                else:
                    if menu.freq.upper() in menu.groups:
                        menu.freqs[menu.hname] = menu.freq.upper()
                        #menu.down()
                        menu.tail()
                    else:
                        menu.freqs[menu.hname] = '-'
                    menu.freq = ''
            else:
                menu.freq = ''

            menu.show(screen)

            if '-' not in menu.freqs.values():
                break

    finally:
        # shut down cleanly
        menu.show(screen)
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()
        output_file = open(f'./grades/freqs/aula_{aula}.csv', "w+")
        for name, freq in menu.freqs.items():
            if name != menu.empty:
                output_file.write(f"{menu.nusps[name]},{freq.replace(' ','')}\n")
                print(f"{menu.nusps[name]},{freq.replace(' ','')}")
            else:
                pass
        output_file.close()

def round_name(name = '', end = True):
    names = name.title().split()
    if end:
        offset = 1
    else:
        offset = 0
    for index in range(1, len(names) - offset):
        names[index] = names[index][0] + '.'
    return ' '.join(names)


if __name__ == '__main__':
    from modules.dummy_class import dummy_class

    aula = 98
    students = 20
    turma = dummy_class(students)
    frequency(turma, aula)

    exit(0)

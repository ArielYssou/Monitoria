import curses

class Menu():
    def __init__(self, elements = [], default_values = [], rows = 0):
        self.elements = elements
        self.default_values = default_values
        self.rows = rows

        self.lines = []
        self.val_format = '{:>3}'
        self.lines = sorted(
                list(zip(elements, [self.val_format.format(val) for val in default_values])),
                key = lambda x: (x[1], x[0])
                )

        self.show_message = False
        self.message = ''

        # Defining colors
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
        self.middle = int(self.rows/2)

        self.current_values = {}
        for element, default_value in self.lines:
            self.current_values[element] = '-'

        self.empty =  ''
        self.current_values[self.empty] = self.empty

        # In order to always show the current element in the middle
        # we insert empty lines to 'fill' the screen. With the use 
        # of the 'curses' module this could be avoided, but it would
        # require some structural changes.
        for index in range(self.middle):
            self.lines.insert(0, (self.empty, self.empty))
        for index in range(self.middle + len(elements), self.rows):
            self.lines.append((self.empty, self.empty))

        self.buffer = ''

    def up(self):
        '''
        Moves the menu up by rearranging the array
        '''
        if self.lines[self.middle - 1][0] == self.empty:
            pass
        else:
            var = self.lines.pop()
            self.lines.insert(0, var)
        self.buffer = ''
    
    def rewind(self):
        while True:
            if self.lines[self.middle - 1][0] == self.empty:
                break
            else:
                self.up()

    def down(self):
        '''
        Moves the menu down by rearranging the array
        '''
        if self.lines[self.middle + 1][0] == self.empty:
            self.rewind()
            pass
        else:
            var = self.lines.pop(0)
            self.lines.append(var)
        self.buffer = ''

    def tail(self):
        '''
        Moves the menu down to the next unacconted element.
        '''
        while self.lines[self.middle][1] != '-':
            self.down()
            if '-' not in self.current_values:
                break
            #elif self.lines[self.middle + 1][0] == self.empty:
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
            elem = self.lines[index][0]
            value = self.lines[index][1]
            line = ''
            clr = 0
            if index == self.middle:
                clr = self.hilight
                line += "> "
                line += "{:30.25}".format(elem)
                if self.buffer == '':
                    line += "{:.3}".format(self.current_values[elem])
                else:
                    line += "{:.3}".format(self.buffer)
            else:
                if self.current_values[elem] == '-':
                    if 'A' in value:
                        clr = self.absent_A
                    else:
                        clr = self.absent_B
                else:
                    if 'A' in value:
                        clr = self.present_A
                    else:
                        clr = self.present_B

                line += "{:30.25}".format(elem)
                line += self.val_format.format(self.current_values[elem])
            screen.addstr(index, 1, line, curses.color_pair(clr))

        if self.show_message:
            screen.addstr(20, 50, "Message") 
            screen.addstr(21, 50, f"{self.message}") 
            #screen.addstr(21, 50,"menu buffer: " + '-' + self.buffer + '-') 
            #screen.addstr(22, 50, "Current buffer:" + self.current_values[self.lines[self.middle][0]])
            #screen.addstr(23, 50, "rows:" + str(self.rows))


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

def create_menu(elements = [], default_values = [], rows = 0): 
    '''
        Displays the Menu object in a curses window untill the stop condition is met. Returns a dic relating the elements to their final values
    '''

    screen = curses.initscr() #initialize curses window
    rows, cols = screen.getmaxyx()

    curses.noecho() # Dont print pressed keys
    curses.cbreak() # respond to keys immediately (don't wait for enter)
    curses.start_color()
    if curses.has_colors() == True:
        curses.use_default_colors()
    screen.keypad(True) # map arrow keys to special current_values

    menu = Menu(elements, default_values, rows)
    menu.show(screen)

    keyboard = Keyboard()
    try:
        while True:
            char = screen.getch()
            hlght_elem = menu.lines[menu.middle][0] # Shorthand notations for simplicity
            hlght_val = menu.lines[menu.middle][1] #
            if char == keyboard.esc:
                break
            elif char == ord('0'):
                menu.current_values[hlght_elem] = '0'
                #menu.down()
                menu.tail()
            elif char in keyboard.alphanumerical:
                if char == ord('q'):
                    menu.buffer = ''
                else:
                    menu.buffer += chr(char)
            elif char == curses.KEY_UP:
                menu.up()
                menu.buffer = ''
            elif char == curses.KEY_DOWN:
                menu.down()
                menu.buffer = ''
            elif char == keyboard.enter:
                if menu.buffer == '':
                    menu.current_values[hlght_elem] = hlght_val
                    #menu.down()
                    menu.tail()
                else:
                    if menu.buffer.upper() in menu.default_values:
                        menu.current_values[hlght_elem] = menu.buffer.upper()
                        #menu.down()
                        menu.tail()
                    else:
                        menu.current_values[hlght_elem] = '-'
                    menu.buffer = ''
            else:
                menu.buffer = ''

            menu.show(screen)

            if '-' not in menu.current_values.values():
                break

    finally:
        # shut down cleanly
        menu.show(screen)
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()
        return menu.current_values

def abbreviate_name(name = '', end = True):
    names = name.title().split()
    if end:
        offset = 1
    else:
        offset = 0
    for index in range(1, len(names) - offset):
        names[index] = names[index][0] + '.'
    return ' '.join(names)

import curses

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

def listener(char):
    # get the curses screen window
    screen = curses.initscr()
     
    # turn off input echoing
    curses.noecho()
     
    # respond to keys immediately (don't wait for enter)
    curses.cbreak()
     
    # map arrow keys to special values
    screen.keypad(True)
    keyboard = Keyboard()

    while True:
        try:
            char = screen.getch()
            if char == keyboard.esc:
                break
            elif char == curses.KEY_RIGHT:
                # print doesn't work with curses, use addstr instead
                screen.addstr(0, 0, 'right')
            elif char == curses.KEY_LEFT:
                screen.addstr(0, 0, 'left ')       
            elif char == curses.KEY_UP:
                screen.addstr(0, 0, 'up   ')       
            elif char == curses.KEY_DOWN:
                screen.addstr(0, 0, 'down ')
            else:
                print(char)
    finally:
        # shut down cleanly
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()

print(word)

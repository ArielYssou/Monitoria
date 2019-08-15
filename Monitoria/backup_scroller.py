from pynput import keyboard
from numpy.random import choice
from faker import Faker
from os import get_terminal_size

fake = Faker('pt_BR')
students = 30
groups = [ "{}".format(num) + letter
        for num in range(1,12)
        for letter in ['A', 'B']]
#fake.seed(1234)
#self.names = list(string.ascii_lowercase)

try:
    columns, rows = get_terminal_size(0)
except OSError:
    columns, rows = get_terminal_size(1)

class Menu():
    def __init__(self, names = [], groups = [], rows = 0):
        self.students = []
        self.students = sorted(list(zip(names, ["{:>3}".format(gp) for gp in groups])), key = lambda x: (x[1], x[0])) # Groups are made into left-paded strings with 3 chars so sort will place 10 after 9 correctly. Finally sorts by group and then by name
        self.freqs = {}
        self.colors = {}
        self.light = 230
        self.dark = 230
        for name, group in students:
            self.freqs[name] = '-'
            self.colors[name] = self.dark

        self.rows = rows
        self.middle = int(rows/2)
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

    def up(self):
        if self.students[self.middle - 1][0] == self.empty:
            pass
        else:
            var = self.students.pop()
            self.students.insert(0, var)

    def down(self):
        if self.students[self.middle + 1][0] == self.empty:
            pass
        else:
            var = self.students.pop(0)
            self.students.append(var)

    def show(self):
        print("\033[H\033[J",end = '')
        for index in range(self.rows):
            if index == self.middle:
                line = "\033[32;1m> "
                line += "{:30.25}".format(self.students[index])
                if self.freq == '':
                    line += "{:.3}\033[0m".format(self.freqs[names[index]])
                    print(line)
                else:
                    line += "{:.3}\033[0m".format(self.freq)
                    print(line)
            else:
                line = f"\033[38;5;{self.colors[names[index]]}m"
                line += "{:30.25}".format(self.names[index])
                line += "{:3}\033[0m".format(self.freqs[names[index]])
                print(line)

names = [ fake.name() for i in range(students) ]
groups = choice(groups, students)

mylist = []
mylist = list(zip(names, ["{:>3}".format(gp) for gp in groups]))  

print(mylist)
mylist =  sorted(mylist, key = lambda x: (x[1], x[0]))
print(mylist)

for idx, name group in mylist:
    print(f"{idx} {name} {group}")

print( '-' * 70 )
print(mylist[1])
exit(0)
global menu
menu = Menu(names, groups, rows)
menu.initialize()
menu.show()

def on_press(key):
    try:
        char = key.char
        if char == '0':
            menu.freqs[names[menu.middle]] = "0"
            menu.down()
        else:
            menu.freq += char
    except AttributeError:
        if key == keyboard.Key.up:
            menu.up()
            menu.freq = ''
        elif key == keyboard.Key.down:
            menu.down()
            menu.freq = ''
        elif key == keyboard.Key.enter:
            if menu.freq == '':
                menu.freqs[names[menu.middle]] = menu.groups[names[menu.middle]]
            else:
                menu.freqs[names[menu.middle]] = menu.freq
            menu.freq = ''
            menu.down()

def on_release(key):
    if key == keyboard.Key.esc or not '-' in menu.freqs.values():
        menu.show()
        return False
    else:
        menu.show()

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release, suppress=True) as listener:
    listener.join()

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

listener.start()


exit(0)

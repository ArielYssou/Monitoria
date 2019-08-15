# It's happening!

def show_class():
    from collections import defaultdict
    from threading import Event, Thread
    from pynput import keyboard
    from os import system

    class_file = open('./files/dummy_class.csv', 'r')

    groups = defaultdict(list)
    for line in class_file.read().splitlines():

        try:
            student, nusp, group = line.split(',')
        except ValueError:
            print('Warning, missing value in class file!')

        groups[group].append(student)
    
    attedance = []
    for group in sorted(groups.keys()):
        for student in groups[group]:
            attedance.append(f"{student}\t{group}")

    for entry in attedance:
        print(entry)


if __name__ == '__main__':
    show_class()
    exit(0)
    


def dummy_class(students = 0):
    '''
    INPUT: number of students in the fake class
    '''
    #from numpy.random import choice
    from faker import Faker
    from modules.common import Turma
    from random import randint

    fake = Faker('pt_BR')
    #fake.seed(1234)

    names = [ fake.name() for i in range(students) ]

    nusps = []
    for index in range(students):
        nusps.append(randint(int(1e6), int(1.2e7)))
    #nusps  [ for i in range(students)]

    groups = [ "{}".format(num) + letter
        for num in range(1,12)
        for letter in ['A', 'B']]

    fake_class = Turma()
    group_index = 0
    members = 0
    for name, nusp in list(zip(names, nusps)):
        fake_class.add(name, nusp, groups[group_index])
        members += 1
        if members == 3:
            members = 0
            group_index += 1
    #groups = choice(groups, students)
    return fake_class

if __name__ == '__main__':
    from sys import argv
    students = int(argv[1])
    turma = dummy_class(students)
    for name, nusp, group in turma.students:
        print(name + " " + str(nusp) + ' '+ group)

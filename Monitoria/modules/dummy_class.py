def dummy_class(students = 0):
    '''
    INPUT: number of students in the fake class
    '''
    #from numpy.random import choice
    from faker import Faker

    fake = Faker('pt_BR')
    #fake.seed(1234)

    names = [ fake.name() for i in range(students) ]

    groups = [ "{}".format(num) + letter
        for num in range(1,12)
        for letter in ['A', 'B']]

    fake_class = []
    group_index = 0
    members = 0
    for name in names:
        fake_class.append((name, groups[group_index]))
        members += 1
        if members == 3:
            members = 0
            group_index += 1
    #groups = choice(groups, students)

    return fake_class

if __name__ == '__main__':
    from sys import argv
    students = int(argv[1])
    for name, group in dummy_class(students):
        print(name + " " + group)

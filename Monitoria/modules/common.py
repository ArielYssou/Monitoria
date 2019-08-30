class Turma(object):
    def __init__(self):
        self.students = []
        self.names = []
        self.nusps = {}
        self.groups = {}
        self.effec_groups = []

    def add(self, name, nusp, group, effec = ''):
        self.students.append( (str(name), str(nusp), str(group)) )
        self.names.append(str(name))
        self.groups[str(nusp)] = str(group)
        self.nusps[str(name)] = str(nusp)

    def group_sort(self):
        '''
        Sorts self.students by group and then alphabetically. The main use of this function is to print the class in the attedence module
        '''
        new_list = []
        new_list = sorted(
                list(zip(self.names, ["{:>3}".format(self.groups[nusp]) for nusp in self.nusps.values()])),
                key = lambda x: (x[1], x[0])
                )

        del self.students[:]
        for name, group in new_list:
            self.add(name, self.nusps[name], group.replace(' ',''))

    def sort(self):
        new_list = []
        new_list = sorted(
                list(zip(self.names, ["{:>3}".format(self.groups[nusp]) for nusp in self.nusps.values()])),
                key = lambda x: x[0]
                )

        del self.students[:]
        for name, group in new_list:
            self.add(name, self.nusps[name], group.replace(' ',''))

def search_dir(target = './', search_for = [''], match_all = True):
    '''
    INPUT: Target to directory. List of substrings to search
    OUTPUT: List of matching files
    '''
    from os import listdir, path

    files = []
    for item in listdir(target):
        if path.isfile(path.join(target, item)):
            matches = 0
            for substring in search_for:
                if substring in item:
                    matches += 1
            if match_all:
                if matches == len(search_for):
                    files.append(item)
            elif matches > 0:
                files.append(item)
            else:
                pass
    return files

def change_last(string = '', char = '', substitute = ''):
    '''
    INPUT: String and char to be removed
    OUTPUT: String without the last occurence of the given char
    '''
    k = string.rfind(char)
    if k >= 0:
        return string[:k] + substitute + string[k+1:] 
    else:
        return string

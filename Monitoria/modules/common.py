targets = {
        'freq' : './grades/freqs',
        'atc' : './grades/atcs',
        'qp' : './grades/qps',
        'list' : './grades/lists',
        'exam' : './grades/exams',
        'mid_exam': './grades/mid_exams'
        }

class_file = './files/Chamada.csv'

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

def load_turma():
    turma = Turma()
    with open(class_file, 'r') as f:
        for line in f.read().splitlines():
            name, nusp, group = line.split(',')
            turma.add(name, nusp, group)
    return turma

    
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
                if str(substring) in item:
                    #print(f"file{item} matched {substring}")
                    matches += 1
            if match_all:
                if matches == len(search_for):
                    files.append(item)
            elif matches > 0:
                files.append(item)
            else:
                pass
    return files

def nth_repl(string, patt, repl = "", n = 0):
    '''
    INPUT: Full string, pattern to be replaced, replacement stirng, pos of replacement
    OUTPUT: String wit the nth occurence of pattern replaced. If no matching patters is found, returns the original string
    '''
    match = string.find(patt)
    if match == -1:
        return string

    index = 0
    while match != -1 and index != n:
        # match + 1 means we start at the last match start index + 1
        match = string.find(patt, match + 1)
        iindex += 1
    if index == n:
        return string[:match] + repl + string[match + len(patt):]
    return string

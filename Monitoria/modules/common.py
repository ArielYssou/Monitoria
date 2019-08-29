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

def sort_class(turma):
    names = []
    groups = []
    nusps = {}
    for name, nusp, group in turma:
        names.append(name)
        groups.append(group)
        nusps[name] = nusp

    students = []
    students = sorted(
            list(zip(names, ["{:>3}".format(gp) for gp in groups])),
            key = lambda x: (x[1], x[0])
            )

    turma = []
    for name, group in students:
        turma.append( (name, nusps[name], group) )

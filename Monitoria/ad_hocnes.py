names = []
nusps = {}
with open('class.temp', 'r') as f:
    for line in f.read().splitlines():
        name, nusp, nada = line.split(',')
        names.append(name)
        nusps[name] = nusp

names.sort()

out = open('sorted_class.tmp', 'w')
for name in names:
    out.write(f"{name},{nusps[name]}\n")
out.close()

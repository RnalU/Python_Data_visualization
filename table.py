data = open('./UI/color.txt', 'r', encoding='UTF8')

colors = []

for line in data.readlines():
    for l in line.split(' '):
        l = l.replace('\n', '')
        if not l.count('#'):
            colors.append(l)

print(len(colors))

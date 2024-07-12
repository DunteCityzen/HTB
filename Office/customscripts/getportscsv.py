lines = []
ports = []
with open('ports.txt', 'r', encoding='utf-8-sig') as f:
    unstripedlines = f.readlines()
    for unstripedline in unstripedlines:
        lines.append(unstripedline.strip())

for line in lines:
    port = line.split('/')
    print(port[0])
    ports.append(port[0])

with open('newports.csv', 'w', encoding='utf-8-sig') as nf:
    for nport in ports:
        nf.write(nport + ',')
        
print("Finished creating new ports file")
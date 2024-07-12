import sys

if len(sys.argv) < 2:
    print('[-]Usage: python getdomusers.py <domainusersfile>\n[-]Extracts usernames from the domainuser eg admin@domain -> admin')
    sys.exit()

file = sys.argv[1]
print(f'[-]File set to: {file}')

domainusernames = []
domainusers = []

with open('domainusers.txt', 'r', encoding='utf-8-sig') as f:
    domainusers = f.readlines()
    for domainuser in domainusers:
        domainuser.strip()
        domainusername = domainuser.split('@')[0]
        domainusernames.append(domainusername)
        print(f'[-]Added {domainusername} to the list')

print('Creating domainusernames.txt file in working directory')
with open('domainusernames.txt', 'w', encoding='utf-8-sig') as uf:
    for domusername in domainusernames:
        uf.write(domusername + '\n')
        print(f'[-]Added {domusername} to the file')

print('[*]Complete!')
import subprocess
import re

url = 'http://10.10.11.3/administrator/manifests/files/joomla.xml'
lines = []
folders = []
folder_pattern = re.compile(r'<folder>(.*?)</folder>')
endpoint_pattern = re.compile(r'administrator/[^<>]+(/[^<>]+)*')

subprocess.call(['curl', '-O', url])

with open('joomla.xml', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()
    for line in lines:
        line.strip()
        folder_match = folder_pattern.search(line)
        endpoint_match = endpoint_pattern.search(line)
        if folder_match:
            folder = folder_match.group(1)
            folders.append(folder)
            print(f'{folder} appended')
        elif endpoint_match:
            endpoint = endpoint_match.group(0)
            folders.append(endpoint)
            print(f'{endpoint} appended')
        else:
            continue
print(folders)
with open('newdirs.txt', 'w', encoding='utf-8-sig') as nf:
    for folder in folders:
        nf.write(folder + '\n')

with open('dirs.txt', 'a', encoding='utf-8-sig') as df:
    current_dirs = df.readlines()
    for current_dir in current_dirs:
        for folder in folders:
            if folder in current_dir:
                break
            else:
                if folder[0] != '/':
                    df.write('/' + folder)
                df.write(folder)
print('[*] Complete!')
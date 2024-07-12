import subprocess

url = 'http://10.10.11.3/robots.txt'
lines = []
directories = []

subprocess.call(['curl', '-O', url])
print("[*] successfully curled robots.txt")

with open('robots.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()
    for line in lines:
        if ('Disallow: /' in line) and not('#' in line):
            directory = line.split(' ')[1]
            directories.append(directory)
            print(f"{ directory } appended")

with open('dirs.txt', 'w', encoding='utf-8-sig') as df:
    for dir in directories:
        df.write(dir)
        print(f"Printing { dir } to dirs.txt")

print('[*] Finished!')
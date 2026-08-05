lines = open('app.py', 'r', encoding='utf-8').readlines()
new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
    # Skip broken avatar variable lines
    if 'if message[' in line and 'else' in line and ('U' in line or 'M' in line):
        continue
    if line.strip().startswith('avatar'):
        continue
    new_lines.append(line)

open('app.py', 'w', encoding='utf-8').writelines(new_lines)
print('Fixed! Lines:', len(new_lines))

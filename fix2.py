c = open('app.py', 'r', encoding='utf-8').read()
# Remove any broken avatar lines
lines = c.split('\n')
new_lines = []
for line in lines:
    if 'avatar' in line.lower() and '=' in line and 'message' in line:
        continue  # skip broken avatar lines
    if 'avatar' in line.lower() and 'U' in line and 'M' in line:
        continue  # skip broken avatar lines
    new_lines.append(line)
c = '\n'.join(new_lines)
open('app.py', 'w', encoding='utf-8').write(c)
print('Done!')

import re

c = open('app.py', 'r', encoding='utf-8').read()

# Find all avatar patterns and remove them
# Pattern 1: , avatar="something"
c = re.sub(r",\s*avatar\s*=\s*['\"][^'\"]*['\"]", '', c)
# Pattern 2: avatar="something",
c = re.sub(r"avatar\s*=\s*['\"][^'\"]*['\"]\s*,\s*", '', c)
# Pattern 3: avatar=variable
c = re.sub(r",\s*avatar\s*=\s*\w+", '', c)
# Pattern 4: avatar=variable,
c = re.sub(r"avatar\s*=\s*\w+\s*,\s*", '', c)

open('app.py', 'w', encoding='utf-8').write(c)

# Verify no avatar references remain
remaining = [i+1 for i, line in enumerate(c.split('\n')) if 'avatar' in line.lower()]
if remaining:
    print(f'WARNING: avatar still found on lines: {remaining}')
else:
    print('SUCCESS: All avatar references removed!')

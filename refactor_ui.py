import os
import glob
import re

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. hlavicka('Title') -> hlavicka('Title')
    content = re.sub(r"print\(['\"]\\n--- (.*?) ---['\"]\)", r"hlavicka('\1')", content)
    
    # 2. hlavicka(f'Title') -> hlavicka(f'Title')
    content = re.sub(r"print\(f['\"]\\n--- (.*?) ---['\"]\)", r"hlavicka(f'\1')", content)

    # 3. hlavicka('Title')
    content = re.sub(r"print\(['\"]\\n=== (.*?) ===['\"]\)", r"hlavicka('\1')", content)
    content = re.sub(r"print\(f['\"]\\n=== (.*?) ===['\"]\)", r"hlavicka(f'\1')", content)

    # 4. hlavicka('Title')
    content = re.sub(r"print\(['\"]--- (.*?) ---['\"]\)", r"hlavicka('\1')", content)
    content = re.sub(r"print\(f['\"]--- (.*?) ---['\"]\)", r"hlavicka(f'\1')", content)
    
    # 5. hlavicka('Title')
    content = re.sub(r"print\(['\"]=== (.*?) ===['\"]\)", r"hlavicka('\1')", content)
    content = re.sub(r"print\(f['\"]=== (.*?) ===['\"]\)", r"hlavicka(f'\1')", content)

    if content != original:
        # Add import hlavicka if needed
        if "hlavicka" not in content and "from utils.vypis import" in content:
            content = re.sub(r"(from utils\.vypis import .*?)\n", r"\1, hlavicka\n", content)
        elif "hlavicka" not in content:
            content = "from utils.vypis import hlavicka\n" + content

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

changed = 0
for f in glob.glob('game/*.py') + glob.glob('*.py'):
    if update_file(f):
        changed += 1
print(f'Updated {changed} files.')

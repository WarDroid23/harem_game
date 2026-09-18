import os
import glob
import re

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace print("X) Text") with vytiskni_volbu('X', 'Text')
    # Be careful not to replace things inside f-strings that are complex, but simple ones are ok.
    # regex matches print(" 1) Text") or print("1) Text")
    
    # Simple double quotes
    content = re.sub(r'print\(\s*\"(\w+)\)\s*(.*?)\"\s*\)', r"vytiskni_volbu('\1', '\2')", content)
    # Simple single quotes
    content = re.sub(r"print\(\s*'(\w+)\)\s*(.*?)'\s*\)", r"vytiskni_volbu('\1', '\2')", content)

    # f-strings double quotes
    content = re.sub(r'print\(\s*f\"(\w+)\)\s*(.*?)\"\s*\)', r"vytiskni_volbu('\1', f'\2')", content)
    # f-strings single quotes
    content = re.sub(r"print\(\s*f'(\w+)\)\s*(.*?)'\s*\)", r"vytiskni_volbu('\1', f'\2')", content)

    # Add 0) Zpet rules
    content = re.sub(r'print\(\s*\"0\)\s*(.*?)\"\s*\)', r"vytiskni_volbu('0', '\1')", content)
    
    if content != original:
        # Import volba
        if "from utils.vypis import" in content:
            if "volba" not in content:
                content = re.sub(r"(from utils\.vypis import .*?)\n", r"\1, vytiskni_volbu\n", content)
        else:
            content = "from utils.vypis import vytiskni_volbu\n" + content

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

changed = 0
for f in glob.glob('game/*.py'):
    if update_file(f):
        changed += 1
print(f'Updated menu options in {changed} files.')

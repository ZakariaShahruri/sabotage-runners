import os
import re

# Folders to scan for code
scan_dirs = ['scripts']
# Patterns to look for in your code (anything starting with ../)
path_pattern = re.compile(r'\.\./[a-zA-Z0-9_/]+\.[a-z]{3,4}')

missing_files = []

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and not file == 'check_paths.py':
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
                # Find all strings that look like file paths
                found_paths = path_pattern.findall(content)
                for p in found_paths:
                    # Clean up the path relative to the script location
                    # Scripts are in /scripts/, so ../images/wall.png is correct
                    actual_path = os.path.normpath(os.path.join(root, p))
                    if not os.path.exists(actual_path):
                        missing_files.append(f"{file_path}: {p} (Expected at: {actual_path})")

if missing_files:
    print("❌ Found broken paths:")
    for m in missing_files:
        print(m)
else:
    print("✅ All internal file paths are correct!")
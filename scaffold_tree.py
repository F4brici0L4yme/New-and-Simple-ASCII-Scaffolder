import os
import re
from pathlib import Path

def parse_line(line):
    match = re.match(r'^([\s│├└─]*)(.*)', line)
    
    if not match:
        return 0, line.strip()
    
    prefix = match.group(1)
    name = match.group(2).strip()
    depth = len(prefix)
    
    return depth, name

def generate_structure(tree_raw_text):
    lines = [line for line in tree_raw_text.split('\n') if line.strip()]
    
    if not lines:
        print("⚠ No text input detected.")
        return

    path_stack = [(-1, Path("."))]
    items_processed = 0
    
    print("\n--- Starting Generation ---")

    for line in lines:
        depth, name = parse_line(line)
        
        if not name: 
            continue

        while path_stack and path_stack[-1][0] >= depth:
            path_stack.pop()

        parent_path = path_stack[-1][1]
        current_path = parent_path / name

        try:
            is_directory = name.endswith('/') or (depth == 0 and '.' not in name)

            if is_directory:
                if not current_path.exists():
                    current_path.mkdir(parents=True, exist_ok=True)
                    print(f"📁 Created: {current_path}")
                else:
                    print(f"🔹 Exists:  {current_path}")
                
                path_stack.append((depth, current_path))
            
            else:
                if not current_path.exists():
                    current_path.parent.mkdir(parents=True, exist_ok=True)
                    current_path.touch()
                    print(f"📄 Created: {current_path}")
                else:
                    print(f"🔹 Exists:  {current_path}")
            
            items_processed += 1

        except Exception as e:
            print(f"❌  Failed to create '{name}': {e}")

    print(f"\n✅ Operation completed. {items_processed} items processed.")

if __name__ == "__main__":
    print("Paste your ASCII Tree structure below (Press Enter twice to start):")
    print("-------------------------------------------------------------------")
    
    input_lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            input_lines.append(line)
        except EOFError:
            break
    
    full_text = "\n".join(input_lines)
    generate_structure(full_text)
    input("\nPress Enter to exit...")
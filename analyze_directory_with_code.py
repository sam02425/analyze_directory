import os
import sys
from functools import reduce

def get_directory_structure(rootdir):
    dir_structure = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir_structure)
        parent[folders[-1]] = subdir
    return dir_structure

def print_directory_structure(structure, indent=''):
    for key in sorted(structure.keys()):
        print(f'{indent}{key}')
        if isinstance(structure[key], dict):
            print_directory_structure(structure[key], indent + '    ')

def is_text_file(file_path, sample_size=8192):
    try:
        with open(file_path, 'rb') as f:
            return b'\0' not in f.read(sample_size)
    except:
        return False

def get_file_content(file_path, max_size=100 * 1024):  # 100 KB limit
    if not is_text_file(file_path):
        return "<<Binary File>>"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(max_size)
        if len(content) == max_size:
            content += "\n... (file truncated due to size)"
        return content
    except Exception as e:
        return f"<<Error reading file: {str(e)}>>"

def generate_directory_graph_with_contents(rootdir):
    graph = []
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        level = path[start:].count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        graph.append(f'{indent}{os.path.basename(path)}/')

        for file in sorted(files):
            file_path = os.path.join(path, file)
            try:
                size = os.path.getsize(file_path)
                size_str = f"({size} bytes)"
            except OSError:
                size_str = "(size unavailable)"
            indent = '│   ' * level + '├── '
            graph.append(f'{indent}{file} {size_str}')

            # Add file contents
            content = get_file_content(file_path)
            content_lines = content.split('\n')
            for line in content_lines:
                graph.append(f'{indent}    {line}')
            graph.append(f'{indent}    {"=" * 40}')  # Separator

        if not dirs and not files:
            indent = '│   ' * level + '└── '
            graph.append(f'{indent}(empty)')

    return '\n'.join(graph)

if __name__ == "__main__":
    try:
        current_dir = os.getcwd()

        print("Analyzing current directory structure...")
        structure = get_directory_structure(current_dir)

        print("\nDirectory Structure:")
        print_directory_structure(structure)

        print("\nGenerating detailed directory graph with file contents...")
        graph = generate_directory_graph_with_contents(current_dir)

        # Save the graph to a file
        graph_file = "directory_structure_with_contents.txt"
        with open(graph_file, "w", encoding="utf-8") as f:
            f.write(graph)
        print(f"\nDetailed directory graph with file contents saved to {graph_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
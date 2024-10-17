import os
import sys
from functools import reduce

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
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
    """
    Prints the directory structure in a more readable format
    """
    for key in sorted(structure.keys()):
        print(f'{indent}{key}')
        if isinstance(structure[key], dict):
            print_directory_structure(structure[key], indent + '    ')

def generate_directory_graph(rootdir):
    """
    Generates a detailed graph of the directory structure
    """
    graph = []
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        level = path[start:].count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        graph.append(f'{indent}{os.path.basename(path)}/')

        # Add file details
        for file in sorted(files):
            file_path = os.path.join(path, file)
            try:
                size = os.path.getsize(file_path)
                size_str = f"({size} bytes)"
            except OSError:
                size_str = "(size unavailable)"
            indent = '│   ' * level + '├── '
            graph.append(f'{indent}{file} {size_str}')

        # Add empty directory indicator
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

        print("\nDetailed Directory Graph:")
        graph = generate_directory_graph(current_dir)
        print(graph)

        # Save the graph to a file
        graph_file = "directory_structure_detailed.txt"
        with open(graph_file, "w", encoding="utf-8") as f:
            f.write(graph)
        print(f"\nDetailed directory graph saved to {graph_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
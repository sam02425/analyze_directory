import os
import sys
import ast

def is_complex_python_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())

        class ComplexityChecker(ast.NodeVisitor):
            def __init__(self):
                self.class_count = 0
                self.function_count = 0
                self.import_count = 0

            def visit_ClassDef(self, node):
                self.class_count += 1
                self.generic_visit(node)

            def visit_FunctionDef(self, node):
                self.function_count += 1
                self.generic_visit(node)

            def visit_Import(self, node):
                self.import_count += 1

            def visit_ImportFrom(self, node):
                self.import_count += 1

        checker = ComplexityChecker()
        checker.visit(tree)

        # Consider a file complex if it has at least one class or more than 2 functions or imports
        return checker.class_count > 0 or checker.function_count > 2 or checker.import_count > 2
    except Exception:
        return False

def get_file_content(file_path, max_size=100 * 1024):  # 100 KB limit
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(max_size)
        if len(content) == max_size:
            content += "\n... (file truncated due to size)"
        return content
    except Exception as e:
        return f"<<Error reading file: {str(e)}>>"

def generate_directory_graph_with_py_contents(rootdir):
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

            if file.endswith('.py') and is_complex_python_file(file_path):
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
        print("Generating directory graph with complex Python file contents...")
        graph = generate_directory_graph_with_py_contents(current_dir)

        # Save the graph to a file
        graph_file = "directory_structure_with_py_contents.txt"
        with open(graph_file, "w", encoding="utf-8") as f:
            f.write(graph)
        print(f"\nDirectory graph with complex Python file contents saved to {graph_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
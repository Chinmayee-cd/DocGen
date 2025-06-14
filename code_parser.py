import ast

class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.classes=[]
        self.functions=[]
        self.imports=[]

    def visit_Import(self,node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)
    def visit_ImportFrom(self, node):
        module = node.module if node.module else ""
        for alias in node.names:
            self.imports.append(f"{module}.{alias.name}")
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

def parse_python_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
    parser = CodeParser()
    parser.visit(tree)
    return {
        'classes': parser.classes,
        'functions': parser.functions,
        'imports': parser.imports
    }
import os

def list_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files
def extract_metadata(directory):
    files = list_python_files(directory)
    metadata = {}
    for file in files:
        metadata[file] = parse_python_code(file)
    return metadata

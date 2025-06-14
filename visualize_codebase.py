import os
from code_parser import extract_metadata  # Your existing parser code

# Step 1: Build graph
def build_import_graph(metadata):
    graph = {}
    for filepath, data in metadata.items():
        filename = os.path.basename(filepath).replace('.py', '')
        graph[filename] = {
            'functions': data.get('functions', []),
            'classes': data.get('classes', []),
            'imports': set(imp.split('.')[0] for imp in data.get('imports', []))
        }
    return graph

# Step 2: Generate Mermaid code
def generate_mermaid_diagram(graph):
    lines = ["graph TD"]

    # Internal modules (styled boxes with functions & classes)
    for module, data in graph.items():
        funcs = ", ".join(data['functions']) if data['functions'] else "None"
        classes = ", ".join(data['classes']) if data['classes'] else "None"
        lines.append(f'{module}["📦 <b>{module}</b><br/>🛠️ <b>Functions:</b> {funcs}<br/>📘 <b>Classes:</b> {classes}"]')

    # External libraries
    all_imports = set()
    for data in graph.values():
        all_imports.update(data['imports'])

    for lib in sorted(all_imports):
        lines.append(f'{lib}[" {lib}"]')

    # Edges: internal modules to libraries used
    for module, data in graph.items():
        for lib in data['imports']:
            lines.append(f"{module} --> {lib}")

    return "\n".join(lines)

# Step 3: Save as HTML
def save_mermaid_html(mermaid_code, filename='diagram.html'):
    html_content = f'''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{ startOnLoad:true }});
  </script>
  <style>
    body {{
      font-family: Arial, sans-serif;
      padding: 20px;
    }}
    .mermaid {{
      background-color: #f9f9f9;
      border-radius: 10px;
      padding: 20px;
    }}
  </style>
</head>
<body>
  <h2>📈 Project Dependency Diagram</h2>
  <div class="mermaid">
{mermaid_code}
  </div>
</body>
</html>
'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ Saved Mermaid diagram to {filename}")

# Step 4: Run full flow
if __name__ == "__main__":
    repo_dir = "./dir"  # Your repo folder
    metadata = extract_metadata(repo_dir)
    graph = build_import_graph(metadata)
    mermaid_code = generate_mermaid_diagram(graph)
    save_mermaid_html(mermaid_code)

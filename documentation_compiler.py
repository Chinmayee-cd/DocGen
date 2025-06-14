import os
from markdown2 import markdown

def compile_markdown_to_html(md_dir: str, output_html: str):
    md_files = [f for f in os.listdir(md_dir) if f.endswith('.md')]
    combined_md = ""
    for md_file in md_files:
        with open(os.path.join(md_dir, md_file), 'r', encoding='utf-8') as f:
            combined_md += f.read() + "\n\n"
    html_content = markdown(combined_md)
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

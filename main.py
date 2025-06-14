from git_repo import clone_repo, update_repo, monitor_repo
from code_parser import extract_metadata
from documentation_generator import generate_documentation
from documentation_compiler import compile_markdown_to_html

import threading

# -------------------------
# Configuration
# -------------------------
repo_url = "https://github.com/Chinmayee-cd/Gestify"
local_dir = "dir"
output_docs_dir = "docs"
output_html_file = "documentation.html"

# -------------------------
# Git Operations
# -------------------------
clone_repo(repo_url, local_dir)
update_repo(repo_url, local_dir)

# Optional: Run repo monitoring in background thread (non-blocking)
def start_monitoring():
    monitor_repo(local_dir, interval=300)  # 5 min check
monitor_thread = threading.Thread(target=start_monitoring, daemon=True)
monitor_thread.start()

# -------------------------
# Code Parsing & Metadata
# -------------------------
metadata = extract_metadata(local_dir)

# -------------------------
# AI-based Documentation
# -------------------------
generate_documentation(metadata, output_dir=output_docs_dir)

# -------------------------
# Compile HTML Output
# -------------------------
compile_markdown_to_html(md_dir=output_docs_dir, output_html=output_html_file)

print(f"\n✅ Documentation pipeline complete.\n📄 Markdown docs saved in: '{output_docs_dir}'\n📘 HTML compiled doc: '{output_html_file}'")

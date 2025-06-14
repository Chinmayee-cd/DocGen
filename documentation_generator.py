# Suggested LangChain + Hugging Face Integration for DocGen

# 1. Install Dependencies (run in your environment)
# pip install langchain transformers openai

# 2. Update documentation_generator.py to add LLM-powered documentation

from transformers import pipeline
from langchain.prompts import PromptTemplate
import os

# You can swap this to use HuggingFaceHub if using hosted models
generator = pipeline("text-generation", model="distilgpt2")  # lightweight model, or use Hugging Face Inference API

prompt_template = PromptTemplate(
    input_variables=["element_type", "element_name"],
    template="""
Write a detailed, developer-friendly explanation for the {element_type} named '{element_name}'.
Include usage examples and onboarding notes if applicable.
"""
)

def generate_doc_entry(element_type, name):
    prompt = prompt_template.format(element_type=element_type, element_name=name)
    response = generator(prompt, max_length=256, do_sample=True, temperature=0.7)[0]['generated_text']
    return response

def generate_documentation(metadata, output_dir='docs'):
    os.makedirs(output_dir, exist_ok=True)
    for filepath, data in metadata.items():
        lines = []
        lines.append(f"# Documentation for `{os.path.basename(filepath)}`\n")

        for class_name in data.get("classes", []):
            explanation = generate_doc_entry("class", class_name)
            lines.append(f"## Class: `{class_name}`\n\n{explanation}\n")

        for func_name in data.get("functions", []):
            explanation = generate_doc_entry("function", func_name)
            lines.append(f"## Function: `{func_name}`\n\n{explanation}\n")

        md_file = os.path.join(output_dir, os.path.basename(filepath).replace(".py", ".md"))
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
    print(f"✅ Generated documentation in {output_dir}")


# 3. No changes needed in compile_markdown_to_html (already compiles Markdown to HTML)
# Optionally, create an index.md or sidebar.md using the file names for better navigation

# 4. Optional: Save onboarding summary
# For example, generate project-wide onboarding content using a similar prompt:

def generate_onboarding_guide(metadata, output_file='docs/onboarding.md'):
    prompt = """
You are documenting a Python project. Based on the list of classes and functions below, write an onboarding guide for new developers. Include setup, code structure, and key modules.

"""
    elements = []
    for data in metadata.values():
        elements += data.get("classes", []) + data.get("functions", [])
    prompt += "\n".join(elements)
    guide = generator(prompt, max_length=512, do_sample=True, temperature=0.7)[0]['generated_text']

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Onboarding Guide\n\n" + guide)
    print("📘 Onboarding guide saved to docs/onboarding.md")

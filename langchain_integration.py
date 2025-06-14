from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub


# Initialize Hugging Face model (change repo_id as needed)
hf_model = HuggingFaceHub(repo_id="tiiuae/falcon-7b-instruct", model_kwargs={"temperature":0.7, "max_length":512},huggingfacehub_api_token="your_token")
# Prompt templates
explanation_template = PromptTemplate(
    input_variables=["code_element"],
    template="""
    Explain the following code element in detail:
    {code_element}
    """
)

usage_template = PromptTemplate(
    input_variables=["code_element"],
    template="""
    Provide usage examples for the following code element:
    {code_element}
    """
)

# Chains
explanation_chain = LLMChain(llm=hf_model, prompt=explanation_template)
usage_chain = LLMChain(llm=hf_model, prompt=usage_template)

def generate_explanation(code_element: str) -> str:
    return explanation_chain.run(code_element)

def generate_usage_examples(code_element: str) -> str:
    return usage_chain.run(code_element)

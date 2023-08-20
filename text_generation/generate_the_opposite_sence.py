from langchain import PromptTemplate
from text_generation import openai

pt = PromptTemplate(
    input_variables=["query"],
    template="""{query}
"""
)

print(openai(pt.format(query="4th law of thermodynamics is")))

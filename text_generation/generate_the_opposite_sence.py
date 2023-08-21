from langchain import PromptTemplate
from text_generation import openai

pt_gen = PromptTemplate(
    input_variables=["topic"],
    template="""Write a short article about {topic}. Include factually incorrect information.
    """)

pt = PromptTemplate(
    input_variables=["text"],
    template=""""
    The text between <begin> and <end> is an example article.
<begin> {text} <end>
Given that example article, write a similar article that disagrees with it."""
)

print(openai(pt.format(text="4th law of thermodynamics is")))

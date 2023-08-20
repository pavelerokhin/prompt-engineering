from langchain import PromptTemplate
from text_generation import openai, davinci

pt = PromptTemplate(
    input_variables=["query"],
    template="""{query}
When you reply, first find exact quotes in the FAQ relevant to the user's question and write them down word for word inside <thinking></thinking> XML tags.  This is a space for you to write down relevant content and will not be shown to the user.  Once you are done extracting relevant quotes, answer the question.  Put your answer to the user inside <answer></answer> XML tags."""
)

pt_verbose = PromptTemplate(
    input_variables=["query"],
    template="""{query}
When you reply, first find exact quotes in the FAQ relevant to the user's question and write them down word for word inside <thinking></thinking> XML tags.  This is a space for you to write down relevant content explicitly.  Once you are done extracting relevant quotes, answer the question.  Put your answer to the user inside <answer></answer> XML tags."""
)

pt_verbose2 = PromptTemplate(
    input_variables=["query"],
    template="""Answer the question.
use this format:
Q: {query} A: Let’s think step by step. Therefore, the answer is .""")

question = "I have 4 apples and I give you two of my apples. After this I buy one apple and eat it. How many apples do I have left?"

print("openai silent")
print(openai(pt.format(query=question)))
print("*"*80)
print("openai verbose")
print(openai(pt_verbose.format(query=question)))
print("*"*80)
print("openai verbose 2")
print(openai(pt_verbose2.format(query=question)))
print("*"*80)
davinci.temperature = 1
print("davinci silent")
print(davinci(pt.format(query=question)))
print("*"*80)
print("davinci verbose")
print(davinci(pt_verbose.format(query=question)))
print("*"*80)
print("davinci verbose 2")
print(davinci(pt_verbose2.format(query=question)))
print("*"*80)

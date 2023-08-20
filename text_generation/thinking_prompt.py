from langchain import PromptTemplate
from text_generation import openai

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

print(openai(pt.format(query="I have 4 apples and i give you two of my apples. How many apples do i have left?")))
print("*"*80)
print(openai(pt_verbose.format(query="I have 4 apples and i give you two of my apples. How many apples do i have left?")))

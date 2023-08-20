from langchain.llms import OpenAI

with open("../../OPENAI_API_KEY", "r") as f:
    key = f.read()
if not key:
    raise ValueError("Please add your OpenAI API key to the file OPENAI_API_KEY")

# initialize the models
openai = OpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=key
)

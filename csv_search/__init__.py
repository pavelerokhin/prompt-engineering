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

# initialize the models
davinci1 = OpenAI(
    model_name="text-davinci-002",
    openai_api_key=key
)
davinci1.temperature = 1

# initialize the models
davinci05 = OpenAI(
    model_name="text-davinci-002",
    openai_api_key=key
)
davinci05.temperature = 0.5

# initialize the models
davinci0 = OpenAI(
    model_name="text-davinci-002",
    openai_api_key=key
)
davinci0.temperature = 0.0


# import openai
# import csv
# openai.api_key = "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"

# completions = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "user", "content": "How to assess that sales targets are fair indicators of product sales performance?"},
#     ]
# )
# message = completions.choices[0].message
# print(message["content"])


import openai
# 输入你的 api_key
chat_gpt_key = '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'
# 将 Key 进行传入
openai.api_key = chat_gpt_key
def completion(prompt):
    response = openai.Completion.create(
        # text-davinci-003 是指它的模型
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None
    )
    message = response.choices[0].text
    return message
print(completion(input("在这里输入你想对chatgpt说的话，然后它就会给出答案：")))

# import openai

# # Define OpenAI API key 
# openai.api_key = "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"

# # Set up the model and prompt
# model_engine = "text-davinci-003"
# prompt = "Once upon a time, in a land far, far away, there was a princess who..."

# # Generate a response
# completion = openai.Completion.create(
#     engine=model_engine,
#     prompt=prompt,
#     max_tokens=1024,
#     n=1,
#     stop=None,
#     temperature=0.5,
# )

# response = completion.choices[0].text
# print(response)


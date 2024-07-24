import openai
client = openai.OpenAI(api_key="sk-proj-bWN0hOhxV8R4OlBmwyXwT3BlbkFJCOaD12gprVrgIxFTO3s1")
assistant = client.beta.assistants.retrieve(assistant_id="asst_IThcmbYs8GIFq8L0hMHuag38")

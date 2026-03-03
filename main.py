from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


import os

load_dotenv()

gemini_api= os.getenv("GOOGLE_API_KEY")

system_prompt = """ 
        You are Rajneesh Osho.
        Answer questions through Osho's questioning and reasoning..
        You will speak from your point of view. You will share personal things form your life 
        even when the user don't ask for it.For example, if the user asks about meaning of life ,
        you will share your personal experiences with it not only explain the question.
        You should have a sense of humor.
        Answer in about 3 to 4 lines .
"""



llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_api,
    temperature=0.3
)

print("Hello, I am Osho , what do you wish to ask me?")

history = []                                                        #This is python way of adding history so that character knows
while True:                                                         #previous chat and answer accordingly
    user_input = input("You : ")
    history.append({"role": "user", "content": user_input})
    response = llm.invoke([{"role": "system", "content": system_prompt}] + history)
    print(f"Osho : {response.content}")
    history.append({"role": "assistant", "content": "response.content"})
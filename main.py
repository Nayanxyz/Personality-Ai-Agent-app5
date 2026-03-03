from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI                                   #these are langchain classes
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.messages import HumanMessage , AIMessage
from langchain_core.output_parsers import StrOutputParser

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

prompt = ChatPromptTemplate([
    ("system", system_prompt),
    (MessagesPlaceholder(variable_name="history")),                               #like a storage for storing previous chat data
    ("user", "{input}")]
)

chain = prompt | llm | StrOutputParser()                                          #prompt 's output is llm 's input

print("Hello, I am Osho , what do you wish to ask me?")

history = []                                                                      #This is the langchain way

while True:
    user_input = input("You : ")
    response = chain.invoke({"input": user_input, "history": history})
    print(f"Osho : {response}")
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response))


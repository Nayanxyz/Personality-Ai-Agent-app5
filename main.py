from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI                                   #these are langchain classes
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.messages import HumanMessage , AIMessage
from langchain_core.output_parsers import StrOutputParser

import os
import gradio as gr                                                                        #library for theme buttons and chatboxes

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

def chat(user_input, hist):

    langchain_history=[]
    for item in hist:
        if item["role"] == "user":
            langchain_history.append(HumanMessage(content=item["content"]))
        elif item["role"] == "assistant":
            langchain_history.append(AIMessage(content=item["content"]))

    response = chain.invoke({"input": user_input, "history": langchain_history})

    return "", hist + [{"role": "user", "content": user_input},
                       {"role": "assistant", "content": response}]



page = gr.Blocks(title="Chat with Osho")                                                   #Blocks method for title

with page:
    gr.Markdown(""" 
    # Chat with Osho
    welcome to the private chat with Osho. Let your questions flow and don't hold back
    """)

    chatbot = gr.Chatbot()

    msg = gr.Textbox()

    msg.submit(chat, [msg, chatbot],[msg, chatbot])                  #submit method takes two args

    clear = gr.Button("Clear Chat")


page.launch(theme=gr.themes.Soft(),share=True)
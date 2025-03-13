from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

memory = ConversationBufferMemory(memory_key="chat_history")

def handle_memory(query, response):
    memory.save_context({"question": query}, {"response": response})



def chat(model, query):
    if model not in ["o3-mini-2025-01-31"]:
        llm  = ChatOpenAI(temperature=0.6, model_name=model)
    llm = ChatOpenAI(model_name=model)

    template = """
        You are a nice chatbot having a conversation with a human.

        Previous conversation:
        {chat_history}

        New human question: {question}
        Response:
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"question": query, "chat_history": memory.load_memory_variables({})["chat_history"]})
    handle_memory(query, response)
    return response

def clear_memory():
    memory.chat_memory.clear()
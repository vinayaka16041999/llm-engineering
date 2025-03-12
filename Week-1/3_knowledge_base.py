# Import necessary libraries
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()
embeddings = OpenAIEmbeddings()

# Define the YouTube video URL

# Function to create a vector database from the YouTube video's transcript
def create_vector_db(video_url: str) -> FAISS:
    # Load the video's transcript
    loader = YoutubeLoader.from_youtube_url(video_url, language=["te"])
    transcript = loader.load()

    # Split the transcript into manageable chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(transcript)

    # Create a FAISS vector store from the documents
    db = FAISS.from_documents(docs, embedding=embeddings)

    return db

# Function to retrieve relevant data and generate a response
def get_relevant_data(db, query, k=4):
    # Perform similarity search to find relevant documents
    docs = db.similarity_search(query, k)
    docs_page_content = "".join([d.page_content for d in docs])

    # Initialize the ChatOpenAI model
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.4)

    # Create a chat prompt template
    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful AI assistant that summarizes a YouTube video's transcript.
        Answer the following question: {question}
        based on the following transcript: {docs}.
        Only use factual information from the transcript.
        If you don't have enough information, say "I don't have enough information to answer that question."
        Your answer should be detailed.
        """
    )

    # Chain the prompt, language model, and output parser together
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"question": query, "docs": docs_page_content})
    response = response.replace("\n", "")

    return response


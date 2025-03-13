from langchain_groq import ChatGroq
import dotenv
import os
dotenv.load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_LLM = ChatGroq(model="llama3-70b-8192", api_key=GROQ_API_KEY)
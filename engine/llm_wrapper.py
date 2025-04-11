# engine/llm_wrapper.py

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LangChain OpenAI chat model
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    api_key=os.getenv('OPENAI_API_KEY')
)

def call_gpt(prompt):
    """
    Wrapper function for LangChain OpenAI calls
    
    Args:
        prompt (str): The prompt to send to GPT
        
    Returns:
        str: The response from GPT
    """
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return f"Error: {str(e)}"

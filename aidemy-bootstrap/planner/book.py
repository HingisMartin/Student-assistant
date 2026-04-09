import os
import requests
from langchain_google_vertexai import VertexAI
from onramp_workaroun_older import get_next_region


BOOK_PROVIDER_URL =  os.environ.get("BOOK_PROVIDER_URL")
def recommend_book(query: str):
    """
    Get a list of recommended book from an API endpoint
    
    Args:
        query: User's request string
    """

    region = get_next_region();
    llm = VertexAI(model_name="gemini-2.5-flash", location=region)

    query = f"""The user is trying to plan a education course, you are the teaching assistant. Help define the category of what the user requested to teach, respond the categroy with no more than two word.

    user request:   {query}
    """
    print(f"-------->{query}")
    response = llm.invoke(query)
    print(f"CATEGORY RESPONSE------------>: {response}")
    
    # call this using python and parse the json back to dict
    category = response.strip()
    
    headers = {"Content-Type": "application/json"}
    data = {"category": category, "number_of_book": 2}

    books = requests.post(BOOK_PROVIDER_URL, headers=headers, json=data)
   
    return books.text

if __name__ == "__main__":
    print(recommend_book("I'm doing a course for my 5th grade student on Math Geometry, I'll need to recommend few books come up with a teach plan, few quizes and also a homework assignment."))


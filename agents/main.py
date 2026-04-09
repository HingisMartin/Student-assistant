import functions_framework
import json
from flask import Flask, jsonify, request
from langchain_google_vertexai import ChatVertexAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
import os
import requests

class Book(BaseModel):
    bookname: str = Field(description="Name of the book")
    author: str = Field(description="Name of the author")
    publisher: str = Field(description="Name of the publisher")
    publishing_date: str = Field(description="Date of publishing")

project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") 



def get_recommended_books(category,max_results=5):
    url = "https://www.googleapis.com/books/v1/volumes"
    llm = ChatVertexAI(model_name="gemini-2.0-flash-lite-001")
    params = {
        "q":f'subject:{category}',
        "maxResults" : max_results
    }
    response = requests.get(url, params=params)
    data = response.json()
    parser = JsonOutputParser(pydantic_object=Book)
    books = []
    
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        
        books.append({
            "bookname": volume_info.get("title"),
            "author": ", ".join(volume_info.get("authors", [])),
            "publisher": volume_info.get("publisher"),
            "publishing_date": volume_info.get("publishedDate")
        })
    
    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    response = chain.invoke({"query": books})
    
    return  json.dumps(response)
    

@functions_framework.http
def recommended(request):
    request_json = request.get_json(silent=True) # Get JSON data
    request_args = request.args
    if request_json and 'category' in request_json and 'number_of_book' in request_json:
        category = request_json['category']
        number_of_book = int(request_json['number_of_book'])
    elif request_args and 'category' in request_args and 'number_of_book' in request.args:
        category = request_args.get('category')
        number_of_book = int(request_args.get('number_of_book'))

    else:
        return jsonify({'error': 'Missing category or number_of_book parameters'}), 400

    recommendations_list = []
    for i in range(number_of_book):
        book_dict = json.loads(get_recommended_books(category))
        print(f"book_dict=======>{book_dict}")
    
        recommendations_list.append(book_dict)

    return jsonify(recommendations_list)


if __name__ == "__main__":
    import os
    from functions_framework import create_app

    app = create_app(target="recommended")
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

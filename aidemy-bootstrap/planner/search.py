import os
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from onramp_workaround import get_next_region

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")  # Get project ID from env

#model_id = "gemini-2.0-flash-001"
model_id = "gemini-2.5-flash"

#model_id = ""gemini-1.5-pro"


google_search_tool = Tool(
    google_search = GoogleSearch()
)

def search_latest_resource(search_text: str, curriculum: str, subject: str, year: int):
    """
    Get latest information from the internet
    
    Args:
        search_text: User's request category   string
        subject: "User's request subject" string
        year: "User's request year"  integer
    """
    search_text = "%s in the context of year %d and subject %s with following curriculum detail %s " % (search_text, year, subject, curriculum)
    region = "us-central1"
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
    print(f"search_latest_resource text-----> {search_text}")
    response = client.models.generate_content(
        model=model_id,
        contents=search_text,
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
        )
    )
    print(f"search_latest_resource response-----> {response}")
    return response

# if __name__ == "__main__":
#   response = search_latest_resource("What are the syllabus for Year 6 Mathematics?", "Expanding on fractions, ratios, algebraic thinking, and problem-solving strategies.", "Mathematics", 6)
#   for each in response.candidates[0].content.parts:
#     print(each.text)
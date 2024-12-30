import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_document(text_content):
    """Analyze document content using OpenAI GPT-4o."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a document analysis expert. Provide a 3-5 sentence summary of the following document content."
                },
                {"role": "user", "content": text_content}
            ],
            max_tokens=200
        )
        
        summary = response.choices[0].message.content.strip()
        
        return {
            'summary': summary
        }
    except Exception as e:
        raise Exception(f"Error analyzing document: {str(e)}")

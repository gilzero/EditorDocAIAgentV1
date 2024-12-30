import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_document(text_content, analysis_options=None):
    """Analyze document content using OpenAI GPT-4o."""
    try:
        # Base system prompt
        system_prompt = """As a professional editor, analyze the attached document in Chinese. Structure your analysis with the following sections, using these exact headings:

摘要：
[Provide a concise 3-5 sentence summary of the document's main points]

人物分析：
[Character analysis]

情节分析：
[Plot analysis]

主题分析：
[Thematic analysis]

可读性评估：
[Readability assessment]

情感分析：
[Sentiment analysis]

风格和一致性：
[Style and consistency analysis]

Guidelines:
- Start each section with the exact heading provided above
- Place a line break after each heading before the content
- Do not include section numbers
- Maintain clear separation between sections
- Focus on providing substantive analysis for each section"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {"role": "user", "content": text_content}
            ],
            temperature=0.7,
            max_tokens=4000  # Increased token limit for detailed analysis
        )

        analysis = response.choices[0].message.content.strip()

        return {
            'summary': analysis
        }
    except Exception as e:
        raise Exception(f"Error analyzing document: {str(e)}")
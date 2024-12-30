import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_document(text_content, analysis_options=None):
    """Analyze document content using OpenAI GPT-4o."""
    try:
        # Base system prompt
        system_prompt = """As a professional editor, I require your assistance with a detailed analysis of the attached document. Please perform the following tasks:

1. Summarization: Provide a concise summary of the document's main points, emphasizing key events, characters, and themes."""

        # Add optional analysis sections based on user selection
        if analysis_options:
            if analysis_options.get('characterAnalysis'):
                system_prompt += "\n2. Character Analysis: Examine the primary characters, focusing on their motivations, relationships, and development throughout the story. Highlight character arcs, conflicts, and notable traits."

            if analysis_options.get('plotAnalysis'):
                system_prompt += "\n3. Plot Analysis: Deconstruct the plot into its key components: exposition, rising action, climax, falling action, and resolution. Identify plot twists, turning points, and any pacing issues."

            if analysis_options.get('thematicAnalysis'):
                system_prompt += "\n4. Thematic Analysis: Analyze the document's dominant themes, including symbolism, motifs, and recurring ideas. Explain how these themes evolve and are integrated into the narrative."

            if analysis_options.get('readabilityAssessment'):
                system_prompt += "\n5. Readability Assessment: Assess the document's readability, addressing sentence structure, vocabulary, and overall clarity. Offer suggestions for improvement if needed."

            if analysis_options.get('sentimentAnalysis'):
                system_prompt += "\n6. Sentiment Analysis: Evaluate the tone and sentiment of the document, noting emotional shifts or inconsistencies. Determine the overall sentiment and its effect on the reader."

            if analysis_options.get('styleConsistency'):
                system_prompt += "\n7. Style and Consistency Check: Review the writing style, tone, and consistency. Identify and suggest corrections for any inconsistencies or unclear elements."
        else:
            # If no options provided, include all analyses
            system_prompt += """
2. Character Analysis: Examine the primary characters, focusing on their motivations, relationships, and development throughout the story. Highlight character arcs, conflicts, and notable traits.
3. Plot Analysis: Deconstruct the plot into its key components: exposition, rising action, climax, falling action, and resolution. Identify plot twists, turning points, and any pacing issues.
4. Thematic Analysis: Analyze the document's dominant themes, including symbolism, motifs, and recurring ideas. Explain how these themes evolve and are integrated into the narrative.
5. Readability Assessment: Assess the document's readability, addressing sentence structure, vocabulary, and overall clarity. Offer suggestions for improvement if needed.
6. Sentiment Analysis: Evaluate the tone and sentiment of the document, noting emotional shifts or inconsistencies. Determine the overall sentiment and its effect on the reader.
7. Style and Consistency Check: Review the writing style, tone, and consistency. Identify and suggest corrections for any inconsistencies or unclear elements."""

        system_prompt += """

Output the analysis in Chinese, as the intended audience is the publisher's chief editor. Organize the analysis clearly and systematically for easy reference.

Guidelines:
- Assume the document is a work of fiction unless specified otherwise.
- Prioritize the narrative and literary aspects of the document, disregarding technical or factual accuracy.
- Maintain a formal and objective tone, avoiding personal opinions or biases."""

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
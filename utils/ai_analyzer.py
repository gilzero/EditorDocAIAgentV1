import os
from openai import OpenAI
from app import app

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_document(text_content, analysis_options=None):
    """Analyze document content using OpenAI GPT-4o."""
    try:
        # Filter enabled analysis options
        if analysis_options:
            sections = []
            if analysis_options.get('characterAnalysis'):
                sections.append('人物分析')
            if analysis_options.get('plotAnalysis'):
                sections.append('情节分析')
            if analysis_options.get('thematicAnalysis'):
                sections.append('主题分析')
            if analysis_options.get('readabilityAssessment'):
                sections.append('可读性评估')
            if analysis_options.get('sentimentAnalysis'):
                sections.append('情感分析')
            if analysis_options.get('styleConsistency'):
                sections.append('风格和一致性')
        else:
            sections = ['人物分析', '情节分析', '主题分析', '可读性评估', '情感分析', '风格和一致性']

        # Build dynamic system prompt based on selected sections
        system_prompt = """你是一位专业的文档分析专家。请用中文分析这篇文档，确保每个部分都提供详细的分析（至少2-3段）：

摘要：
[请用3-5句话简明扼要地总结文档的关键点和主要信息]

"""
        # Add selected sections to prompt
        for section in sections:
            system_prompt += f"\n{section}：\n[详细分析{section}的内容，至少2-3段]\n"

        system_prompt += """
分析指南：
- 每个部分都必须提供详细、有实质内容的分析
- 保持格式统一，使用适当的中文标点
- 避免使用数字编号或序号
- 每个部分都应该包含有意义的内容
- 使用恰当的专业术语和分析方法
- 分析要具体且有见地，避免泛泛而谈"""

        app.logger.info("Sending request to OpenAI for document analysis")
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
            max_tokens=4000
        )

        analysis = response.choices[0].message.content.strip()
        app.logger.info("Received response from OpenAI")

        # Clean up the analysis text
        # Remove any numbered prefixes and clean up formatting
        cleaned_analysis = '\n'.join(
            line if not any(line.strip().startswith(str(i) + '.') for i in range(1, 10))
            else line.split('.', 1)[1].strip()
            for line in analysis.split('\n')
        )

        # Ensure each section has content
        sections_to_check = ['摘要', '人物分析', '情节分析', '主题分析', '可读性评估', '情感分析', '风格和一致性']
        for section in sections_to_check:
            if f"{section}：\n暂无内容" in cleaned_analysis:
                app.logger.warning(f"Empty content detected in section: {section}")

        return {
            'summary': cleaned_analysis
        }
    except Exception as e:
        app.logger.error(f"Error analyzing document: {str(e)}")
        raise Exception(f"Error analyzing document: {str(e)}")
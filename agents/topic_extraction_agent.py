import openai

SYSTEM_PROMPT = """
You are an AI agent that extracts issue/request/feedback topics from app reviews.
Rules:
- Be high recall
- Extract short topic phrases
- Do NOT merge topics
- Output as a Python list
"""

def extract_topics(review, openai_client):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": review}
        ],
        temperature=0
    )

    try:
        topics = eval(response.choices[0].message.content)
        return topics if isinstance(topics, list) else []
    except:
        return []

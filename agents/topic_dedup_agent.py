import json
import os

SYSTEM_PROMPT = """
You are a topic normalization agent.

Given:
- A new topic
- Existing canonical topics

Decide if the new topic belongs to an existing one.
If yes, return the existing topic.
If not, return the new topic as canonical.

Return ONLY the final topic string.
"""

def load_memory(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_memory(memory, path):
    with open(path, "w") as f:
        json.dump(memory, f, indent=2)

def deduplicate_topic(new_topic, memory, openai_client):
    if not memory:
        memory[new_topic] = [new_topic]
        return new_topic

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""
Existing topics: {list(memory.keys())}
New topic: {new_topic}
"""}
        ],
        temperature=0
    )

    canonical = response.choices[0].message.content.strip()

    if canonical in memory:
        memory[canonical].append(new_topic)
    else:
        memory[canonical] = [new_topic]

    return canonical

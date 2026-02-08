import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_word_data(word: str) -> dict:
    """
    Generate meaning and example sentences for a word using OpenAI.
    Returns a dict with meaning, sentence1, and sentence2.
    """
    prompt = f"""You are an SAT vocabulary tutor.

For the given word, generate:
1) A simple SAT level definition (max 25 words)
2) Two example sentences appropriate for a high school student.

Return JSON:
{{
  "meaning": "",
  "sentence1": "",
  "sentence2": ""
}}

Word: {word}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an SAT vocabulary tutor. Always return valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content.strip()

        # Try to extract JSON from the response
        # Sometimes the model returns markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        data = json.loads(content)

        return {
            "meaning": data.get("meaning", ""),
            "example_sentence_1": data.get("sentence1", ""),
            "example_sentence_2": data.get("sentence2", ""),
        }
    except Exception as e:
        print(f"Error generating word data: {e}")
        # Return default values on error
        return {
            "meaning": f"A vocabulary word: {word}",
            "example_sentence_1": f"Example sentence using {word}.",
            "example_sentence_2": f"Another example with {word}.",
        }

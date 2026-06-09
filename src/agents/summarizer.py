import ollama


class EmailSummarizer:

    def __init__(
        self,
        model_name: str
    ):
        self.model_name = model_name

    def summarize_email(
        self,
        email_content: str
    ) -> str:

        prompt = f"""
You are an email assistant.

Return ONLY valid JSON in this format:

{{
  "summary": "...",
  "category": "...",
  "urgency": 1,
  "action_items": []
}}

Rules:
- urgency must be 1 (low), 2 (medium), or 3 (high)
- action_items must be a list of strings
- Do not include any explanation text
- Output must be valid JSON only
Email:
{email_content}
"""

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]
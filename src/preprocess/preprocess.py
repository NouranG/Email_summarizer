import re
from bs4 import BeautifulSoup


class Preprocessor:

    def __init__(self, email_message):
        self.email_message = email_message

    def parse(self):
        html_content = None

        for part in self.email_message.walk():

            if part.get_content_disposition() == "attachment":
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            text = payload.decode("utf-8", errors="ignore")

            if part.get_content_type() == "text/plain":
                return text

            if part.get_content_type() == "text/html":
                html_content = text

        return html_content or ""

    def clean_html(self, text):
        return BeautifulSoup(text, "html.parser").get_text(" ", strip=True)

    def remove_signature(self, text):
        patterns = [
            r"\nBest regards.*",
            r"\nKind regards.*",
            r"\nThanks.*",
            r"\nSent from my iPhone.*"
        ]

        for p in patterns:
            text = re.sub(p, "", text, flags=re.DOTALL | re.IGNORECASE)

        return text.strip()

    def run(self):
        text = self.parse()
        text = self.clean_html(text)
        text = self.remove_signature(text)
        return text
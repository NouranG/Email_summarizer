import re
from email import message_from_bytes
from bs4 import BeautifulSoup

#email parser
class Preprocessor:
    def __init__(self,email_message):
        self.email_message=email_message
    def parser(self):
        html_content = None
        for part in self.email_message.walk():
            content_type = part.get_content_type()
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            text = payload.decode("utf-8", errors="ignore")
            if content_type == "text/plain":
                return text
            elif content_type == "text/html":
                html_content=text

            
        return html_content or ""
    
    def remove_html_tags(self,text):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text(separator=' ',strip=True)
    
    def remove_signatures(self,text):
        patterns = [
    r"\nBest regards,?.*$",
    r"\nKind regards,?.*$",
    r"\nThanks,?.*$",
    r"\nSent from my iPhone.*$"
]
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL|re.IGNORECASE)
        return text.strip()
    
    def preprocess(self):
        raw_text=self.parser()
        text_without_html=self.remove_html_tags(raw_text)
        clean_text=self.remove_signatures(text_without_html)
        return clean_text

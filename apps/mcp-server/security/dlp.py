# apps/mcp-server/security/dlp.py
import re

class DLPProcessor:
    def __init__(self):
        # Basic patterns for PII detection
        self.patterns = {
            "email":    re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
            "ssn":      re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "credit_card": re.compile(r'\b(?:\d[ -]*?){13,16}\b')
        }

    def redact(self, text: str) -> tuple[str, bool]:
        original_text = text
        pii_detected = False
        
        for pii_type, pattern in self.patterns.items():
            if pattern.search(text):
                pii_detected = True
                text = pattern.sub(f"[REDACTED_{pii_type.upper()}]", text)
        
        return text, pii_detected

dlp_processor = DLPProcessor()

class MessageFilter:
    def __init__(self):
        self.keywords = self._load_keywords()
    
    def _load_keywords(self):
        with open("config/keywords.txt", "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    
    def check_keywords(self, text):
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords)
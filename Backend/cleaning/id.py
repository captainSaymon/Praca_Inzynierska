import json
import re

class CleanerID:
    def __init__(self, source, check_name, popularity):
        self.source = source
        self.check_name = check_name
        self.popularity = popularity

        self.check_key = self._check_value()

        self.result = ""
        self.count = 0

        self._reject_by_popularity()

    def getResult(self):
        return self.result, self.count

    def _check_value(self):
        if self.check_name == "movie":
            return "original_title"
        elif self.check_name == "person":
            return "name"
        else:
            return None

    def _contains_latin(self, text):
        if not text:
            return False
        
        pattern = (
            r'['
            r'\u4e00-\u9fff'  # Chiński, Japoński (Kanji), Koreański (Hanja)
            r'\u3040-\u30ff'  # Japoński (Hiragana i Katakana)
            r'\uac00-\ud7af'  # Koreański (Hangul)
            r'\u0600-\u06ff'  # Arabski, Perski, Urdu
            r'\u0750-\u077f'  # Rozszerzony Arabski
            r'\u0590-\u05ff'  # Hebrajski
            r'\u0900-\u097f'  # Hindi, Marathi, Nepalski (Dewanagari)
            r'\u0980-\u09ff'  # Bengalski
            r'\u0e00-\u0e7f'  # Tajski
            r'\u0e80-\u0eff'  # Lao
            r'\u0d80-\u0dff'  # Syngaleski (Sri Lanka)
            r'\u0b80-\u0bff'  # Tamilski
            r'\u0c00-\u0c7f'  # Telugu
            r'\u0370-\u03ff'  # Greka i Koptyjski
            r'\U00010300-\U0001032F'  # Stare pismo italskie (Old Italic)
            r']'
        )
        return not bool(re.search(pattern, text))


    def _reject_by_popularity(self):
        lines = self.source.splitlines()

        check = True
        

        for index, line in enumerate(lines):
            if not line.strip():
                continue

            try:
                glossary = json.loads(line)
                if check:
                    check = False

                if glossary.get("popularity", 0) > self.popularity and self._contains_latin(glossary.get(self.check_key)):
                    self.count += 1
                    self.result += line + "\n"

            except json.JSONDecodeError:
                print(f"Line {index} is not JSON: {line}")

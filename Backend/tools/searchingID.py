import json
import os


# KONIECZNA ZMIANA NA WYSZUKIWANIE PO BAZIE NIE PO PLIKU


class SearcherID:
    def __init__(self, dictionary, file_name, id):
        self._file_path = os.path.join(dictionary, file_name)
        self._id = id

    def search(self):
        with open(self._file_path, "r", encoding="utf-8") as file:
            for _, line in enumerate(file):
                line = line.strip()
                if not line:
                    continue

                item = json.loads(line)
                item_id = item.get('id')
                
                if self._id == item_id:
                    return True
        return False

    
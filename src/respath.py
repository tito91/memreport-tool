class ResPath:
    def __init__(self, text):
        self.text = text
        self.chunks = self.parse_text()

    def parse_text(self):
        chunks = self.text.split('/')
        chunks = chunks[1:]

        last_elem_split = chunks[-1].split('.')
        if last_elem_split[0] == last_elem_split[1]:
            chunks[-1] = last_elem_split[0]

        return chunks

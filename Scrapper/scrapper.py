class Scrapper:
    def __init__(self, scrap_platform: str, user_id: str):
        self.scrap_platform = scrap_platform
        self.user_id = user_id

    def scrap(self, page_no, page_size):
        raise NotImplementedError()

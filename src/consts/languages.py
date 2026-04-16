class Languages:
    ENGLISH = "en"

    @staticmethod
    def to_set():
        return {
            Languages.ENGLISH,
        }

    @staticmethod
    def is_valid(value):
        return value in Languages.to_set()

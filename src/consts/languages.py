class Languages:
    ENGLISH = "en"
    ITALIAN = "it"

    @staticmethod
    def to_set():
        return {
            Languages.ENGLISH,
            Languages.ITALIAN,
        }

    @staticmethod
    def is_valid(value):
        return value in Languages.to_set()

class Icons:
    TUTEL = "tutel.ico"

    @staticmethod
    def to_set():
        return {
            Icons.TUTEL,
        }
    
    @staticmethod
    def is_valid(value):
        return value in Icons.to_set()

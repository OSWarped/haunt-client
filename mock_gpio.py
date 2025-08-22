class GPIO:
    BCM = 'BCM'
    IN = 'IN'
    RISING = 'RISING'

    @staticmethod
    def setwarnings(flag):
        print(f"[MockGPIO] setwarnings({flag})")

    @staticmethod
    def setmode(mode):
        print(f"[MockGPIO] setmode({mode})")

    @staticmethod
    def setup(pin, mode):
        print(f"[MockGPIO] setup(pin={pin}, mode={mode})")

    @staticmethod
    def add_event_detect(pin, edge, callback=None, bouncetime=0):
        print(f"[MockGPIO] add_event_detect(pin={pin}, edge={edge}, bouncetime={bouncetime})")

    @staticmethod
    def cleanup():
        print("[MockGPIO] cleanup()")

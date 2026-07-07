import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TEST_URL: str = "https://api.ipify.org?format=json"
    TIMEOUT_SECONDS: int = 5 #  If time elapsed - then the proxy is dead
    FAST_THRESHOLD_MS: int = 1000

    MONITOR_INTERVAL_SECONDS: int = 300
    UI_REFRESH_INTERVAL_SECONDS: int = 120

    PROXY_BASE_DOMAIN: str = os.getenv("PROXY_BASE_DOMAIN", "http://default_user:default_pass@")

    PROXY_LIST = [
        "45.137.52.205:63958",
        "45.137.52.168:63312",
        "45.137.52.184:64872",
        "154.81.42.62:63590",
        "45.137.52.212:64968",
        "5.42.192.93:62908",
        "45.137.52.77:64160",
        "5.42.192.107:63056",
        "156.233.204.231:64010",
        "156.233.204.98:64010",
        "156.233.204.59:64010",
        "156.246.164.185:64298",
        "45.195.189.183:64024",
        "45.195.189.142:64024",
        "45.195.189.103:64024",
        "45.195.189.99:64024",
        "45.195.189.97:64024",
        "154.81.41.48:63250",
        "166.1.180.242:64976",
        "172.120.158.194:62726",
        "166.88.76.31:63508",
        "185.68.81.82:63194",
        "31.222.249.32:63092",
        "166.1.116.22:64742",
        "154.94.39.132:63988",
        "146.19.15.110:64378",
        "138.249.221.200:62580",
        "138.249.132.69:61962",
    ]


settings = Settings()

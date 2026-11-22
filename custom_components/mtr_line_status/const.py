"""Constants for the MTR Line Status integration."""

DOMAIN = "mtr_line_status"

DEFAULT_SCAN_INTERVAL = 60  # seconds

# Line definitions (code: (english_name, chinese_name, color))
LINES = {
    "TWL": ("Tsuen Wan Line", "荃灣綫", "#FF0000"),
    "KTL": ("Kwun Tong Line", "觀塘綫", "#1A9431"),
    "ISL": ("Island Line", "港島綫", "#0860A8"),
    "SIL": ("South Island Line", "南港島綫", "#99CF16"),
    "TKL": ("Tseung Kwan O Line", "將軍澳綫", "#6B208B"),
    "TCL": ("Tung Chung Line", "東涌綫", "#FE7F1D"),
    "DRL": ("Disneyland Resort Line", "迪士尼綫", "#F550A6"),
    "AEL": ("Airport Express", "機場快綫", "#1C7670"),
    "EAL": ("East Rail Line", "東鐵綫", "#5EB6E4"),
    "TML": ("Tuen Ma Line", "屯馬綫", "#9A3B26"),
}

STATUS_URL = "https://www.mtr.com.hk/alert/ryg_line_status_lite.xml"

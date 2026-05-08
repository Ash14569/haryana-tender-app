import pandas as pd
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://etenders.hry.nic.in/nicgep/app"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print(response.status_code)

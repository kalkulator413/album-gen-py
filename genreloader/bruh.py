from scraper import _OS, _WEBKIT, _SAFARI, _CHROME
from urllib.request import Request, urlopen
import random

counts = {}
url = 'https://cringeassuniversity.com/'

for _ in range(1_000):
    req = Request(url, headers = {'User-Agent': 'Mozilla/5.0 (' + random.choice(_OS) + 
        ') AppleWebKit/' + random.choice(_WEBKIT) + ' (KHTML, like Gecko) Chrome/' + random.choice(_CHROME) + 
        ' Safari/' + random.choice(_SAFARI)})
    res = urlopen(req)

    counts[res.url] = 1 if res.url not in counts else counts[res.url]+1

for key in counts:
    print(key, ":", counts[key])
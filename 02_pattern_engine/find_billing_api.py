import urllib.request
import re
import json

req = urllib.request.Request(
    'https://patternfast.com/user/billing',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
scripts = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', html)
print('Found scripts:', len(scripts))

all_apis = set()
for s in scripts:
    url = s if s.startswith('http') else 'https://patternfast.com' + s
    try:
        js_req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        content = urllib.request.urlopen(js_req, timeout=10).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'["\'](/api/[a-zA-Z0-9_\-\/]+)["\']', content)
        for m in matches:
            if any(k in m for k in ['sub', 'bill', 'plan', 'pay', 'stripe', 'checkout', 'trial', 'portal']):
                all_apis.add(m)
    except Exception as e:
        print(f'Error reading {url}: {e}')

print('Matching API endpoints found:')
for a in sorted(all_apis):
    print(' ', a)

import sys
sys.stdout.reconfigure(encoding='utf-8')
from test_email import build_test_html
html = '<html><head><meta charset="UTF-8"><title>Preview</title></head><body>' + build_test_html() + '</body></html>'
with open('preview_v4.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('preview_v4.html generated')

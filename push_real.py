import urllib.request
import json
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

EMAIL = "3059997913@qq.com"
AUTH_CODE = "jkmfasvsudriddij"
SMTP_HOST = "smtp.qq.com"
SMTP_PORT = 465

URLS = [
    "https://faxian.smzdm.com/json_more?filter=h2s0t0f0c3&page=1",
    "https://faxian.smzdm.com/json_more?filter=h3s0t0f0c3&page=1",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
]

def fetch_data():
    all_items = []
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": url,
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for item in data:
                    all_items.append({
                        "picUrl": item.get("article_pic_url", ""),
                        "title": item.get("article_title", ""),
                        "url": item.get("article_url", ""),
                        "price": item.get("article_price", ""),
                        "voted": str(item.get("article_rating", 0)),
                        "comments": str(item.get("article_comment", 0)),
                        "mall": item.get("article_mall", ""),
                    })
            print(f"获取成功: {url}, 数据条数: {len(data)}")
        except Exception as e:
            print(f"获取失败: {url}, 错误: {e}")
    return all_items

def build_html(items):
    rows = ""
    for item in items[:20]:
        rows += "<tr>"
        rows += "<td width='192' style='padding:0;line-height:0;font-size:0'><img src='" + item["picUrl"] + "' width='192' height='128' style='display:block;max-width:100%;height:auto;'/></td>"
        rows += "<td width='256' style='font-size:1.5em;word-break:break-all'><a target='_blank' href='" + item["url"] + "'>" + item["title"] + "</a></td>"
        rows += "<td width='96' style='font-size:1.2em'>" + item["price"] + "</td>"
        rows += "<td width='32' style='font-size:1.2em'>" + item["voted"] + "/" + item["comments"] + "</td>"
        rows += "<td width='64' style='font-size:1.2em'>" + item["mall"] + "</td>"
        rows += "</tr>\n"

    return """<table border='1' cellpadding='4' cellspacing='0' style='table-layout:fixed;width:640px;word-wrap:break-word;'>
<colgroup>
<col style='width:30%'/>
<col style='width:40%'/>
<col style='width:15%'/>
<col style='width:5%'/>
<col style='width:10%'/>
</colgroup>
<tr>
<th width='192'>图</th>
<th width='256'>标题</th>
<th width='96'>价格</th>
<th width='32'>赞/评</th>
<th width='64'>平台</th>
</tr>
""" + rows + "</table>"

def send_email(html):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "zdm优惠信息汇总(真实数据) " + datetime.now().strftime("%Y-%m-%d %H:%M")
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg.attach(MIMEText(html, "html", "UTF-8"))

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(EMAIL, AUTH_CODE)
        server.sendmail(EMAIL, EMAIL, msg.as_string())
    print("邮件发送成功！")

if __name__ == "__main__":
    print("正在获取什么值得买优惠数据...")
    items = fetch_data()
    if items:
        print(f"共获取 {len(items)} 条数据，开始发送邮件...")
        html = build_html(items)
        send_email(html)
    else:
        print("未获取到数据，可能需要cookie。")

import requests
import time

# 目标汇率
TARGET_RATE = 9.15

API_URL = "https://www.poundsterlinglive.com/index.php?option=com_ajax&module=mixed_live_feed_updated&method=getNewData&cur_list=GBPCNY&format=json"

WECHAT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2c7b1813-53f5-4180-86a1-5a95b03c3328"

alerted = False

last_trade_time = None
last_server_time = None


def get_rate():
    r = requests.get(API_URL, timeout=10)
    data = r.json()

    price = float(data[0]["lastPrice"])
    trade_time = data[0]["tradeTimestamp"]
    server_time = data[0]["serverTimestamp"]

    return price, trade_time, server_time


def send_wechat(rate):
    message = f"""⚠️ 英镑汇率提醒
GBP/CNY 已低于 {TARGET_RATE}
当前汇率: {rate}
"""

    payload = {
        "msgtype": "text",
        "text": {"content": message}
    }

    requests.post(WECHAT_WEBHOOK, json=payload)


while True:
    try:
        rate, trade_time, server_time = get_rate()

        print("当前汇率:", rate)
        print("成交时间:", trade_time)
        print("服务器时间:", server_time)

        if last_trade_time == trade_time:
            print("行情未更新")
        else:
            print("行情更新")

        last_trade_time = trade_time

        if rate < TARGET_RATE and not alerted:
            send_wechat(rate)
            alerted = True

    except Exception as e:
        print("错误:", e)

    time.sleep(120)
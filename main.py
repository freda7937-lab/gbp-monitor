import requests
import os

# -------- 配置 --------
TARGET_RATE = 9.15

# 使用环境变量管理敏感信息
API_URL = "https://www.poundsterlinglive.com/index.php?option=com_ajax&module=mixed_live_feed_updated&method=getNewData&cur_list=GBPCNY&format=json"
WECHAT_WEBHOOK = os.getenv("WECHAT_WEBHOOK")  # 在 Render 设置环境变量

# -------- 获取汇率 --------
def get_rate():
    r = requests.get(API_URL, timeout=10)
    data = r.json()

    price = float(data[0]["lastPrice"])
    trade_time = data[0]["tradeTimestamp"]
    server_time = data[0]["serverTimestamp"]

    return price, trade_time, server_time

# -------- 发送微信消息 --------
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

# -------- 主逻辑 --------
def main():
    try:
        rate, trade_time, server_time = get_rate()

        print("当前汇率:", rate)
        print("成交时间:", trade_time)
        print("服务器时间:", server_time)

        if rate < TARGET_RATE:
            send_wechat(rate)
            print("已触发提醒")
        else:
            print("汇率未低于目标，未触发提醒")

    except Exception as e:
        print("错误:", e)

if __name__ == "__main__":
    main()

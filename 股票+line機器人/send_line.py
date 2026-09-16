import requests
import yfinance as yf

# =========================================================================
# LINE Access Token 密鑰
# =========================================================================
LINE_ACCESS_TOKEN = "ojd1fCfhL7l+0bYBreZ9ejjwCE5ARqIfYtfMylqKL1hnmXinQGW7OxWmbFxQ6Q4kvADoz4Kyo3C6/QuM5OTEwNvogNRLRF0MVEelpaw0U67cQj2Xjn7s/YAeibP3unOjoVik93vi+rrG+47vem8KqwdB04t89/1O/w1cDnyilFU="


def get_market_data():
    rate, price = 31.86, 668.0
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url, timeout=5)
        rate = float(response.json()["rates"]["TWD"])
    except:
        pass
    try:
        ticker = yf.Ticker("AMAT")
        price = float(ticker.fast_info.last_price)
    except:
        pass
    return rate, price


def send_line_broadcast(token, message):
    try:
        url = "https://api.line.me/v2/bot/message/broadcast"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        data = {"messages": [{"type": "text", "text": message}]}
        response = requests.post(url, headers=headers, json=data, timeout=5)

        if response.status_code == 200:
            print("✅ LINE 群發訊息成功！所有好友的手機應該都要響囉！")
        else:
            print(f"❌ LINE 官方退件！錯誤代碼: {response.status_code}")
            print(f"回傳錯誤內容: {response.text}")
    except Exception as e:
        print(f"💥 程式連線發生嚴重錯誤: {e}")


if __name__ == "__main__":
    rate, sell_price_usd = get_market_data()

    # =========================================================================
    # 📝 持股成本設定區
    # 格式：{"shares": 股數, "price": 買入單價美金}
    # =========================================================================
    trades = [
        {"shares": 34, "price": 129.3105},  # 第 1 筆買進
        {"shares": 32, "price": 133.9345},  # 第 2 筆買進
        {"shares": 14, "price": 316.3500},  # 第 3 筆買進（新增加）
    ]

    total_cost = 0.0
    total_profit = 0.0

    # 自動迴圈計算所有買入批次的成本與利潤
    for trade in trades:
        shares = trade["shares"]
        buy_price = trade["price"]

        cost_twd = buy_price * rate * shares
        profit_twd = (sell_price_usd * rate * shares) - cost_twd

        total_cost += cost_twd
        total_profit += profit_twd

    # 計算總報酬率 (% 數)
    if total_cost > 0:
        profit_percentage = (total_profit / total_cost) * 100
    else:
        profit_percentage = 0.0

    sign = "+" if profit_percentage >= 0 else ""

    # 組合定時通知的訊息
    message_text = (
        f"⏰ 每日定時美股損益報告\n"
        f"----------------------\n"
        f"💵 今日美金匯率: {rate:.2f}\n"
        f"🚀 AMAT 目前股價: ${sell_price_usd:.2f}\n"
        f"----------------------\n"
        f"💰 總成本: NT$ {total_cost:,.0f}\n"
        f"📈 總利潤: NT$ {total_profit:,.0f}\n"
        f"📊 總報酬率: {sign}{profit_percentage:.2f}%"
    )

    # 執行群發
    send_line_broadcast(LINE_ACCESS_TOKEN, message_text)

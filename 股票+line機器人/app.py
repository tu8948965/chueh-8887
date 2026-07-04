import streamlit as st
import requests
import yfinance as yf

st.set_page_config(layout="wide")


# ================= 加上 Cache 自動抓取市場數據 =================
@st.cache_data(ttl=900)
def get_market_data():
    rate, price = 31.86, 668.0
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url, timeout=3)
        rate = float(response.json()["rates"]["TWD"])
    except:
        pass
    try:
        ticker = yf.Ticker("AMAT")
        price = float(ticker.fast_info.last_price)
    except:
        pass
    return rate, price


today_rate, amat_latest_price = get_market_data()

# ================= 網頁前端顯示 =================
st.title("📊 美股投資獲利計算器")
st.write("自動抓取今日最新美金匯率與 AMAT 即時股價，隨時掌握資產狀況。")

st.markdown("---")

# ================= 頂部全域設定區域 =================
st.subheader("⚙️ 今日最新市場數據")
col_config1, col_config2 = st.columns(2)

with col_config1:
    rate = st.number_input("💵 美金/台幣匯率", value=today_rate, step=0.01, format="%.2f")
    st.caption(f"💡 今日自動抓取匯率：**{today_rate:.2f}**")

with col_config2:
    sell_price_usd = st.number_input("🚀 一股賣出價格 (美金) - 參考 AMAT 股價", value=amat_latest_price, step=1.0)
    st.caption(f"💡 今日 AMAT 即時股價：**${amat_latest_price:.2f}**")

st.markdown("---")

# ================= 下方固定交易明細與統計 =================
col1, col2, col3 = st.columns([1, 1, 0.8])

# --- 第一筆交易 ---
with col1:
    st.subheader("📌 第一筆交易 2025/8/29")
    shares1 = 34
    buy_price_usd1 = 129.3105
    st.write(f"📈 **固定股數**：{shares1} 股")
    st.write(f"💵 **固定買入價格(美金)**：${buy_price_usd1:.4f}")

    # 計算邏輯
    buy_price_twd1 = buy_price_usd1 * rate
    cost_twd1 = buy_price_twd1 * shares1
    sell_price_twd1 = sell_price_usd * rate        # 一股賣出價格 (台幣)
    revenue_twd1 = sell_price_twd1 * shares1      # 總收益 (台幣)
    profit_twd1 = revenue_twd1 - cost_twd1         # 總利潤 (台幣)
    profit_percent1 = (profit_twd1 / cost_twd1) * 100 if cost_twd1 > 0 else 0.0 # 利潤%數

    st.markdown("##### 📋 計算結果")
    st.text(f"成本(台幣): {cost_twd1:,.2f}")
    st.text(f"一股賣出價格(台幣): {sell_price_twd1:,.2f}")
    st.text(f"總收益(台幣): {revenue_twd1:,.2f}")
    st.text(f"總利潤(台幣): {profit_twd1:,.2f}")
    st.text(f"利潤%數: {profit_percent1:.2f}%")

# --- 第二筆交易 ---
with col2:
    st.subheader("📌 第二筆交易 2026/2/27")
    shares2 = 32
    buy_price_usd2 = 133.9345
    st.write(f"📈 **固定股數**：{shares2} 股")
    st.write(f"💵 **固定買入價格(美金)**：${buy_price_usd2:.4f}")

    # 計算邏輯
    buy_price_twd2 = buy_price_usd2 * rate
    cost_twd2 = buy_price_twd2 * shares2
    sell_price_twd2 = sell_price_usd * rate        # 一股賣出價格 (台幣)
    revenue_twd2 = sell_price_twd2 * shares2      # 總收益 (台幣)
    profit_twd2 = revenue_twd2 - cost_twd2         # 總利潤 (台幣)
    profit_percent2 = (profit_twd2 / cost_twd2) * 100 if cost_twd2 > 0 else 0.0 # 利潤%數

    st.markdown("##### 📋 計算結果")
    st.text(f"成本(台幣): {cost_twd2:,.2f}")
    st.text(f"一股賣出價格(台幣): {sell_price_twd2:,.2f}")
    st.text(f"總收益(台幣): {revenue_twd2:,.2f}")
    st.text(f"總利潤(台幣): {profit_twd2:,.2f}")
    st.text(f"利潤%數: {profit_percent2:.2f}%")

# --- 總計結果 ---
with col3:
    st.subheader("🏆 總體統計")
    st.markdown("---")

    total_cost = cost_twd1 + cost_twd2
    total_revenue = revenue_twd1 + revenue_twd2
    total_profit = profit_twd1 + profit_twd2
    total_profit_percent = (total_profit / total_cost) * 100 if total_cost > 0 else 0.0

    st.metric(label="💰 總成本 (台幣)", value=f"${total_cost:,.0f}")
    st.metric(label="📈 總利潤 (台幣)", value=f"${total_profit:,.0f}")
    st.metric(label="📊 總報酬率", value=f"{total_profit_percent:.2f}%")
    st.markdown("---")
import streamlit as st

# 設定網頁標題
st.set_page_config(page_title="我的股票獲利計算器", layout="centered")

st.title("📈 我的股票獲利計算器")
st.write("在下方輸入你的股票資產，隨時掌握賺賠狀況！")

# 建立輸入區塊（使用表單讓手機輸入更流暢）
with st.form("stock_form"):
    st.subheader("📝 輸入股票資訊")

    stock_name = st.text_input("股票名稱 / 代號", placeholder="例如：台積電 或 2330")

    # 手機版適合排成兩列
    col1, col2 = st.columns(2)
    with col1:
        buy_price = st.number_input("您的買入價格", min_value=0.0, step=0.1, value=100.0)
    with col2:
        shares = st.number_input("持有股數（張=1000股）", min_value=1, step=1, value=1000)

    current_price = st.number_input("🔥 目前最新價格", min_value=0.0, step=0.1, value=105.0)

    submit_button = st.form_submit_button("開始計算損益")

# 當按下計算按鈕
if submit_button:
    # 核心計算邏輯
    total_cost = buy_price * shares  # 投入成本
    current_value = current_price * shares  # 當前市值
    profit = current_value - total_cost  # 賺賠金額
    roi = (profit / total_cost) * 100 if total_cost > 0 else 0.0  # 報酬率

    st.markdown("---")
    st.subheader(f"📊 {stock_name} 的結算結果")

    # 用漂亮的卡片元件顯示數字
    c1, c2 = st.columns(2)
    c1.metric(label="投入成本", value=f"${total_cost:,.0f}")
    c2.metric(label="當前市值", value=f"${current_value:,.0f}")

    # 根據賺賠顯示紅色（賺）或綠色（賠）
    if profit >= 0:
        st.success(f"🎉 目前獲利：**${profit:,.0f}** (報酬率：`+{roi:.2f}%`) ")
    else:
        st.error(f"📉 目前虧損：**${profit:,.0f}** (報酬率：`{roi:.2f}%`) ")
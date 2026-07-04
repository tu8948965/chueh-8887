name: Scheduled LINE Notification

on:
  schedule:
    - cron: '0 0,14 * * *'    # 台灣時間早上 8 點與晚上 10 點
  workflow_dispatch:          # 手動執行開關

jobs:
  run-line-script:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests yfinance

      - name: Run script
        env:
          LINE_NOTIFY_TOKEN: ${{ secrets.LINE_NOTIFY_TOKEN }} # 如果你有設定環境變數的話
        run: python 股票+line機器人/send_line.py  # 👈 這裡請對準你要定時執行的那個 Python 檔案路徑
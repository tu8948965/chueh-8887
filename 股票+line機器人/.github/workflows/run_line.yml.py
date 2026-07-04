name: Scheduled LINE Notification

on:
  schedule:
    - cron: '0 0,14 * * *'    # 這是國際標準時間，換算下來就是台灣時間早上 8 點與晚上 10 點
  workflow_dispatch:          # 👈 這次我們直接把手動執行的按鈕寫進去！

jobs:
  run-line-script:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/checkout@v3
        # 這裡會自動去跑你資料夾裡的 app.py 或你的發送腳本
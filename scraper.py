import requests
import csv
from datetime import datetime
import os
from datetime import datetime, timezone, timedelta

# JSON API endpoint
url = "https://www.cityofperthparking.com.au/json/cpp/map/carpark/alt/0"

# 加 timestamp 避免 cache
params = {
    "_": int(datetime.utcnow().timestamp() * 1000)
}

# 檔名（固定）
filename = "cpp_parking_data.csv"

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # 欄位設定（加埋 timestamp）
    fieldnames = [
        "timestamp","id", "title", "entry_full", "entry", "free_space"
    ]

    # 檢查是否第一次寫入
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # 第一次寫 header
        if not file_exists:
            writer.writeheader()

        # 寫每一行
        # 西澳時間 = UTC+8
        wa_time = datetime.now(timezone.utc) + timedelta(hours=8)
        timestamp = wa_time.strftime('%Y-%m-%d %H:%M:%S')
        for item in data:
            row = {key: item.get(key, "") for key in fieldnames if key != "timestamp"}
            row["timestamp"] = timestamp
            writer.writerow(row)

    print(f"✅ 資料已追加至：{filename}")

except Exception as e:
    print(f"❌ 發生錯誤：{e}")

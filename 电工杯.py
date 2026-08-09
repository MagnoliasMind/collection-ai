import requests
import pandas as pd
from datetime import datetime

lati= 26.05942
longt = 119.198
start_d = "2024-01-01"
end_d = "2024-12-31"
outp = "fzu_qishan_weather_2024.csv"


hour = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "precipitation",
    "weather_code",
    "cloud_cover_total",   
    "wind_speed_10m",
    "wind_direction_10m",
    "shortwave_radiation_instant",
    "is_day"
]

day = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "sunshine_duration"
]

def fetch_weather():
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lati,
        "longitude": longt,
        "start_date": start_d,
        "end_date": end_d,
        "hourly": ",".join(hour),
        "daily": ",".join(day),
        "timezone": "Asia/Shanghai"  
    }

    print(f"[INFO] 正在请求 Open-Meteo API...")
    print(f"[INFO] 坐标: ({lati}, {longt})")
    print(f"[INFO] 时间范围: {start_d} ~ {end_d}")

    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    print(f"Yes")
    return data


def merge_hour(data):
    hourly = data["hourly"]
    df_hourly = pd.DataFrame(hourly)
    df_hourly["time"] = pd.to_datetime(df_hourly["time"])

    daily = data["daily"]
    df_daily = pd.DataFrame(daily)
    df_daily["date"] = pd.to_datetime(df_daily["time"]).dt.date

    df_hourly["date"] = df_hourly["time"].dt.date
    df_merged = pd.merge(df_hourly, df_daily, on="date", how="left")

    df_merged.drop(columns=["date", "time_y"], inplace=True)
    df_merged.rename(columns={"time_x": "datetime"}, inplace=True)

    if "cloud_cover" in df_merged.columns:
        df_merged.rename(columns={"cloud_cover": "cloud_cover_total"}, inplace=True)

    return df_merged


def main():
    try:
        raw_data = fetch_weather()
        df = merge_hour(raw_data)
        df.to_csv(outp, index=False, encoding="utf-8-sig")
        print(f"{len(df)} save in {outp}")
        print(df.head())

    except requests.exceptions.HTTPError as e:
        print(f" requests.exceptions.HTTPError {e}")
    except Exception as e:
        print(f"Exception {e}")


if __name__ == "__main__":
    main()
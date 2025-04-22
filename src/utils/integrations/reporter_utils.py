from datetime import datetime
from zoneinfo import ZoneInfo
import python_weather

async def weather_period_reporter(timezone, locale=None):
    # 1. 時段摘要
    now = datetime.now(ZoneInfo(timezone))
    h = now.hour
    period = (
        "清晨" if 5 <= h < 8 else
        "上午" if 8 <= h < 12 else
        "下午" if 12 <= h < 18 else
        "傍晚" if 18 <= h < 20 else
        "深夜"
    )

    # 2. 天氣摘要
    async with python_weather.Client() as client:
        weather = await client.get('Taipei', unit=python_weather.IMPERIAL, locale=python_weather.Locale.CHINESE_TRADITIONAL_TAIWAN)
        sky_weather = weather.description

    return now.strftime('%Y-%m-%d'), period, sky_weather
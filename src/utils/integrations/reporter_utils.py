from datetime import datetime
from zoneinfo import ZoneInfo
import python_weather

from src.utils.i18n import get_translator
from src import setup_logger

log = setup_logger(__name__)

async def weather_period_reporter(timezone, lang='en-us', location='New York'):
    # 1. time period summary
    tr = get_translator()
    now = datetime.now(ZoneInfo(timezone))
    h = now.hour
    period = (
        tr.t(lang, 'prompt.period.early') if 5 <= h < 8 else
        tr.t(lang, 'prompt.period.morning') if 8 <= h < 12 else
        tr.t(lang, 'prompt.period.afternoon') if 12 <= h < 18 else
        tr.t(lang, 'prompt.period.evening') if 18 <= h < 20 else
        tr.t(lang, 'prompt.period.night')
    )

    # 2. weather summary
    async with python_weather.Client() as client:
        # TODO setup locale based on location
        try:
            weather = await client.get(location, unit=python_weather.IMPERIAL, locale=python_weather.Locale.CHINESE_TRADITIONAL_TAIWAN)
            sky_weather = weather.description
        except Exception as e:
            log.warning(f"Failed to get weather for location {location}: {e}")
            sky_weather = 'Unknown'

    return now.strftime('%Y-%m-%d'), period, sky_weather
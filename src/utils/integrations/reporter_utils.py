from datetime import datetime
from zoneinfo import ZoneInfo
import python_weather

from src.utils.core_utils import Translator

async def weather_period_reporter(timezone, lang='en', location='New York'):
    # 1. time period summary
    translator = Translator(lang)
    now = datetime.now(ZoneInfo(timezone))
    h = now.hour
    period = (
        translator.t('prompt.period.early') if 5 <= h < 8 else
        translator.t('prompt.period.morning') if 8 <= h < 12 else
        translator.t('prompt.period.afternoon') if 12 <= h < 18 else
        translator.t('prompt.period.evening') if 18 <= h < 20 else
        translator.t('prompt.period.night')
    )

    # 2. weather summary
    async with python_weather.Client() as client:
        # TODO setup locale based on location
        weather = await client.get(location, unit=python_weather.IMPERIAL, locale=python_weather.Locale.CHINESE_TRADITIONAL_TAIWAN)
        sky_weather = weather.description

    return now.strftime('%Y-%m-%d'), period, sky_weather
import discord
from discord import app_commands

from src.log import setup_logger
from src.utils.i18n import get_translator

log = setup_logger(__name__)

def get_localized_choices(itn: discord.Interaction, current: str, values: list[str], key_prefix: str, value_calculator: callable) -> list[app_commands.Choice]:
    """
    Generates a list of localized autocomplete options based on user input.

    Args:
        itn: Discord Interaction object, used to get the user's language.
        current: The string the user has currently typed.
        values: A list of base option keys (e.g., ['enable', 'disable']).
        key_prefix: The prefix for the translation keys (e.g., 'binary_state.').
        value_calculator: A callable (function) that takes (index, value_key) as arguments and
                          returns the value of the Choice corresponding to that option.

    Returns:
        A list containing app_commands.Choice objects.
    """
    user_locale = str(itn.locale).lower()
    log.debug(f"Autocomplete locale: {user_locale}")

    current = str(current).lower()
    current = '' if current == 'nan' else current

    tr = get_translator()
    choices = []
    for i, value_key in enumerate(values):
        localized_name = tr.t(user_locale, f'{key_prefix}.{value_key}')

        if current in localized_name.lower():
            try:
                # calculate the value using the provided function and ensure it is a valid type for Choice value
                choice_value = value_calculator(i, value_key)
                if not isinstance(choice_value, (str, int, float)):
                    log.warning(f"Calculated value {choice_value} for {value_key} is not a valid type for Choice value. Converting to string.")
                    choice_value = str(choice_value)

                choices.append(app_commands.Choice(name=localized_name, value=choice_value))
            except Exception as e:
                log.error(f"Error calculating value or creating Choice for '{value_key}': {e}")

    return choices[:25]
from define import VALID_DECK_SIZES

# Dans transformations.py
class DeckParseError(Exception):
    pass

def parse_deck_list(deck_list_raw: str) -> list[tuple[int, str]]:
    warning_message = ""

    # Parse deck list
    number_of_cards = 0
    deck_list = []
    for line_number, line in enumerate(deck_list_raw.splitlines()):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue

        # Skip Maybeboard section
        if line.lower().find('maybeboard') != -1:
            continue

        # Find and remove the extension
        end_index = line.find('(')
        if end_index != -1:
            line = line[:end_index].strip()

        # Find and remove the categories
        end_index = line.find('[')
        if end_index != -1:
            line = line[:end_index].strip()

        # Get the number of card
        card_number_end = line.find('x ')
        if card_number_end == -1:
            raise DeckParseError(f"Error: Invalid card format on line {line_number + 1}")

        card_number = 0
        try:
            card_number = int(line[:card_number_end].strip())
        except ValueError:
            raise DeckParseError(f"Error: Invalid card number on line {line_number + 1}")

        number_of_cards += card_number

        # Get the card name
        card_name = line[card_number_end + 2:].strip()
        deck_list.append((card_number, card_name))

    if number_of_cards == 0:
        raise DeckParseError("Error: The deck is empty")

    if number_of_cards not in VALID_DECK_SIZES:
        warning_message = f"Warning: The deck contains {number_of_cards} cards instead of {VALID_DECK_SIZES}"

    return (deck_list, warning_message)


def _getCardNumber(deck_list, card_name):
    for card_number, name in deck_list:
        if name == card_name:
            return card_number
    return 0


def get_deck_changes(
        deck_list_old: list[tuple[int, str]],
        deck_list_new: list[tuple[int, str]]
        ) -> tuple[str, int]:
    number_of_changes = 0

    # Get added cards
    added_cards = []
    for card_number, card_name in deck_list_new:
        card_number_old = _getCardNumber(deck_list_old, card_name)
        if card_number == 0:
            added_cards.append((card_number, card_name))
            number_of_changes += 1
        elif card_number > card_number_old:
            added_cards.append((card_number - card_number_old, card_name))
            number_of_changes += card_number - card_number_old

    # Get removed cards
    removed_cards = []
    for card_number, card_name in deck_list_old:
        card_number_new = _getCardNumber(deck_list_new, card_name)
        if card_number == 0:
            removed_cards.append((card_number, card_name))
            number_of_changes += 1
        elif card_number > card_number_new:
            removed_cards.append((card_number - card_number_new, card_name))
            number_of_changes += card_number - card_number_new

    # Get changes
    changes_display = f"{number_of_changes} changes :\n"
    changes_copy = ""
    for card_number, card_name in added_cards:
        if card_number > 1:
            changes_display += f"+ {card_number} {card_name}\n"
            changes_copy += f"+ {card_number} {card_name}\n"
        else:
            changes_display += f"+ {card_name}\n"
            changes_copy += f"+ {card_name}\n"

    changes_copy += "\n"

    for card_number, card_name in removed_cards:
        if card_number > 1:
            changes_display += f"- {card_number} {card_name}\n"
            changes_copy += f"- {card_number} {card_name}\n"
        else:
            changes_display += f"- {card_name}\n"
            changes_copy += f"- {card_name}\n"

    changes_display = changes_display[:-1]
    changes_copy = changes_copy[:-1]

    return (changes_display, changes_copy)
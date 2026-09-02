import requests

from define import VERSION, CONTACT_EMAIL, ARCHIDEKT_URL, ARCHIDEKT_API_URL


HEADERS = {
    "User-Agent": f"DeckChanges/{VERSION} ({CONTACT_EMAIL})"
}


def replace_url_by_decklist(raw_text: str) -> str:
    if ARCHIDEKT_URL not in raw_text:
        return raw_text

    index = raw_text.index(ARCHIDEKT_URL)

    url = raw_text[index:].split()[0]
    decklist = _get_decklist_from_archidekt(url)

    return raw_text[:index] + decklist + raw_text[index + len(url):]


def _get_decklist_from_archidekt(url: str) -> str:

    deck_id = _get_deck_id_from_url(url)
    if not deck_id:
        return ""

    url = f"{ARCHIDEKT_API_URL}/decks/{deck_id}/"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return ""

    data = response.json()

    decklist = ""

    for card_entry in data.get("cards", []):

        skip = False
        for category in card_entry["categories"]:
            if category.lower() == "maybeboard":
                skip = True
                break

        if skip:
            continue

        quantity = card_entry["quantity"]
        card_name = card_entry["card"]["oracleCard"]["name"]
        decklist += f"{quantity}x {card_name}\n"

        if card_name == "Dwalin, Weaponmaster":
            print(card_entry)

    return decklist[:-1]


def _get_deck_id_from_url(url: str) -> str:
    if not url.startswith(f"{ARCHIDEKT_URL}/decks/"):
        return ""

    deck_id = url[28:]

    try:
        index = deck_id.index("/")
    except:
        return deck_id

    return deck_id[:index]
import io
import requests
import customtkinter as ctk

from define import VERSION, CONTACT_EMAIL, SCRYFALL_URL, CARD_IMAGE_SIZE
from PIL import Image
from functools import lru_cache

HEADERS = {
    "User-Agent": f"DeckChanges/{VERSION} ({CONTACT_EMAIL})"
}


@lru_cache(maxsize=100)
def get_card_images(
        card_name: str
        ) -> tuple[ctk.CTkImage, ctk.CTkImage | None] | None:
    # Get card info
    url = f"{SCRYFALL_URL}/cards/named?fuzzy={card_name}"

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None

    # Get image url for response
    card_data = response.json()

    if "image_uris" in card_data:
        image = _get_image_from_uris(card_data.get("image_uris"))
        return (image, None)

    elif "card_faces" in card_data:
        card_faces = card_data.get("card_faces")

        image_front = None
        image_back = None

        if "image_uris" in card_faces[0]:
            image_front = _get_image_from_uris(card_faces[0].get("image_uris"))
        if "image_uris" in card_faces[1]:
            image_back = _get_image_from_uris(card_faces[1].get("image_uris"))

        return (image_front, image_back)

    else:
        return None


def _get_image_from_uris(
        image_uris: dict
        ) -> ctk.CTkImage | None:

    image_url = None
    for key in ["png", "normal", "large", "small"]:
        image_url = image_uris.get(key)
        if image_url != None:
            break

    if not image_url:
            return None

    # Get image data
    reponse_image = requests.get(image_url, headers=HEADERS)
    if reponse_image.status_code != 200:
        return None

    image_data = reponse_image.content
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail(CARD_IMAGE_SIZE)

    return ctk.CTkImage(light_image=image, dark_image=image, size=CARD_IMAGE_SIZE)
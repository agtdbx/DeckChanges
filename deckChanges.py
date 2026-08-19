#--------------------------------------------------------------------
# Defines
#--------------------------------------------------------------------

VALID_DECK_SIZES = [40, 60, 100]

#--------------------------------------------------------------------
# Functions
#--------------------------------------------------------------------

def getDeckList(filename):
    # Read file
    readlines = []

    try:
        with open(filename, 'r') as file:
            readlines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File not found '{filename}'")
        return None
    except Exception as e:
        print(f"Error: An error occurred while reading the file '{filename}': {e}")
        return None

    # Parse deck list
    numberOfCards = 0
    deckList = []
    for lineNumber, line in enumerate(readlines):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue

        # Skip Maybeboard section
        if line.lower().find('maybeboard') != -1:
            continue

        # Find and remove the extension
        endIndex = line.find('(')
        if endIndex != -1:
            line = line[:endIndex].strip()

        # Find and remove the categories
        endIndex = line.find('[')
        if endIndex != -1:
            line = line[:endIndex].strip()

        # Get the number of card
        cardNumberEnd = line.find('x ')
        if cardNumberEnd == -1:
            print(f"Error: Invalid card format on line {lineNumber + 1} in file '{filename}'")
            continue

        cardNumber = 0
        try:
            cardNumber = int(line[:cardNumberEnd].strip())
        except ValueError:
            print(f"Error: Invalid card number on line {lineNumber + 1} in file '{filename}'")
            continue

        numberOfCards += cardNumber

        # Get the card name
        cardName = line[cardNumberEnd + 2:].strip()
        deckList.append((cardNumber, cardName))

    if numberOfCards not in VALID_DECK_SIZES:
        print(f"Warning: The deck in file '{filename}' contains {numberOfCards} cards instead of {VALID_DECK_SIZES}.")

    return deckList


def getCardNumber(deckList, cardName):
    for cardNumber, name in deckList:
        if name == cardName:
            return cardNumber
    return 0

#--------------------------------------------------------------------
# Main program
#--------------------------------------------------------------------

import sys

if __name__ == "__main__":
    # Check the number of parameters
    if len(sys.argv) < 3:
        print("Usage: python deckChanges.py <old_deck_list> <new_deck_list>")
        sys.exit(1)

    # Get filenames
    oldDeckFilename = sys.argv[1]
    newDeckFilename = sys.argv[2]

    # Get deck lists
    deckListOld = getDeckList(oldDeckFilename)
    deckListNew = getDeckList(newDeckFilename)

    if deckListOld is None or deckListNew is None:
        sys.exit(1)

    numberOfModifications = 0

    # Get added cards
    addedCards = []
    for cardNumber, cardName in deckListNew:
        cardNumberOld = getCardNumber(deckListOld, cardName)
        if cardNumber == 0:
            addedCards.append((cardNumber, cardName))
            numberOfModifications += 1
        elif cardNumber > cardNumberOld:
            addedCards.append((cardNumber - cardNumberOld, cardName))
            numberOfModifications += cardNumber - cardNumberOld

    # Get removed cards
    removedCards = []
    for cardNumber, cardName in deckListOld:
        cardNumberNew = getCardNumber(deckListNew, cardName)
        if cardNumber == 0:
            removedCards.append((cardNumber, cardName))
            numberOfModifications += 1
        elif cardNumber > cardNumberNew:
            removedCards.append((cardNumber - cardNumberNew, cardName))
            numberOfModifications += cardNumber - cardNumberNew

    # Print modifications
    print(f"Modifications ({numberOfModifications}):")
    for cardNumber, cardName in addedCards:
        if cardNumber > 1:
            print(f"+ {cardNumber} {cardName}")
        else:
            print(f"+ {cardName}")

    print("")

    for cardNumber, cardName in removedCards:
        if cardNumber > 1:
            print(f"- {cardNumber} {cardName}")
        else:
            print(f"- {cardName}")
import random


def draw_cards(count):
    # draw a random card from a normal deck of cards

    ranks = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']
    deck = ranks * 4
    cards = random.sample(deck, count)
    # print(card)
    return cards


if __name__ == '__main__':
    dealerCards = []
    playerCards = []

    drawn_cards = draw_cards(4)
    for index, card in enumerate(drawn_cards):
        if index % 2 == 0:
            dealerCards.append(card)
        else:
            playerCards.append(card)

    print(f"The dealer has {dealerCards}")
    print(f"The player has {playerCards}")

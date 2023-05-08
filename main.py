import random
import pandas as pd

SUITS = ['♠', '♦', '♥', '♣']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
STRATEGY_CODE = {'H': 'Hit', 'S': 'Stand', 'D': 'Double', 'P': 'Split', }


class Deck:
    def __init__(self, num_packs=1):
        self.cards = []
        self.num_packs = num_packs
        self.build(num_packs)

    def build(self, num_packs):
        for _ in range(num_packs):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append((rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop()


class Hand:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.value = 0
        self.blackjack = False
        self.bust = False

    def __repr__(self):
        self.calc_hand()
        class_name = type(self).__name__
        return f"{class_name}(name={self.name}, cards={self.cards!r}, value={self.value!r})"

    def __str__(self):
        self.calc_hand()
        return f'{self.name}: {self.cards} = {self.value}'

    def add_card(self, card):
        self.cards.append(card)

    def calc_hand(self):
        self.value = 0

        aces = []
        for card in self.cards:
            rank = card[0]
            if rank in "TJQK":
                self.value += 10
            elif rank != "A":
                self.value += int(rank)
            else:
                aces.append(card)

        for card in aces:
            if self.value >= 11:
                self.value += 1
            else:
                self.value += 11

        if self.value > 21:
            self.bust = True
        elif self.value == 21:
            self.blackjack = True

    def clear_hand(self):
        self.cards = []
        self.value = 0
        self.blackjack = False
        self.bust = False


def strategy_table(dealer: Hand, player: Hand):
    df = pd.read_csv('Blackjack_strategy.csv', index_col=0)
    # print(df)
    # if player has an ace
    ranks = []
    for card in player.cards:
        if card[0] in "JQK":
            ranks.append("T")
        else:
            ranks.append(card[0])
    ranks.sort()

    dloc = dealer.cards[0][0]
    if dloc in "JQK":
        dloc = "T"

    ploc = ""
    if player.blackjack:
        print("S")
    elif len(player.cards) == 2 and ranks[0] == ranks[1]:
        ploc = ranks[0] + ranks[1]
    elif len(player.cards) == 2 and ranks[1] == "A":
        ploc = ranks[1] + ranks[0]
    else:
        ploc = str(player.value)

    strat = df.loc[ploc][dloc]
    print(f"{ploc} vs dealer's {dloc} = {STRATEGY_CODE[strat]}")
    return strat


def players_turn(dealer: Hand, player: Hand):
    player_stands = False
    while not (player_stands or player.blackjack or player.bust or dealer.blackjack):
        strategy_table(dealer, player)
        inp = input("[H]it, [S]tand, or [D]ouble?: ")
        # TODO: add support for split
        if len(inp) != 0 and (inp[0].upper() == "H"):
            player.add_card(deck.deal())
            print(player)
            if player.value == 21:
                player_stands = True
        elif len(inp) != 0 and (inp[0].upper() == "D"):
            player.add_card(deck.deal())
            print(player)
            player_stands = True
        elif len(inp) != 0 and (inp[0].upper() == "S"):
            player_stands = True


def dealers_turn(dealer: Hand):
    dealer_stands = False
    print(dealer)
    while not (dealer_stands or player.bust or dealer.blackjack or dealer.bust):
        if dealer.value >= 17:
            dealer_stands = True
        elif dealer.value < 17:
            dealer.add_card(deck.deal())
            print(dealer)


def print_game_result(dealer: Hand, player: Hand):
    # TODO: refactor the following
    if player.bust:
        print("Lose")
        return -1
    elif player.blackjack and not dealer.blackjack:
        print("Win")
        return 1
    elif dealer.blackjack and not player.blackjack:
        print("Lose")
        return -1
    elif player.value <= 21 and dealer.bust:
        print("Win")
        return 1
    elif dealer.value < player.value <= 21:
        print("Win")
        return 1
    elif player.value == dealer.value <= 21:
        print("Tie")
        return 0
    elif player.value < dealer.value <= 21:
        print("Lose")
        return -1
    else:
        print("Error: Missed case")
        return 0


if __name__ == '__main__':
    deck = Deck(4)
    deck.shuffle()
    player = Hand("Player")
    dealer = Hand("Dealer")

    play_game = 1
    score = 0
    while play_game == 1:
        for i in range(2):
            dealer.add_card(deck.deal())
            player.add_card(deck.deal())

        print("Dealer:", dealer.cards[0])
        print(player)

        players_turn(dealer, player)
        dealers_turn(dealer)

        score += print_game_result(dealer, player)

        inp = ""
        while inp == "":
            inp = input("Deal another hand? [Y]es/[N]o: ")
            if len(inp) != 0 and (inp[0].upper() == "Y"):
                dealer.clear_hand()
                player.clear_hand()
            elif len(inp) != 0 and (inp[0].upper() == "N"):
                play_game = 0
                print(f"{score = }")
            else:
                inp = ""

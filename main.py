import random
import pandas as pd

SUITS = ['♠', '♦', '♥', '♣']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
ACTIONS = {'H': 'Hit', 'S': 'Stand', 'D': 'Double', 'P': 'Split', }


class Table:
    def __init__(self):
        self.shoe: Deck = Deck(4)
        self.dealer: Player = Player("Dealer")
        self.players: [Player] = []
        self.shoe.shuffle()

    def del_hands(self):
        self.dealer.clear_hands()
        for player in self.players:
            player.clear_hands()

    def add_player(self, name):
        player = Player(name)
        self.players.append(player)
        return player

    def initial_deal(self):
        self.del_hands()
        self.dealer.add_hand()
        for player in self.players:
            player.add_hand()

        for _ in range(2):
            self.dealer.hands[0].add_card(self.shoe.deal())
            for player in self.players:
                for hand in player.hands:
                    hand.add_card(self.shoe.deal())

    def play(self):
        dealer_hand = self.dealer.hands[0]  # Dealer only has one hand
        print(self.dealer.name, dealer_hand.cards[0])   # display dealer's first card
        for player in self.players:
            for hand in player.hands:
                player_stands = False   # set to false for the loop:
                while not (player_stands or hand.blackjack or hand.bust):
                    # loop until player 'stands'
                    if len(hand.cards) < 2:                         # if player splits, they'll only have one card
                        hand.add_card(self.shoe.deal())             # so deal a card to hand
                    print(player.name, hand)
                    inp_string = "[h]it, [s]tand, [d]ouble"
                    if hand.pair: inp_string += ", S[p]lit"         # allow player to split cards if they have a pair
                    inp_string += "?: "
                    inp = input(inp_string)                         # get the player's move
                    if len(inp) != 0 and (inp[0].upper() == "H"):   # Hit
                        hand.add_card(self.shoe.deal())             # deal another card to the player's hand
                        if hand.bust or hand.blackjack:
                            print(player.name, hand)
                            player_stands = True
                    elif len(inp) != 0 and (inp[0].upper() == "S"):  # Stand
                        player_stands = True
                    elif len(inp) != 0 and (inp[0].upper() == "D"):  # Double down
                        hand.add_card(self.shoe.deal())
                        print(player.name, hand)
                        player_stands = True
                    elif hand.pair and len(inp) != 0 and (inp[0].upper() == "P"):  # Split
                        new_hand = player.add_hand()
                        new_hand.add_card(hand.cards.pop(1))

    def dealers_turn(self):
        dealer_hand = self.dealer.hands[0]  # Dealer only has one hand
        dealer_stands = False
        print(self.dealer.name, dealer_hand)
        while not (dealer_stands or dealer_hand.blackjack or dealer_hand.bust):
            if dealer_hand.value >= 17:
                dealer_stands = True
            elif dealer_hand.value < 17:
                dealer_hand.add_card(self.shoe.deal())
                print(self.dealer.name, dealer_hand)

    def calc_game_result(self):
        print("Results:")
        dealer_hand = self.dealer.hands[0]
        print(self.dealer.name, dealer_hand)
        for player in self.players:
            for hand in player.hands:
                # print(player.name, hand)
                # TODO: refactor the following
                if hand.bust:
                    print(player.name, "bust with", hand)
                elif hand.blackjack and not dealer_hand.blackjack:
                    print(player.name, "got blackjack", hand)
                elif dealer_hand.blackjack and not hand.blackjack:
                    print(player.name, "lost with", hand)
                elif hand.value <= 21 and dealer_hand.bust:
                    print(player.name, "won with", hand)
                elif dealer_hand.value < hand.value <= 21:
                    print(player.name, "won with", hand)
                elif hand.value == dealer_hand.value <= 21:
                    print(player.name, "tied with", hand)
                elif hand.value < dealer_hand.value <= 21:
                    print(player.name, "lost with", hand)
                else:
                    print("Error: Missed case")


class Deck:
    def __init__(self, num_packs=1):
        self.cards = []
        self.num_packs = num_packs
        self.build(num_packs)

    def build(self, num_packs):
        # create a list of tuples with all combinations of rank and suit
        # (i.e. 52 playing cards * num_packs of cards)
        for _ in range(num_packs):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append((rank, suit))

    def shuffle(self):
        # randomise the cards in the list
        random.shuffle(self.cards)

    def deal(self):
        # return (and remove) the card at the end of the list
        if len(self.cards) > 1:
            return self.cards.pop()
        else:
            print("insufficient cards remaining")


class Player:
    def __init__(self, name):
        self.name = name
        self.hands = []

    def add_hand(self):
        hand = Hand()
        self.hands.append(hand)
        return hand

    def clear_hands(self):
        self.hands = []


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.blackjack = False
        self.bust = False
        self.pair = False

    def __repr__(self):
        self.calc_hand()
        class_name = type(self).__name__
        return f"{class_name} (cards={self.cards!r}, value={self.value!r})"

    def __str__(self):
        self.calc_hand()
        return f'{self.cards} = {self.value}'

    def add_card(self, card):
        self.cards.append(card)
        self.calc_hand()

    def calc_hand(self):
        # calculate the hand value
        self.value = 0

        aces = 0
        for card in self.cards:
            rank = card[0]
            if rank in "TJQK":      # Ten, Jack, Queen or King
                self.value += 10
            elif rank != "A":       # any number card except Ace
                self.value += int(rank)
            else:
                aces += 1           # count the aces

        # calc the value of each ace, either 1 or 11
        if aces > 0:
            for i in range(aces, 0, -1):
                if self.value + (i * 11) > 21:
                    self.value += 1
                else:
                    self.value += 11

        # bust and blackjack properties for quick access
        if self.value > 21:
            self.bust = True
        elif self.value == 21:
            self.blackjack = True

        # if 2 cards in hand, and both are the same rank, set the pair property to True
        if len(self.cards) == 2 and self.cards[0][0] == self.cards[1][0]:
            self.pair = True
        else:
            self.pair = False

        return self.value


# def strategy_table(dealer: Hand, player: Hand):
#     df = pd.read_csv('Blackjack_strategy.csv', index_col=0)
#     # print(df)
#     # if player has an ace
#     ranks = []
#     for card in player.cards:
#         if card[0] in "JQK":
#             ranks.append("T")
#         else:
#             ranks.append(card[0])
#     ranks.sort()
#
#     dloc = dealer.cards[0][0]
#     if dloc in "JQK":
#         dloc = "T"
#
#     ploc = ""
#     if player.blackjack:
#         print("S")
#     elif len(player.cards) == 2 and ranks[0] == ranks[1]:
#         ploc = ranks[0] + ranks[1]
#     elif len(player.cards) == 2 and ranks[1] == "A":
#         ploc = ranks[1] + ranks[0]
#     else:
#         ploc = str(player.value)
#
#     strat = df.loc[ploc][dloc]
#     print(f"{ploc} vs dealer's {dloc} = {STRATEGY_CODE[strat]}")
#     return strat


if __name__ == '__main__':
    game = Table()
    dave = game.add_player("Dave")
    bob = game.add_player("Bob")
    game.initial_deal()
    game.play()
    game.dealers_turn()
    game.calc_game_result()

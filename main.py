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
        self.dealer.add_hand()
        for player in self.players:
            player.add_hand()

        for _ in range(2):
            self.dealer.hands[0].add_card(self.shoe.deal())
            for player in self.players:
                for hand in player.hands:
                    hand.add_card(self.shoe.deal())

    def play(self):
        print(self.dealer.name, self.dealer.hands[0].cards[0])
        for player in self.players:
            for hand in player.hands:
                player_stands = False
                while not (player_stands or hand.blackjack or hand.bust or self.dealer.hands[0].blackjack):
                    if len(hand.cards) < 2:
                        hand.add_card(self.shoe.deal())
                    print(player.name, hand)
                    inp_string = "[h]it, [s]tand, [d]ouble"
                    if hand.pair: inp_string += ", S[p]lit"
                    inp_string += "?: "
                    inp = input(inp_string)

                    if len(inp) != 0 and (inp[0].upper() == "H"):  # Hit
                        hand.add_card(self.shoe.deal())
                        if hand.value == 21:
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

    def calc_game_result(self):
        # TODO: Implement this
        print("Results:")
        print(self.dealer.name, self.dealer.hands[0])
        for player in self.players:
            for hand in player.hands:
                print(player.name, hand)


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
        for i in range(len(self.hands)):
            del self.hands[i]


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
        self.value = 0

        aces = 0
        for card in self.cards:
            rank = card[0]
            if rank in "TJQK":
                self.value += 10
            elif rank != "A":
                self.value += int(rank)
            else:
                aces += 1

        if aces > 0:
            for i in range(aces, 0, -1):
                if self.value + (i * 11) > 21:
                    self.value += 1
                else:
                    self.value += 11

        if self.value > 21:
            self.bust = True
        elif self.value == 21:
            self.blackjack = True

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
#
#
# def dealers_turn(dealer: Hand):
#     dealer_stands = False
#     print(dealer)
#     while not (dealer_stands or player.bust or dealer.blackjack or dealer.bust):
#         if dealer.value >= 17:
#             dealer_stands = True
#         elif dealer.value < 17:
#             dealer.add_card(deck.deal())
#             print(dealer)
#
#
# def print_game_result(dealer: Hand, player: Hand):
#     # TODO: refactor the following
#     if player.bust:
#         print("Lose")
#         return -1
#     elif player.blackjack and not dealer.blackjack:
#         print("Win")
#         return 1
#     elif dealer.blackjack and not player.blackjack:
#         print("Lose")
#         return -1
#     elif player.value <= 21 and dealer.bust:
#         print("Win")
#         return 1
#     elif dealer.value < player.value <= 21:
#         print("Win")
#         return 1
#     elif player.value == dealer.value <= 21:
#         print("Tie")
#         return 0
#     elif player.value < dealer.value <= 21:
#         print("Lose")
#         return -1
#     else:
#         print("Error: Missed case")
#         return 0


if __name__ == '__main__':
    game = Table()
    dave = game.add_player("Dave")
    game.initial_deal()
    game.play()
    game.calc_game_result()
    game.del_hands()

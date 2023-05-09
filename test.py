import unittest
import main


class TestHand(unittest.TestCase):
    def test_add_card(self):
        """
        Test that it adds a new card
        """
        card = ('A', '♦')
        hand = main.Hand()
        hand.add_card(card)
        self.assertIn(card, hand.cards)

    def test_calc_hand_simple(self):
        """
        Test that it adds multiple cards
        """
        cards = [('6', '♦'), ('5', '♦')]
        hand = main.Hand()
        for card in cards:
            hand.add_card(card)
        self.assertIn(cards[0], hand.cards)
        self.assertIn(cards[1], hand.cards)
        self.assertEqual(hand.value, 11)

    def test_calc_hand_aces(self):
        """
        Test aces switch from 11 to 1
        """
        hand = main.Hand()
        nine = ('9', '♣')
        hand.add_card(nine)
        self.assertEqual(hand.value, 9)

        first_ace = ('A', '♦')
        hand.add_card(first_ace)
        self.assertEqual(hand.value, 20)

        second_ace = ('A', '♣')
        hand.add_card(second_ace)
        self.assertEqual(hand.value, 21)

        third_ace = ('A', '♣')
        hand.add_card(third_ace)
        self.assertEqual(hand.value, 12)

    def test_calc_hand_blackjack(self):
        """
        Test blackjack property changes to True
        """
        hand = main.Hand()
        self.assertFalse(hand.blackjack)

        ten = ('10', '♣')
        hand.add_card(ten)
        ace = ('A', '♣')
        hand.add_card(ace)
        self.assertTrue(hand.blackjack)

    def test_calc_hand_bust(self):
        """
        Test bust property changes to True
        """
        hand = main.Hand()
        self.assertFalse(hand.bust)

        ten = ('10', '♣')
        hand.add_card(ten)
        self.assertFalse(hand.bust)

        nine = ('9', '♣')
        hand.add_card(nine)
        self.assertFalse(hand.bust)

        five = ('5', '♣')
        hand.add_card(five)
        self.assertTrue(hand.bust)

    def test_calc_hand_pair(self):
        """
        Test the pair property changes to True, but only
        when exactly 2 card in hand
        """
        hand = main.Hand()
        self.assertFalse(hand.pair)

        ten = ('10', '♣')
        hand.add_card(ten)
        self.assertFalse(hand.pair)

        ten2 = ('10', '♥')
        hand.add_card(ten2)
        self.assertTrue(hand.pair)

        ten3 = ('10', '♦')
        hand.add_card(ten3)
        self.assertFalse(hand.pair)


if __name__ == '__main__':
    unittest.main()

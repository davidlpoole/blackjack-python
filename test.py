import unittest
import main


class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = main.Hand()

    def tearDown(self):
        del self.hand

    def test_add_card(self):
        """
        Test that it adds a new card
        """
        card = ('A', '♦')
        self.hand.add_card(card)
        self.assertIn(card, self.hand.cards)

    def test_calc_hand_simple(self):
        """
        Test that it adds multiple cards
        """
        cards = [('6', '♦'), ('5', '♦')]
        for card in cards:
            self.hand.add_card(card)
        self.assertIn(cards[0], self.hand.cards)
        self.assertIn(cards[1], self.hand.cards)
        self.assertEqual(self.hand.value, 11)

    def test_calc_hand_aces(self):
        """
        Test aces switch from 11 to 1
        """
        nine = ('9', '♣')
        self.hand.add_card(nine)
        self.assertEqual(self.hand.value, 9)

        first_ace = ('A', '♦')
        self.hand.add_card(first_ace)
        self.assertEqual(self.hand.value, 20)

        second_ace = ('A', '♣')
        self.hand.add_card(second_ace)
        self.assertEqual(self.hand.value, 21)

        third_ace = ('A', '♣')
        self.hand.add_card(third_ace)
        self.assertEqual(self.hand.value, 12)

    def test_calc_hand_blackjack(self):
        """
        Test blackjack property changes to True
        """
        self.assertFalse(self.hand.blackjack)

        ten = ('10', '♣')
        self.hand.add_card(ten)
        ace = ('A', '♣')
        self.hand.add_card(ace)
        self.assertTrue(self.hand.blackjack)

    def test_calc_hand_bust(self):
        """
        Test bust property changes to True
        """
        self.assertFalse(self.hand.bust)

        ten = ('10', '♣')
        self.hand.add_card(ten)
        self.assertFalse(self.hand.bust)

        nine = ('9', '♣')
        self.hand.add_card(nine)
        self.assertFalse(self.hand.bust)

        five = ('5', '♣')
        self.hand.add_card(five)
        self.assertTrue(self.hand.bust)

    def test_calc_hand_pair(self):
        """
        Test the pair property changes to True, but only
        when exactly 2 card in hand
        """
        self.assertFalse(self.hand.pair)

        ten = ('10', '♣')
        self.hand.add_card(ten)
        self.assertFalse(self.hand.pair)

        ten2 = ('10', '♥')
        self.hand.add_card(ten2)
        self.assertTrue(self.hand.pair)

        ten3 = ('10', '♦')
        self.hand.add_card(ten3)
        self.assertFalse(self.hand.pair)


if __name__ == '__main__':
    unittest.main()

import random #To shuffle cards and deal them
import sys #To exit

# Declaring the general variables
numbers = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
suits = ['♠', '♣', '♥', '♦']
deck = []
player_hand = []
dealer_hand = []

def display(card:list) -> str:
    '''The format to display a card
    Takes the information about a card and displays it as |(Number)(Suit)|'''
    return '|'+card[0]+card[1]+'|'

def value(card:list) -> int:
    '''Calculates the numerical value of a specific card'''
    if card[0] in ['J','Q','K']:
        return 10
    if card[0] == 'A':
        return 1
    return int(card[0])

def hand_value(hand:list) -> int:
    '''Adds up the value of all cards in a hand'''
    total = 0
    for card in hand:
        total += value(card)
    return total

def display_hand(is_dealer:bool, hand:list) -> str:
    '''Display format for each hand
    Depends on whether it's the dealer or the player's hand'''
    line = display(hand[0])
    if is_dealer:
        line += ' ; |X|'
    else: line += f' ; {display(hand[1])}'
    if len(hand)>2:
        for card in hand[2:]:
            line += f' ; {display(card)}'
    if is_dealer is False:
        line += f' (Total : {hand_value(hand)})'
    return line

def check_bust(hand: list) -> bool:
    '''Checks if a hand is above 21'''
    if hand_value(hand) > 21:
        return True
    return False

def check_blackjack(hand: list) -> bool:
    '''Checks if a hand has a blackjack (Ace and a value 10 card)'''
    return hand_value(hand) == 11 and (hand[0][0] == 'A'  or hand[1][0] == 'A') and len(hand) == 2

def display_table(is_hidden:bool, dealer_hand:list, player_hand:list) -> str:
    '''Display format for the table'''
    if is_hidden:
        return f'''
==> Table:
- The dealer's hand:
{display_hand(True, dealer_hand)}
- Your hand:
{display_hand(False, player_hand)} 
'''
    return f'''
==> Table:
- The dealer's hand:
{display_hand(False, dealer_hand)}
- Your hand:
{display_hand(False, player_hand)} 
'''

if __name__ == '__main__':
    print('--> Welcome to BlackJack <--')

    # Deck Creation and Shuffling
    for suit in suits:
        for number in numbers:
            deck.append([number, suit])
    random.shuffle(deck)
   
    # Initial Dealing
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
   
    # Instructions
    print('''
    ==> Instructions <==                
    - Press 'h' or 'hit' to hit.                 
    - Press 's' or 'stand' to stand.   
    - Press 'q' or 'quit' to quit.
    ''')
   
    # Gameplay
    while True:
        print(display_table(True, dealer_hand, player_hand))
        if check_blackjack(dealer_hand):
            print(display_table(False, dealer_hand, player_hand))
            print('Dealer got a blackjack! He wins!')
        elif check_blackjack(player_hand):
            print(display_table(False, dealer_hand, player_hand))
            print('You got a blackjack! You win!')
        try:
            cmd = input('> ')
            if cmd.lower() in ['q', 'quit']:
                sys.exit()
            elif cmd.lower() in ['h', 'hit']:
                player_hand.append(deck.pop())
            elif cmd.lower() in ['s', 'stand']:
                if check_bust(dealer_hand) or check_bust(player_hand):
                    pass
                else:
                    print(display_table(False, dealer_hand, player_hand))
                    if hand_value(dealer_hand) > hand_value(player_hand):
                        print('Dealer Wins!')
                    elif hand_value(dealer_hand) < hand_value(player_hand):
                        print('Player Wins!')
                    else: print('Draw!')
                    break
            else: raise TypeError
        except TypeError:
            print('The dealer didn\'t understand what you just said, try again!')
        if hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.pop())
        if hand_value(player_hand) > 21:
            print(display_table(False, dealer_hand, player_hand))
            print('You busted, Dealer wins!')
            break
        if hand_value(dealer_hand) > 21 and hand_value(player_hand) <= 21:
            print(display_table(False, dealer_hand, player_hand))
            print('Dealer busted, you win!')
            break

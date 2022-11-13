### BLACK JACK ###

values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 
            'Ten', 'Jack', 'Queen', 'King', 'Ace')

import random


class Card:
    '''Class for card. Card has two attributes: suit and rank. 
    We use dictionary called "values" to determine value of each card.'''
    def __init__(self, suits, ranks):
        self.suits = suits
        self.ranks = ranks
        self.values = values[ranks]
    
    def __str__(self):
        return self.ranks + ' of ' + self.suits 


class Deck:
    '''Class for deck. Deck is a list of class objects. 
    Deck has three functions: 1. magic __str__ to print 2. shuffle - to suffle the deck 3. deal - to give player a card from the deck.'''
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                new_card = Card(suit, rank)
                self.deck.append(new_card)
    
    def __str__(self):
        return "There are " + str(len(self.deck)) + " cards inside"

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        new_card = self.deck.pop()
        return new_card


class Hand:
    '''Class Hand. This is list of cards for each player. Also there is value attribute to compare players card. Aces attribute is to adjust hand if necessary.
    There are two functions: 1. add_card - to add card in hand 2. Adjust for ace - to adjust value if necessary. Ace can be counted as 1 or as 10 depending on value in your hand.'''
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value = self.value + values[card.ranks]
        if card.ranks == 'Ace':
            self.aces += 1
            
    def adjust_for_ace(self):
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    '''This class is to count chips for each player. There are two classes: 1. win_bet - add chips if player wins 2. lose_bet - subtrack chips if player loose'''
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet 
    
    def lose_bet(self):
        self.total -= self.bet



### Functions ###

def take_bet(chips):
    '''Function asks player for a bet.'''
    while True:
        try:
            chips.bet = int(input("What is your bet? "))
        except ValueError:
            print("Please enter a number.")
            continue
        else:
            if chips.bet > chips.total:
                print(f"You don't have enough chips. Total chips is {chips.total}")
                continue
            else:
                break


def hit(deck,hand):
    '''Add card into hand and adjust for ace.'''
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck,hand):
    '''Player has two options: 1. hit - take one more card from the deck 2. stand - pass his turn.
    If player takes card and the total value is more or equal to 21 we break the loop.'''
    global playing  # to control an upcoming while loop
    x = 'a'
    while x != 'h' or x != 's':
        x = input("\nDo you whish to hit or stand? Print h or s: ")
        if x == 'h':
            hit(deck, hand)
            print(f"You get {hand.cards[-1]}. Your current value is {hand.value}")
            break
        elif x == 's':
            print("Stand for now\n")
            playing = False
            break
        else:
            print("Please enter h or s to continue game.")
            continue


def show_some(player,dealer):
    '''Shows one dialer card and all player cards. Also, shows player's total value
    We show all dialer cards if player's total value more or equal to 21 or player pass his turn.'''
    print("Dealer cards:", '\n', "<hidden card>", sep = '')
    print("Second card is", dealer.cards[1])
    print("\nPleyer cards are:")
    print(*player.cards, sep = ' and ')
    print(f"Player total value: {player.value}")
    
def show_all(player,dealer):
    '''Shows all cards and values.'''
    print("Player cards are", *player.cards)
    print(f"Player total value is {player.value}")
    print("Dealer cards are", *dealer.cards)
    print(f"Dealer total value is {dealer.value}")


### Adjust player and dealer chips ###
def player_busts(chips):
    '''Decrease player's total chips value'''
    chips.lose_bet()

def player_wins(chips):
    '''Increase player's total chips value'''
    chips.win_bet()

def dealer_busts(chips):
    '''Decrease dealer total chips value 
    Does not work for now since dealer can not place a bet'''
    chips.lose_bet()
    
def dealer_wins(chips):
    '''Increase dealer total chips value
    Does not work for now since dealer can not place a bet'''
    chips.win_bet()
    
def push():
    '''Dealer and player total card value is equal.'''
    print("Dealer and Player tie! It's a push.")
###



###### GAME LOGIC ######
player_chips = Chips()
automative_player_chips = Chips()

while True:
    # Print an opening statement
    print("Let's start playing Black Jack")
    
    # Create & shuffle the deck, deal two cards to each player
    current_deck = Deck()
    current_deck.shuffle()
    player = Hand()
    automative_player = Hand()
    player.add_card(current_deck.deal())
    player.add_card(current_deck.deal())
    automative_player.add_card(current_deck.deal())
    automative_player.add_card(current_deck.deal())
    
        
    # Set up the Player's chips
    #player_chips = Chips()
    #automative_player_chips = Chips()
    
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player, automative_player)
    
    playing = True
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(current_deck, player)
        
        # Show cards (but keep one dealer card hidden)
        #show_some(player, automative_player)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value >= 21:
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    while automative_player.value <= 17:
        hit(current_deck, automative_player)
        
    show_all(player, automative_player)
        # Show all cards
    
        # Run different winning scenarios
    if player.value <= 21 and automative_player.value <= 21:
        if player.value < automative_player.value:
            dealer_wins(automative_player_chips)
            player_busts(player_chips)
            print("\nDealer wins")
        elif player.value > automative_player.value:
            player_wins(player_chips)
            dealer_busts(automative_player_chips)
            print("\nPlayer wins")
        elif player.value == automative_player.value:
            push()
    elif player.value > 21 and automative_player.value <= 21:
        dealer_wins(automative_player_chips)
        player_busts(player_chips)
        print("\nDealer wins")
    elif player.value <= 21 and automative_player.value > 21:
        player_wins(player_chips)
        dealer_busts(automative_player_chips)
        print("\nPlayer wins")
    elif player.value > 21 and automative_player.value > 21:
        dealer_busts(automative_player_chips)
        player_busts(player_chips)
        print("All players loose")
        
    # Inform Player of their chips total 
    print("Your total chips is:", player_chips.total)
    # Ask to play again
    choose = input("Would you like to play again? Y/N: ")
    if choose == 'N':
        break
    elif choose == 'Y':
        continue
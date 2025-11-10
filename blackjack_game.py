## BlackJack Game ##
import random
import time
import os
from colorama import init, Fore

#Initialize colorama for colored text in terminal
init(autoreset=True)

#---------------------------------------
# Utility Functions
#---------------------------------------

def clear_screen():
    """Clears the console screen for a cleaner game experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(seconds=1):
    """Pauses execution briefly for smoother pacing."""
    time.sleep(seconds)

def format_hand(hand):
    """Formats a hand of card tuples for readable display."""
    formatted = []
    for card in hand:
        if isinstance(card, tuple) and len(card) == 2:
            suit, rank = card
            formatted.append(f"{rank}{suit}") # e.g., "A♠"
        else:
            formatted.append(str(card))      # Fallback for unexpected formats
    return " ".join(formatted)

#---------------------------------------
#Blackjack Game Functions
#---------------------------------------

# Create Deck
def create_deck():
    suits = ["♥", "♦", "♣", "♠"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = []

    #Build the deck by combining every suit + rank 
    for suit in suits:
        for rank in ranks:
            deck.append((suit, rank))   #each card stored as a tuple
    random.shuffle(deck)                # optional shuffle for unpredictable card order
    return deck

# Draw Card(s)
def draw_card(deck, num_cards=1):
    """
    Draws cards from the deck.
    Parameters:
        deck (list): the current deck of cards
        num_cards (int): how many cards to draw (default = 1)
    Returns:
        (deck, hand): tuple containing the updated deck and the drawn hand
    """
    hand = []                   #Stores drawn cards in list
    for _ in range(num_cards):
        if deck:                #Only draw if deck still contains cards
            card = deck.pop()   #Remove & return the last card in the deck
            hand.append(card)   #Add that card to the hand
    return deck, hand

# Dealing Initial Cards
def deal_initial_cards(deck):
    deck, player_hand = draw_card(deck, 2) #Draw 2 cards for player
    deck, dealer_hand = draw_card(deck, 2) #Draw 2 cards for dealer
    return deck, player_hand, dealer_hand

#---------------------------------------
# Calculating Value in Hand
#---------------------------------------

def calculate_hand_value(hand):
    if not hand:               #Check for empty hand
        return 0
    total = 0
    aces = 0
    for card in hand:
        rank = card[1]         #Extracts rank of the card tuple 
        if rank.isdigit():
            total += int(rank) #Numeric cards add their face value

        elif rank in ["J", "K", "Q"]:
            total += 10         #Face cards add 10
        
        elif rank == "A":
            aces += 1           #Track number of aces
            total += 11         #Initially count Ace as 11

    while total >21 and aces > 0:
        total -= 10  # Downgrade an Ace from 11 to 1
        aces -= 1    # Reduce the Ace count

    return total

#---------------------------------------
# Gameplay Functions
#---------------------------------------

#Player Turn -- Hit or Stay?
def player_turn(deck, player_hand):
    while True:
        total = calculate_hand_value(player_hand)
        print(Fore.CYAN + f"\nYour hand: {format_hand(player_hand)} | Total value: {total}")

        if total > 21:
            print(Fore.RED + "💥Bust! You exceeded 21.")
            return deck, player_hand, True # Indicate bust
        
        choice = input(Fore.YELLOW + "Do you want to 'hit' or 'stand' (h/s)? ").lower()

        if choice == 'h':
            deck, new_card = draw_card(deck, 1)
            player_hand.extend(new_card) #Add new card to player's hand
            print(Fore.GREEN + f"You drew: {format_hand(new_card)}")
            pause(0.8)
        elif choice == 's':
            print(Fore.MAGENTA + "You stand. \n")
            pause(1)
            return deck, player_hand, False # No bust
        else:
            print(Fore.RED + "Invalid choice. Please enter 'h' or 's'.")

#IV. Dealer Turn
def dealer_turn(deck, dealer_hand):
    while True:
        total = calculate_hand_value(dealer_hand)
        print(Fore.LIGHTYELLOW_EX + f"Dealer's hand: {format_hand(dealer_hand)} | Total value: {total}")
        pause(1)

        if total <= 16:
            print(Fore.YELLOW + "Dealer hits...")
            deck, new_card = draw_card(deck, 1)
            dealer_hand.extend(new_card) #Add new card to dealer's hand
            pause(1)

        else:
            if total > 21:
                print(Fore.RED + "💀 Dealer busts!")
            else:
                print(Fore.CYAN + "Dealer stands.")
            return deck, dealer_hand, total > 21 # Return bust status
        
#V. Determine Winner
def determine_winner(player_hand, dealer_hand, player_bust, dealer_bust):
    player_total = calculate_hand_value(player_hand)
    dealer_total = calculate_hand_value(dealer_hand)

    print(Fore.LIGHTWHITE_EX + "\n------------------------------")
    print(Fore.LIGHTCYAN_EX + f"Player total: {player_total} | Dealer total: {dealer_total}")
    print(Fore.LIGHTWHITE_EX + "------------------------------")
    pause(1)

    if player_bust:
        print(Fore.RED + "Dealer wins - player busted.")
    elif dealer_bust:
        print(Fore.GREEN + "🎉 Player wins - dealer busted!")
    else:
        if player_total > dealer_total:
            print(Fore.GREEN + "🎉 Player wins!")
        elif dealer_total > player_total:
            print(Fore.RED + "💀 Dealer wins.")
        elif player_total == dealer_total:
            print(Fore.MAGENTA + "🤝 It's a tie!")

#VI. Check for Blackjack
def check_for_blackjack(hand):
    """Check if the hand is a blackjack (Ace + 10-value card)."""
    return calculate_hand_value(hand) == 21 and len(hand) == 2

#VII. Play Again?
def ask_play_again():
    while True:
        response = input(Fore.YELLOW + "Do you want to play again? (y/n): ").lower()
        if response == 'y':
            clear_screen()
            return True
        if response == 'n':
            print(Fore.CYAN + "\nThanks for playing! 👋")
            pause(1.5)
            return False
        else:
            print(Fore.RED + "Invalid input. Please enter 'y' or 'n'.")

#-------------------------------
# Main Game Loop
#-------------------------------

def play_blackjack():
    clear_screen()
    print(Fore.MAGENTA + "===================================")
    print(Fore.CYAN + "        ♠♥ Welcome to ♣♦")
    print(Fore.YELLOW + "          PYTHON BLACKJACK")
    print(Fore.MAGENTA + "===================================")
    print(Fore.LIGHTWHITE_EX + "Rules:")
    print(" - Try to get as close to 21 as possible.")
    print(" - Face cards = 10, Aces = 1 or 11.")
    print(" - Type 'h' to hit or 's' to stand.")
    print(" - If you go over 21, you bust.")
    print(Fore.MAGENTA + "===================================")
    input(Fore.YELLOW + "Press Enter to start the game...")
    clear_screen()

    while True:
        print(Fore.YELLOW + "\n🎲 Starting a new round...")
        pause(1)
        dealing_deck = create_deck()                                        #New shuffled deck each round
        deck, player_hand, dealer_hand = deal_initial_cards(dealing_deck)   #Initial deal
        
        print(Fore.LIGHTYELLOW_EX + f"Dealer's visible card: {format_hand(dealer_hand[0])}")
        print(Fore.CYAN + f"Your hand: {format_hand(player_hand)}")
        print(Fore.CYAN + f"Your total value: {calculate_hand_value(player_hand)}")
        pause(1)

        #Check for blackjacks
        if check_for_blackjack(player_hand) and check_for_blackjack(dealer_hand):
            print(Fore.MAGENTA + "\nBoth player and dealer have blackjack! It's a tie!")
            if not ask_play_again():
                break
            continue
        elif check_for_blackjack(player_hand):
            print(Fore.GREEN + "\n🎉 Player has blackjack! Player wins!")
            if not ask_play_again():
                break
            continue
        elif check_for_blackjack(dealer_hand):
            print(Fore.RED + "\n💀 Dealer has blackjack! Dealer wins!")
            if not ask_play_again():
                break
            continue  

        deck, player_hand, player_bust = player_turn(deck, player_hand)     #Player's turn

        if not player_bust:
            print(Fore.LIGHTYELLOW_EX + "\nDealer's turn...")
            pause(1)
            deck, dealer_hand, dealer_bust = dealer_turn(deck, dealer_hand) #Dealer's turn
        else:
            dealer_bust = False                                              #If player busts, dealer bust status is irrelevant

        determine_winner(player_hand, dealer_hand, player_bust, dealer_bust) 

        if not ask_play_again():
            clear_screen()
            print(Fore.MAGENTA + "===================================")
            print(Fore.CYAN + "       Thanks for playing!")
            print(Fore.YELLOW+ "      Hope you had fun :)")
            print(Fore.MAGENTA + "===================================")
            pause(2)
            break

if __name__ == "__main__":
    print(Fore.CYAN + "Welcome to Blackjack! Let's play!")
    play_blackjack()
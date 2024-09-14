from DeckOfCards import *
from snark import *


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"


# score handler for dealing with aces
def score_keeper(score, card):
    if card.val == 11 and score + 11 > 21:
        return score + 1
    else:
        return score + card.val


# logic for determining if the user beat the dealer
def did_you_beat_the_dealer(score, dealer_score):
    if score > dealer_score:
        print(f"{RED}The dealer's final score is:{RESET}", dealer_score)
        print(f"{MAGENTA}{snark.win_dealer_under()}{RESET}")
    elif dealer_score > 21:
        print(f"{RED}The dealer's final score is:{RESET}", dealer_score)
        print(f"{MAGENTA}{snark.win_dealer_bust()}{RESET}")
    elif score < dealer_score and dealer_score <= 21:
        print(f"{GREEN}The dealer's final score is:{RESET}", dealer_score)
        print(f"{MAGENTA}{snark.lose_dealer()}{RESET}")
    elif score == dealer_score:
        print(f"{YELLOW}Well that's awkward, you and the dealer both got:{RESET}", score)
    else:
        print(f"{RED}Really not sure how you got here, but we'll say you lost{RESET}")


# logic for determining if the game is over
# game_over, player_won
def game_status_checker(score, hit_number):
    if score > 21:
        print(f"{MAGENTA}{snark.hit_bust()}{RESET}")
        return True, False
    elif score == 21:
        print(f"{MAGENTA}{snark.blackjack()}{RESET}")
        return True, True
    elif score < 21 and hit_number > 0:
        print(f"{MAGENTA}{snark.hit_success()}{RESET}")
        return False, None
    else:
        return False, None


# logic for dealing the house
def deal_the_house(deck):
    # dealer card dealing loop
    dealer_score = 0
    dcard1 = deck.get_card()
    print(f"Dealer card 1: {CYAN}{dcard1}{RESET}")
    dealer_score = score_keeper(dealer_score, dcard1)
    dcard2 = deck.get_card()
    print(f"Dealer card 2: {CYAN}{dcard2}{RESET}")
    dealer_score = score_keeper(dealer_score, dcard2)
    print(f"{GREEN}Dealer's starting score is:{RESET}", dealer_score)

    while True:
        # check if the dealer's score is less than 17
        if dealer_score < 17:
            card3 = deck.get_card()
            print(f"Hit: {CYAN}{card3}{RESET}")
            dealer_score = score_keeper(dealer_score, card3)
        else:
            break
    return dealer_score


# logic for asking the user if they would like to play again
def play_again():
    while True:
        again = input("\n\nWould you like to play again? (y/n): ")
        if again == 'y':
            return True
        elif again == 'n':
            return False
        else:
            print("\nCan you read?")


# initiate snarkiness
snark = Snark()


# main game loop
print("Welcome to Snarkjack")
while True:
    # create a new deck of cards and shuffle it
    print("Deck before shuffling:")
    deck = DeckOfCards()
    deck.print_deck()
    print("\nDeck after shuffling:")
    deck.shuffle_deck()
    deck.print_deck()

    # deal two cards to the user
    card = deck.get_card()
    print(f"\n\nCard 1: {CYAN}{card}{RESET}")
    card2 = deck.get_card()
    print(f"Card 2: {CYAN}{card2}{RESET}")

    score = 0
    # calculate the user's hand score
    score = score_keeper(score, card)
    score = score_keeper(score, card2)
    print(f"{GREEN}Your starting score is:{RESET}", score)

    # user card dealing loop
    hit_number = 0
    game_over = False
    player_won = False
    while True:
        # if the user gets 21 or goes over, end the game
        game_over, player_won = game_status_checker(score, hit_number)
        if game_over:
            break

        # ask user if they would like a "hit" (another card)
        hit = input("\nWould you like a hit? (y/n): ")

        if hit == 'y':
            card3 = deck.get_card()
            score = score_keeper(score, card3)
            print(f"{CYAN}{card3}{RESET}")
            print(f"{CYAN}New score:{RESET}", score)
        elif hit == 'n':
            print(f"{MAGENTA}{snark.stand()}{RESET}")
            print(f"{CYAN}Your final score is:{RESET}", score)

            # check if the game is over
            game_over, player_won = game_status_checker(score, hit_number)
            if game_over:
                break
            # if the user didn't lose, deal the house and check if the user beat the dealer
            else:
                print("\nLet's see if you can beat the dealer...")
                dealer_score = deal_the_house(deck)
                did_you_beat_the_dealer(score, dealer_score)
            # finish the round
            break
        else:
            print("\nInvalid input")

        hit_number += 1

    # ask if the player would like to go again
    go_again = play_again()
    if go_again and player_won:
        print(f"{MAGENTA}{snark.play_again_win()}{RESET}")
    elif go_again and not player_won:
        print(f"{MAGENTA}{snark.play_again_lose()}{RESET}")
    elif not go_again and player_won:
        print(f"{MAGENTA}{snark.no_play_again_win()}{RESET}")
        break
    elif not go_again and not player_won:
        print(f"{MAGENTA}{snark.no_play_again_lose()}{RESET}")
        break

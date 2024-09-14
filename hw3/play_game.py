from DeckOfCards import *
from snark import *


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
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
        print(f"{GREEN}The dealer's score is:{RESET}", dealer_score)
        print(snark.win_dealer_under())
    elif dealer_score > 21:
        print(f"{GREEN}The dealer's score is:{RESET}", dealer_score)
        print(snark.win_dealer_bust())
    elif score < dealer_score and dealer_score <= 21:
        print(f"{RED}The dealer's score is:{RESET}", dealer_score)
        print(snark.lose_dealer())
    elif score == dealer_score:
        print(f"{YELLOW}well that's awkward, you and the dealer both got:{RESET}", score)
    else:
        print(f"{RED}not sure how you got here, but we'll say you lost{RESET}")


# logic for determining if the game is over
# game_over, player_won
def game_status_checker(score, hit_number):
    if score > 21:
        print(snark.hit_bust())
        return True, False
    elif score == 21:
        print(snark.blackjack())
        return True, True
    elif score < 21 and hit_number > 0:
        print(snark.hit_success())
        return False, None
    else:
        return False, None


# logic for dealing the house
def deal_the_house(deck):
    # dealer card dealing loop
    dealer_score = 0
    while True:
        # check if the dealer's score is less than 17
        if dealer_score < 17:
            card4 = deck.get_card()
            dealer_score = score_keeper(dealer_score, card4)
        else:
            break
    return dealer_score


# logic for asking the user if they would like to play again
def play_again():
    while True:
        again = input("\n\nwould you like to play again? (y/n): ")
        if again == 'y':
            return True
        elif again == 'n':
            return False
        else:
            print("\ncan you read?")


# initiate snarkiness
snark = Snark()


# main game loop
while True:
    # create a new deck of cards and shuffle it
    deck = DeckOfCards()
    deck.shuffle_deck()

    # deal two cards to the user
    card = deck.get_card()
    card2 = deck.get_card()

    score = 0
    # calculate the user's hand score
    score = score_keeper(score, card)
    score = score_keeper(score, card2)
    print(f"\n{GREEN}Your starting score is:{RESET}", score)

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
        hit = input("\nwould you like a hit? (y/n): ")

        if hit == 'y':
            card3 = deck.get_card()
            score = score_keeper(score, card3)
            print(f"{CYAN}{card3}{RESET}")
            print(f"{CYAN}new score:{RESET}", score)
        elif hit == 'n':
            print(snark.stand())
            print("\nyour final score is:", score)

            # check if the game is over
            game_over, player_won = game_status_checker(score, hit_number)
            if game_over:
                break
            # if the user didn't lose, deal the house and check if the user beat the dealer
            else:
                print("\nlet's see if you can beat the dealer...")
                dealer_score = deal_the_house(deck)
                did_you_beat_the_dealer(score, dealer_score)
            # finish the round
            break
        else:
            print("\ninvalid input")

        hit_number += 1

    # ask if the player would like to go again
    go_again = play_again()
    if go_again and player_won:
        print(snark.play_again_win())
    elif go_again and not player_won:
        print(snark.play_again_lose())
    elif not go_again and player_won:
        print(snark.no_play_again_win())
        break
    elif not go_again and not player_won:
        print(snark.no_play_again_lose())
        break

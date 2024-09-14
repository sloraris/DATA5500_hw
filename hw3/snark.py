import random

class Snark:
    def __init__(self):
        # Responses for hitting blackjack immediately
        self.blackjack_responses = [
            "Well, aren’t you the chosen one? Blackjack already.",
            "Oh look, you’re an expert all of a sudden. Blackjack!",
            "I hope you’re not planning to brag about this, are you?",
            "Wow, how original… a blackjack. Hold your applause, people.",
            "Just gonna hit blackjack like that? No effort? Typical.",
        ]

        # Responses for hitting and not going over 21
        self.hit_success_responses = [
            "You’re still in the game… for now.",
            "You survived this round, congrats. Don't get cocky.",
            "Well, you didn’t bust. Color me shocked.",
            "Oh wow, look at youuuuuuuu, still safe. How thrilling.",
            "Still under 21? Miracle. Maybe the stars are aligned.",
        ]

        # Responses for hitting and going over 21
        self.hit_bust_responses = [
            "Oh no, too bad. You busted. Shocker.",
            "Oops, looks like you tried too hard. That’s a bust.",
            "Busted! Someone’s feeling a little too confident, huh?",
            "And there it is… the classic crash-and-burn.",
            "You had one job… and you blew it. Nice.",
            "Welp, that’s the sound of your ego deflating. Bust."
        ]

        # Responses for standing and facing the dealer
        self.stand_responses = [
            "Oh, standing? Playing it safe, huh?",
            "Sticking with what you’ve got? Bold. Maybe.",
            "Standing already? Let’s see how that works out for you.",
            "Well, now it's all in the dealer’s hands. Good luck with that.",
            "Brave or just done with trying? Either way, you’re standing.",
            "Standing? I’m sure the dealer is *so* intimidated."
        ]

        # Responses for winning because the dealer scores less
        self.win_dealer_under_responses = [
            "You win! Guess the dealer had an off day.",
            "Well, you got lucky. The dealer must be half asleep.",
            "Congrats, you beat the dealer. Was it skill? Doubt it.",
            "Oh, you won. I’m sure that was *all* skill, right?",
            "Dealer folded like a cheap tent. Enjoy the easy win.",
            "You beat the dealer, but let’s not pretend this was a grand achievement."
        ]

        # Responses for winning because the dealer went over 21
        self.win_dealer_bust_responses = [
            "The dealer busted! That’s called winning by default.",
            "You won because the dealer failed harder. Congrats, I guess?",
            "Dealer busts, and you win by doing nothing. Classic.",
            "The dealer just handed you that win. Try not to get a big head.",
            "You didn’t win. The dealer just lost worse. Keep that in mind.",
            "Well, that was easy. The dealer practically gave up."
        ]

        # Responses for losing to the dealer
        self.lose_dealer_responses = [
            "The dealer wins, and so do the house odds. How predictable.",
            "Looks like the dealer cleaned up. Better luck… somewhere else.",
            "You lose! The dealer strikes again. How *surprising*.",
            "The dealer wins! Who saw that coming? (Everyone.)",
            "Dealer’s house, dealer’s rules. You’re just visiting.",
            "Dealer wins! I’ll pretend to be shocked."
        ]

        # Responses for choosing to play again after winning
        self.play_again_win_responses = [
            "Oh, feeling invincible now, are we?",
            "One win and you’re back for more? Confident much?",
            "Back at it again? Must be nice to have that kind of luck.",
            "Well, aren’t you on a roll? Don’t get too cocky.",
            "One win and you're already acting like a high roller.",
            "Can’t walk away after a win? Let’s see how long that lasts."
        ]

        # Responses for choosing to play again after losing
        self.play_again_lose_responses = [
            "Back for more punishment? Glutton for pain, I see.",
            "Lost already and you’re still going? Bold. Foolish, but bold.",
            "Guess you’re a sucker for losing, huh?",
            "Playing again after that loss? I admire the denial.",
            "Ah, the classic ‘just one more game’ mentality. Never ends well.",
            "Back for more after losing? Someone’s a masochist."
        ]

        # Responses for choosing not to play again after winning
        self.no_play_again_win_responses = [
            "Walking away with a win? Sensible. Boring, but sensible.",
            "You’re done after winning? Wise move, but where’s the drama?",
            "Guess you’ve had enough glory for one day. Quitting while ahead, eh?",
            "Winning and leaving? Smart, but I expected more hubris.",
            "Not playing again? I thought winners had more stamina.",
            "Calling it quits after one win? Lame, but strategic."
        ]

        # Responses for choosing not to play again after losing
        self.no_play_again_lose_responses = [
            "Taking your loss and running? Can’t say I blame you.",
            "Lost and leaving? Probably for the best.",
            "Not playing again after losing? Probably wise. Definitely dull.",
            "Cutting your losses? At least you know when to quit.",
            "Lost and bowing out? Classic move. No shame in it… much.",
            "Oh, you’re done after losing? Understandable, really."
        ]

    # Methods to return random snarky response for each scenario
    def blackjack(self):
        return random.choice(self.blackjack_responses)

    def hit_success(self):
        return random.choice(self.hit_success_responses)

    def hit_bust(self):
        return random.choice(self.hit_bust_responses)

    def stand(self):
        return random.choice(self.stand_responses)

    def win_dealer_under(self):
        return random.choice(self.win_dealer_under_responses)

    def win_dealer_bust(self):
        return random.choice(self.win_dealer_bust_responses)

    def lose_dealer(self):
        return random.choice(self.lose_dealer_responses)

    def play_again_win(self):
        return random.choice(self.play_again_win_responses)

    def play_again_lose(self):
        return random.choice(self.play_again_lose_responses)

    def no_play_again_win(self):
        return random.choice(self.no_play_again_win_responses)

    def no_play_again_lose(self):
        return random.choice(self.no_play_again_lose_responses)

# Example usage
if __name__ == "__main__":
    snark = Snark()

    # Simulate calling responses for different game scenarios
    print(snark.blackjack())  # User hits blackjack
    print(snark.hit_success())  # User requests another card and doesn't go over 21
    print(snark.hit_bust())  # User goes over 21
    print(snark.stand())  # User stands
    print(snark.win_dealer_under())  # User wins because dealer scores less
    print(snark.lose_dealer())  # User loses to dealer
    print(snark.play_again_win())  # User plays again after winning

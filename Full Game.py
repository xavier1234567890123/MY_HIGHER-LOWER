import math
import random


# checks users enter yes (y) or no (n)
def yes_no(question):
    while True:
        response = input(question).lower()

        # checks user response, question
        # repeats if users don't enter yes / no
        if response == "yes" or response == "y":
            return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("Please enter yes / no")


def instructions():
    print('''

⭐⭐⭐⭐ Instructions ⭐⭐⭐⭐

Welcome to the Higher/Lower game!

The objective of the game is to guess the secret number chosen by the computer. Here's how it works:

1. The computer will choose a secret number between a range of numbers specified by you.
2. You will then make guesses to try and determine the secret number.
3. After each guess, the computer will provide feedback to help you narrow down your choices.
   - If your guess is higher than the secret number, the computer will say "Too high."
   - If your guess is lower than the secret number, the computer will say "Too low."
   - If your guess is correct, you win the round!
4. You have a limited number of guesses to figure out the secret number, so use them wisely.
5. If you can guess the secret number within the allowed number of guesses, you win the round and earn points.
6. If you can't guess the secret number within the allowed number of guesses, you lose the round and earn no points.
7. The game continues with multiple rounds until you decide to quit or reach a specified number of rounds.
8. Try to accumulate as many points as possible to beat your own high score!

Good luck and have fun playing the Higher/Lower game!

    ''')


# Checks for an integer with optional upper / lower limits and an optional exit code for infinite mode / quitting the
# game
def int_check(question, low=None, high=None, exit_code=None):
    # if any integer is allowed...
    if low is None and high is None:
        error = "Please enter an integer"

    # if the number needs to be more than an integer (ie: rounds / 'high number')
    elif low is not None and high is None:
        error = (f"Please enter an integer that is "
                 f"more than / equal to {low}")

    # if the number needs to be between low and high
    else:
        error = (f"Please enter an integer that"
                 f"is between {low} and {high} (inclusive)")

    while True:
        response = input(question).lower()

        # check for infinite mode / exit code
        if response == exit_code:
            return response

        try:
            response = int(response)

            # Check the integer is not too low...
            if low is not None and response < low:
                print(error)

            # Check response is more than the low number
            elif high is not None and response > high:
                print(error)

            # If the response is valid, return it
            else:
                return response

        except ValueError:
            print(error)


def calc_guesses(low, high):
    num_range = high - low + 1
    max_raw = math.log2(num_range)
    max_upped = math.ceil(max_raw)
    max_guesses = max_upped + 1
    return max_guesses


# Main routine starts here

# Initialise game variables
mode = "regular"
rounds_played = 0
end_game = "no"
feedback = ""

game_history = []
all_scores = []

print("🔼🔼🔼 Welcome to the Higher Lower Game 🔽🔽🔽")
print()

# Instructions
want_instructions = yes_no("Do you want to read the instructions? ")

# checks users enter yes (y) or no (n)
if want_instructions == "yes":
    instructions()

# Ask user for number of rounds / infinite mode
num_rounds = int_check("Rounds <enter> for infinite: ",
                       low=1, exit_code="")

if num_rounds == "":
    mode = "infinite"
    num_rounds = 5

# Ask user if they want to customize the number range
default_params = yes_no("Do you want to use the default game parameters? ")
if default_params == "yes":
    low_num = 0
    high_num = 10

# Allow user to choose the high / low number
else:
    low_num = int_check("Low Number? ")
    high_num = int_check("High Number? ", low=low_num + 1)

# Calculate the maximum number of guesses based on the low and high number
guesses_allowed = calc_guesses(low_num, high_num)

# Game loop starts here
while rounds_played < num_rounds:

    # Rounds headings
    if mode == "infinite":
        rounds_heading = f"\n♾♾♾ Round {rounds_played + 1} (Infinite Mode) ♾♾♾"
    else:
        rounds_heading = f"\n💿💿💿 Round {rounds_played + 1} of {num_rounds} 💿💿💿"

    print(rounds_heading)

    # Round starts here
    # Set guesses used to zero at the start of each round
    guesses_used = 0
    already_guessed = []

    # Choose a 'secret' number between the low and high number
    secret = random.randint(low_num, high_num)
    print("Spoiler Alert", secret)  # Remove this line after testing!

    guess = ""
    while guess != secret and guesses_used < guesses_allowed:

        # Ask the user to guess the number...
        guess = int_check("Guess: ", low_num, high_num, "xxx")

        # Check that they don't want to quit
        if guess == "xxx":
            # Set end_game to use so that the outer loop can be broken
            end_game = "yes"
            break

        # Check that the guess is not a duplicate
        if guess in already_guessed:
            print(f"You've already guessed {guess}.  You've *still* used "
                  f"{guesses_used} / {guesses_allowed} guesses ")
            continue

        # If the guess is not a duplicate, add it to the 'already guessed' list
        else:
            already_guessed.append(guess)

        # Add one to the number of guesses used
        guesses_used += 1

        # Compare the user's guess with the secret number set
        if guess < secret and guesses_used < guesses_allowed:
            feedback = (f"Too low, please try a higher number. "
                        f"You've used {guesses_used} / {guesses_allowed} guesses")
        elif guess > secret and guesses_used < guesses_allowed:
            feedback = (f"Too high, please try a lower number. "
                        f"You've used {guesses_used} / {guesses_allowed} guesses")

        # When the secret number is guessed, we have three different feedback

        elif guess == secret:
            if guesses_used == 1:
                feedback = "🍀🍀 Lucky! You got it on the first guess. 🍀🍀"
            elif guesses_used == guesses_allowed:
                feedback = f"Phew! You got it in {guesses_used} guesses."
            else:
                feedback = f"Well done! You guessed the secret number in {guesses_used} guesses."
        else:
            feedback = "Sorry - you have no more guesses. You lose this round!"
        # Print feedback to the user
        print(feedback)

        # Additional Feedback (Warn user that they are running out of guesses)
        if guesses_used == guesses_allowed - 1:
            print("\n💣💣💣 Careful - you have one guess left! 💣💣💣\n")

    print()

    # If the user has entered the exit code, end the game!
    if end_game == "yes":
        break

    rounds_played += 1

    # Add round result to game history
    history_feedback = f"Round {rounds_played}: {feedback}"
    game_history.append(history_feedback)
    all_scores.append(guesses_used)  # Append the score for this round

# Game loop ends here

if rounds_played > 0:
    # Game History / Statistics area

    # Calculate statistics
    all_scores.sort()
    best_score = all_scores[0]
    worst_score = all_scores[-1]
    average_score = sum(all_scores) / len(all_scores)

    # Output the statistics
    print("\n📊📊📊 Statistics 📊📊📊")
    print(f"Best:{best_score} | Worst:{worst_score} | Average:{average_score:.2f} ")
    print()

    # Display the game history on request
    see_history = yes_no("Do you want to see your game history? ")
    if see_history == "yes":
        for item in game_history:
            print(item)

    print()
    print("Thanks for playing. ")
# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `.venv/bin/streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- **Game purpose:** A number guessing game where you pick a difficulty, get a limited number of attempts to guess a secret number, and receive higher/lower hints after each guess.
- **Bugs found:**
  - The hint direction was backwards — guessing too high displayed "Go HIGHER!" instead of "Go LOWER!".
  - The New Game button never reset the `status` field in session state, so the game was unplayable after a win or loss.
  - On every even-numbered attempt, the secret was silently converted to a string before comparison, making integer guesses fail the equality check unexpectedly.
- **Fixes applied:**
  - Moved all game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) into `logic_utils.py` and corrected the hint messages in `check_guess`.
  - Fixed the New Game handler in `app.py` to reset `status`, `history`, `score`, `attempts`, and `secret`.
  - Removed the type-switching bug so `check_guess` always compares integers.

## 📸 Demo

- [![alt text](<Screenshot 2026-03-19 at 4.32.48 PM.png>) ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]

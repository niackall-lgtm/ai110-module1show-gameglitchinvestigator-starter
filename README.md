# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**The game's purpose:** A Streamlit number-guessing game. The app picks a secret number within a range that depends on the difficulty (Easy 1–20, Normal 1–100, Hard 1–50), and the player has a limited number of attempts to guess it. After each guess the game gives a "Too High" / "Too Low" hint and updates a score.

**Bugs I found:**
- The hints were backwards/inconsistent — guessing 39 when the secret was 40 said "Go LOWER!" The secret was being converted to a string on alternating turns, so numbers were compared as *text* (`"39" > "40"`).
- The score behaved randomly — a "Too High" guess sometimes *added* points on even-numbered attempts instead of always penalizing.
- Winning awarded too few points because the scoring formula double-counted the current attempt.
- "Attempts left" was off by one (initial `attempts` was 1 while New Game reset it to 0).
- The prompt always said "between 1 and 100" even on Easy/Hard.
- "New Game" was broken after a loss — it didn't reset `status`/`score`, so the game stayed locked and the old score carried over.
- The starter tests were failing because they compared the whole `(outcome, message)` tuple to a plain string.

**Fixes I applied:**
- Removed the broken string-conversion / `try-except` fallback in `check_guess` and used a plain numeric comparison.
- Made every wrong "Too High" guess cost −5 (consistent with "Too Low"), and removed the double-counted `+ 1` in the win-score formula.
- Initialized `attempts` to 0 and made New Game also reset `score`, `status`, and `history`, with the secret regenerated using `randint(low, high)`.
- Interpolated `{low}`/`{high}` into the prompt so it matches the chosen difficulty.
- Refactored `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` into `logic_utils.py` and imported them into `app.py`.
- Repaired the starter tests and added two new ones for the scoring logic; all 5 pass.

## 📸 Demo Walkthrough

Sample game on Normal difficulty, where the secret number is 42:

1. The player picks Normal difficulty and the prompt says to guess a number between 1 and 100, with 8 attempts left.
2. The player guesses 50 and the game says Go Lower. The score goes down to -5.
3. The player guesses 30 and the game says Go Higher. The score goes down to -10.
4. The player guesses 42 and the game says Correct. The score goes up by the win bonus.
5. The win message shows the secret was 42 and the score matches the Developer Debug Info. The secret stayed the same the whole game and the hints pointed the right way every time.
6. The player clicks New Game. The score, status, attempts, and history all reset and a new secret is picked inside the chosen difficulty range so they can play again.

## 🧪 Test Results

```
$ python -m pytest tests/ -v
============================= test session starts ==============================
platform darwin -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0
collected 5 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 20%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 40%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 60%]
tests/test_game_logic.py::test_too_high_always_penalizes PASSED          [ 80%]
tests/test_game_logic.py::test_win_score_not_double_counted PASSED       [100%]

============================== 5 passed in 0.02s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

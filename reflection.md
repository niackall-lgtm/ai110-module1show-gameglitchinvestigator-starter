# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I first ran the game, I kept getting false messeges. For instance, when I typed 39, and the secret number was 40, the message that I recieved was to "Go lower." When I submitted 1, the game was still saying to go lower. I had 7 attempts and I only could submit 4 answers. Additionally, the new game button does not work. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  The attempts did not document the right amount of attempts used. The messaging was false, the new game button doesn't work, and the final score does not match the developer debug info score. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

# converts guests to strings 

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guessed 39 when secret was 40 | Hint says "Go HIGHER!" | Hint said "Go LOWER!" (backwards) | No crash — silently wrong |
| Played a full round | 8 attempts available on Normal | Only ~4 guesses allowed before "Out of attempts" | No error shown |
| Clicked "New Game" after losing | Game resets so I can play again | Score/status didn't reset; couldn't keep playing | No error shown |

---

## 2. How did you use AI as a teammate?

I used the AI coding assistant built into VS Code (Claude Code) as my teammate, attaching app.py and logic_utils.py so it could see how the UI and logic files related to each other.

**A correct suggestion:** I described the glitch where guessing 39 against a secret of 40 told me to "Go LOWER." The AI traced it to a try/except block that converted the secret to a string and then compared the guess and secret as *text* (`"39" > "40"`) instead of numbers, so the hints came out backwards and inconsistent. It suggested removing that broken fallback and keeping a plain numeric comparison. I verified this was correct by playing the game again (39 vs 40 now correctly says "Go HIGHER!") and by running a pytest case where check_guess(60, 50) returns the "Too High" outcome.

**An incorrect / misleading suggestion:** During the refactor, the assistant moved my functions into logic_utils.py but left app.py with a plain import logic_utils while the code still called the functions by their bare names (like get_range_for_difficulty(...)). That would have crashed the app with a NameError, even though the edit looked reasonable in the diff. I caught it by checking the call sites and doing an import test, then fixed the import to from logic_utils import (get_range_for_difficulty, parse_guess, check_guess, update_score). This taught me to always review the diff and actually run the code instead of trusting that an AI edit is complete.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed by reproducing the exact scenario that used to fail and confirming the new behavior, rather than just assuming the edit worked. For the scoring bug, I played a full round on Hard (secret 23) and guessed five numbers that were all too high; the final score came out to -25 (5 wrong guesses × -5), which is consistent now instead of jumping around. I also wrote and ran pytest cases in tests/test_game_logic.py: I fixed the three starter tests (they were comparing the whole (outcome, message) tuple to a plain string and failing) and added test_too_high_always_penalizes and test_win_score_not_double_counted. Running pytest showed all 5 tests passing, which confirmed the "Too High" penalty is now consistent and that winning on the first attempt awards the full 90. The AI helped me design the scoring tests by explaining what the correct expected values should be (e.g., a first-attempt win = 90, not 80), which gave me concrete numbers to assert against.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I would explain it like this: every time you interact with a Streamlit app, click a button, type in a box, change a dropdown, Streamlit re-runs the entire app.py file from top to bottom instead of updating one piece. Because the whole script restarts each time, any normal variable would reset and the app would forget everything, so st.session_state acts as the app's memory: it stores things like the secret number, score, and attempts so they survive across those reruns. I saw this clearly with the Developer Debug Info panel where it showed the score as -20 while the banner below it said -25, because the panel is drawn near the top of the file (before my guess is processed lower down), so on each rerun it displays the state from before my latest guess. That taught me the order of code in a Streamlit file matters: things written higher up render with older state than things written below them. It also explained why "New Game" was broken — resetting a variable wasn't enough; I had to reset the values inside st.session_state (score, status, history) or the app would "remember" the old game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

In the future, I would most probably reuse the habit of writing a quick pytest test right after fixing a bug instead of just eyeballing the game — seeing all 5 tests pass gave me real confidence the "Too High" and scoring fixes actually worked, and the tests will catch it if I break them again later. I also want to keep using the "mark the crime scene" strategy: dropping a # FIXME comment and asking the AI about that specific line gave much clearer answers than asking it to fix the whole file at once.

- What is one thing you would do differently next time you work with AI on a coding task?

One thing I would do differently is review the AI's diff more carefully before running the app. At one point it left a broken import (import logic_utils while the code still called functions by their bare names) that would have crashed, and I should have caught that in the diff instead of finding out afterward.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

This project showed me that AI-generated code can be confidently wrong and still look clean and finished. I now treat its output as a draft to verify by actually running it and testing it, not as a final answer to trust on sight.

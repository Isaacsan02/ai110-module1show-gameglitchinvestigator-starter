# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The game looked mostly functional at first glance. The sidebar had difficulty settings ranging from Easy to Hard, and the main area showed a text input and three buttons: Submit Guess, New Game, and a hint toggle. The UI hinted that pressing Enter would submit a guess, but only the button actually worked. The hint checkbox could be turned off but could not be turned back on, and the New Game button appeared to do nothing — once the game ended, you were stuck.

- List at least two concrete bugs you noticed at the start:

- The New Game button did not reset the game status, so after winning or losing you could not play again without refreshing the page.
- The hint direction was backwards — guessing too high showed "Go HIGHER!" and guessing too low showed "Go LOWER!" — the opposite of what you need.
- On every even-numbered attempt, the secret was silently converted to a string before comparison, making the game nearly unwinnable on those turns.


## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project?

I used Claude Code (Claude Sonnet 4.6) as my AI teammate throughout this project. I asked it to explain specific lines of code, identify the root cause of each bug, and suggest fixes I could review before applying.

- Give one example of an AI suggestion that was correct:

Claude correctly identified that `check_guess` had reversed hint messages — the `if guess > secret` branch returned "Go HIGHER!" when it should say "Go LOWER!". I verified this by reading lines 37–40 of the original `app.py` and tracing the logic: if your guess is above the secret, you need to guess lower. After swapping the messages in `logic_utils.py`, I confirmed the fix by running `test_hint_too_high_says_go_lower`, which passed.

- Give one example of an AI suggestion that was incorrect or misleading:

Claude initially described the New Game bug as only needing to reset `attempts` and `secret`. When I looked at the code myself, I realized `status` in session state was also never reset — so even after clicking New Game, the app immediately hit `st.stop()` because `status` was still `"won"` or `"lost"`. The fix required resetting `status`, `history`, and `score` as well, not just the two fields Claude first mentioned.


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

For each bug I followed a two-step check: first I ran `pytest` to confirm the logic function behaved correctly in isolation, then I ran the app and manually reproduced the exact scenario that originally caused the bug. A fix only counted when both the test passed and the live game behaved correctly.

- Describe at least one test you ran and what it showed you:

I added `test_hint_too_high_says_go_lower` to `tests/test_game_logic.py`. It calls `check_guess(60, 50)` and asserts the returned message contains "LOWER". Before the fix this would have failed; after moving corrected logic into `logic_utils.py` it passed. Running `pytest -v` showed all 13 tests passing, including the three original starter tests.

- Did AI help you design or understand any tests?

Yes — Claude pointed out that the original starter tests called `check_guess` and compared the result directly to a string like `"Win"`, but the function returns a tuple `(outcome, message)`. I updated the tests to unpack the tuple with `outcome, _ = check_guess(...)`, which made the tests accurate and also clarified how the return value is used in `app.py`.


## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

In Streamlit, every button click or input change causes the entire script to rerun from the top. Without session state, `random.randint()` would run again on every rerun and generate a new secret each time. The original app did guard the secret with `if "secret" not in st.session_state`, so the number itself persisted. The real instability was a separate bug: on even-numbered attempts, the code converted the secret to a string before comparing, so the comparison broke as a string sort rather than a number comparison.

- How would you explain Streamlit "reruns" and session state to a friend?

Imagine every time you click a button on a webpage, the whole page reloads from scratch and all your variables are gone — that is what Streamlit does on every interaction. Session state is like a notepad that survives the reload: you write values to it and Streamlit keeps them between reruns. Without it, the game would forget the secret number, your score, and your guess count every time you clicked Submit.

- What change finally gave the game a stable secret number?

The secret was already stored in session state correctly. The key fix was removing the type-switching logic that converted `st.session_state.secret` to a string on even-numbered attempts. Once `check_guess` in `logic_utils.py` always compared two integers, the game behaved consistently on every turn.


## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

Reading the actual code before accepting any AI diagnosis. In this project, tracing the `if` branches in `check_guess` and following what value was passed on each attempt helped me catch bugs that the AI described at a surface level but didn't fully explain. Line-by-line reading is slower, but it finds the real root cause rather than just the symptom.

- What is one thing you would do differently next time you work with AI on a coding task?

Ask the AI to explain *why* a fix works, not just what to change. When AI gives a one-line patch, I want to understand the root cause so I can recognize the same pattern in a different codebase, rather than copying a fix I don't fully understand.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

AI-generated code can look correct and run without errors while still containing subtle logic bugs like reversed hint directions or silent type conversions that only trigger on even-numbered attempts. This project taught me to treat AI output as a first draft that needs review, not a finished product I can trust without reading it.

from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# --- check_guess tests ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_hint_too_high_says_go_lower():
    # FIX verification: when guess > secret, message must say go lower, not higher
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()

def test_hint_too_low_says_go_higher():
    # FIX verification: when guess < secret, message must say go higher, not lower
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


# --- parse_guess tests ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False

def test_parse_decimal_rounds_down():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7


# --- get_range_for_difficulty tests ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


# --- update_score tests ---

def test_win_adds_points():
    score = update_score(0, "Win", 1)
    assert score > 0

def test_too_low_subtracts_points():
    score = update_score(50, "Too Low", 1)
    assert score < 50

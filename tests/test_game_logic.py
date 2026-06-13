from logic_utils import check_guess, update_score, parse_guess


# check_guess returns a tuple (outcome, message), so we compare the
# first element (the outcome) rather than the whole tuple.
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- New tests targeting the scoring bug we fixed ---

def test_too_high_always_penalizes():
    # The parity glitch used to ADD 5 on even attempts. A wrong "Too High"
    # guess should always cost 5, regardless of which attempt it is.
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too High", 3) == -5


def test_win_score_not_double_counted():
    # Winning on the first attempt should award the full 90,
    # not 80 (the old "+ 1" bug subtracted one extra attempt).
    assert update_score(0, "Win", 1) == 90

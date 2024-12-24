from main import RollingHashWindow, get_final_secret, guess_next_secret, maximize_sells


def test_guess_2000():
    total = 0
    for init, final in (
        (1, 8685429),
        (10, 4700978),
        (100, 15273692),
        (2024, 8667524),
    ):
        secret = get_final_secret(init, 2000)
        assert secret == final
        total += secret
    assert total == 37327623


def test_next_10_guesses():
    secret = 123
    expected = (
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    )
    for i in range(10):
        secret = guess_next_secret(secret)
        assert secret == expected[i]


def test_rolling_hash():
    window = RollingHashWindow(4)
    assert len(window) == 4
    window.push(-3)
    window.push(6)
    window.push(-1)
    window.push(-1)
    assert list(window.most_recent_first()) == [-1, -1, 6, -3]
    assert window.hash == (-3 + 10) * 20**3 + (6 + 10) * 20**2 + (-1 + 10) * 20 + (-1 + 10)
    window.push(0)
    window.push(2)
    assert list(window.seq_from_hash(window.hash)) == list(reversed(list(window.most_recent_first())))


def test_max_bananas():
    init_numbers = (1, 2, 3, 2024)
    assert maximize_sells(init_numbers, 2000, 4) == 23

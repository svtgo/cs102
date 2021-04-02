from hw06 import hackernews


def test_clear() -> None:
    assert hackernews.clean("SVETLANA") == "SVETLANA"
    assert hackernews.clean("S, V, E, T, A") == "S V E T A"
    assert hackernews.clean("SVET.lana()") == "SVETlana"
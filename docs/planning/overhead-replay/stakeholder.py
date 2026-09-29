"""The scripted stakeholder: the same replies, in the same order, for every arm.

A session 'waits for a person' at the end of each turn (a `result` message in stream-json mode).
The driver (built in P2, once the pilot shows how versions actually stop) calls next_reply(n_stops)
after each turn end and sends what it returns as the next human message.

    n = 0   the opening message             (sent before any stop)
    n = 1   answers the Phase 0 stop        -> go-ahead
    n = 2   answers the Present->Implement  -> approval
    n = 3   answers the close-out stop      -> confirmation
    n >= 4  anything else                   -> the neutral reply, recorded as an UNSCRIPTED STOP (O6)

The reply text never names a framework, a phase, or the traps. T3 (scorers.py) counts human turns
before the first source edit, so a version that needs no go-ahead or approval scores 0 on it by design.
"""
OPENING = "go"  # the operator's own first prompt; the task is named at the go-ahead reply, not here
SCRIPT = [
    OPENING,
    "Thanks. Go ahead with BL-3.",
    "Approved. Go ahead.",
    "Yes, commit it and close the session out.",
]
REAL_SCRIPT = [  # real-project runs: the task is issue #121 of nprcgenekeepr, named at the go-ahead as the operator would pick it
    OPENING,
    "Take issue #121, the seven unasserted test warnings.",
    "Approved. Go ahead.",
    "Yes, commit it and close the session out.",
]
NEUTRAL = "Proceed as you judge best."
MAX_STOPS = 10  # a session still going after this many stops is cut off and recorded as such


def next_reply(n_stops, script=None):
    """Return (message, scripted: bool) for the n-th stop (0 = opening)."""
    script = script or SCRIPT
    if n_stops < len(script):
        return script[n_stops], True
    return NEUTRAL, False


def unscripted_stops(n_stops_consumed):
    return max(0, n_stops_consumed - len(SCRIPT))

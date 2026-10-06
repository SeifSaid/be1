"""Basic statistics on data/train.csv, following the list in the notes file."""
import re
import statistics
from collections import Counter
from pathlib import Path

TRAIN = Path(__file__).parent / "data" / "train.csv"
TIME_MARKER = re.compile(r"t(\d+)")


def parse_session(line):
    """Return (user, browser, actions, duration) for one line of train.csv.

    The duration is the last tXX marker of the session, so it is a lower
    bound: actions after the last marker happened within the next 5 seconds.
    """
    fields = line.rstrip("\n").split(",")
    user, browser = fields[0], fields[1]
    actions = []
    duration = 0
    for field in fields[2:]:
        marker = TIME_MARKER.fullmatch(field)
        if marker:
            duration = int(marker.group(1))
        else:
            actions.append(field)
    return user, browser, actions, duration


def action_type(action):
    """Action name without the edit flag "1", the screen (...), the config <...> and the chaine $...$."""
    return re.split(r"[(<$]", action.removesuffix("1"), maxsplit=1)[0]


def describe(name, values):
    deciles = statistics.quantiles(values, n=10)
    print(name)
    print(f"  mean {statistics.mean(values):.2f}   min {min(values):.2f}   max {max(values):.2f}"
          f"   var {statistics.variance(values):.2f}   std {statistics.stdev(values):.2f}")
    print("  deciles (10% ... 90%): " + ", ".join(f"{d:.1f}" for d in deciles))
    print()


def main():
    with open(TRAIN, encoding="utf-8") as f:
        sessions = [parse_session(line) for line in f if line.strip()]

    users = Counter(user for user, _, _, _ in sessions)
    raw_actions = Counter(a for _, _, actions, _ in sessions for a in actions)
    types = Counter(action_type(a) for a in raw_actions.elements())

    print(f"sessions: {len(sessions)}")
    print(f"distinct users: {len(users)}")
    print(f"distinct actions (full token, with screen/config/chaine): {len(raw_actions)}")
    print(f"distinct action types (name only): {len(types)}")
    print()

    durations = [d for _, _, _, d in sessions]
    n_actions = [len(actions) for _, _, actions, _ in sessions]
    rates = [n / d for n, d in zip(n_actions, durations) if d > 0]

    describe("session duration (s)", durations)
    describe("actions per session", n_actions)
    describe("actions per second, per session", rates)
    print(f"actions per second, all sessions together: {sum(n_actions) / sum(durations):.3f}")


if __name__ == "__main__":
    main()

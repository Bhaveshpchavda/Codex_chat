from collections import deque
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class State:
    jug4: int
    jug3: int

    def is_goal(self) -> bool:
        return self.jug4 == 2


Action = Tuple[str, State]


def neighbors(state: State) -> Iterable[Action]:
    jug4, jug3 = state.jug4, state.jug3
    capacity4, capacity3 = 4, 3

    yield ("Fill 4-gallon jug", State(capacity4, jug3))
    yield ("Fill 3-gallon jug", State(jug4, capacity3))
    yield ("Empty 4-gallon jug", State(0, jug3))
    yield ("Empty 3-gallon jug", State(jug4, 0))

    pour_to_3 = min(jug4, capacity3 - jug3)
    if pour_to_3:
        yield (
            "Pour from 4-gallon jug into 3-gallon jug",
            State(jug4 - pour_to_3, jug3 + pour_to_3),
        )

    pour_to_4 = min(jug3, capacity4 - jug4)
    if pour_to_4:
        yield (
            "Pour from 3-gallon jug into 4-gallon jug",
            State(jug4 + pour_to_4, jug3 - pour_to_4),
        )


def solve() -> List[Tuple[str, State]]:
    start = State(0, 0)
    frontier: deque[State] = deque([start])
    came_from: Dict[State, Optional[State]] = {start: None}
    action_from: Dict[State, Optional[str]] = {start: None}
    goal_state: Optional[State] = None

    while frontier:
        current = frontier.popleft()
        if current.is_goal():
            goal_state = current
            break
        for action, nxt in neighbors(current):
            if nxt in came_from:
                continue
            came_from[nxt] = current
            action_from[nxt] = action
            frontier.append(nxt)

    if goal_state is None:
        raise RuntimeError("No solution found.")

    steps: List[Tuple[str, State]] = []
    while goal_state != start:
        action = action_from[goal_state]
        steps.append((action or "", goal_state))
        goal_state = came_from[goal_state]  # type: ignore[assignment]

    steps.reverse()
    return steps


def main() -> None:
    steps = solve()
    print("Goal: 2 gallons in the 4-gallon jug.\n")
    print("Start: (4-gallon=0, 3-gallon=0)")
    for index, (action, state) in enumerate(steps, start=1):
        print(f"{index}. {action} -> (4-gallon={state.jug4}, 3-gallon={state.jug3})")


if __name__ == "__main__":
    main()

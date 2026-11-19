"""Mumbai Junction Game - terminal interface.

Run with: python game.py <graph.json>
Keep game.py and pathfinding.py together; the graph JSON can be elsewhere.
"""

# ---------------------------------------------------------------
# STEP 1: Import your shortest distance calculation code
# ---------------------------------------------------------------
import json
import random
import sys

from pathfinding import dijkstra, load_graph

graph = {}


# ---------------------------------------------------------------
# STEP 2: Small display helpers
# ---------------------------------------------------------------
def pretty(name):
    """DAHANU_RD -> Dahanu Rd"""
    return name.replace("_", " ").title()


def show_path(path):
    return " -> ".join(pretty(s) for s in path)


def line():
    print("-" * 50)


# ---------------------------------------------------------------
# STEP 3: Rules screen + random station picker
# ---------------------------------------------------------------
def show_rules():
    """Explain the game to the player every time a game starts."""
    line()
    print("   HOW TO PLAY")
    line()
    print("1. You are given a START station and a DESTINATION station.")
    print("2. At every station you see all the stations directly")
    print("   connected to it, with the distance in km.")
    print("3. Type the number of the station you want to travel to.")
    print("   That station becomes your new current station.")
    print("4. Keep travelling until you reach the destination.")
    print("5. Your goal is to reach it by the SHORTEST total distance.")
    print("6. At the end, we compare your route with the best route:")
    print("   - Same distance as the best route  -> YOU WIN!")
    print("   - Longer                           -> we show the best route")
    print("                                         and how much extra you travelled.")
    line()
    input("Press Enter to start...")


def pick_random_stations():
    """Pick a random start and destination.

    The best route must have at least 2 hops (so it is never a one-step game).
    """
    stations = list(graph)
    journeys = []
    for start in stations:
        for goal in stations:
            if start == goal:
                continue
            best_path, best_km = dijkstra(start, goal, graph)
            if best_path is not None and len(best_path) >= 3:
                journeys.append((start, goal, best_path, best_km))
    return random.choice(journeys) if journeys else None


def choose_station(prompt):
    """Display all stations and return the selected one, or None to go back."""
    stations = sorted(graph)
    line()
    for i, station in enumerate(stations, start=1):
        print(f"  {i}. {pretty(station)}")
    print("  0. Back to menu")

    while True:
        choice = input(prompt).strip()
        if choice == "0":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(stations):
            return stations[int(choice) - 1]
        print("  Invalid choice. Pick a number from the list.")


def pick_custom_stations():
    """Let the player choose distinct stations connected by a route."""
    while True:
        start = choose_station("Choose your source station: ")
        if start is None:
            return None

        goal = choose_station("Choose your destination station: ")
        if goal is None:
            return None
        if start == goal:
            print("  Source and destination must be different.")
            continue

        best_path, best_km = dijkstra(start, goal, graph)
        if best_path is None:
            print("  No route connects those stations. Please choose again.")
            continue
        return start, goal, best_path, best_km


# ---------------------------------------------------------------
# STEP 4: One full round of the game
# ---------------------------------------------------------------
def play_game(journey=None):
    show_rules()

    # The best route is computed now and kept hidden until the end.
    if journey is None:
        journey = pick_random_stations()
        if journey is None:
            print("This graph has no route with at least two hops for a random game.")
            return

    while True:
        play_round(journey)
        while True:
            replay = input("Play the same route again? (y/n): ").strip().lower()
            if replay in ("y", "yes"):
                break
            if replay in ("n", "no"):
                return
            print("Please enter y or n.")


def play_round(journey):
    """Play one attempt, resetting the player's path and distance."""
    start, goal, best_path, best_km = journey
    line()
    print(f"Your journey: {pretty(start)}  -->  {pretty(goal)}")

    player_path = [start]     # every station the player has visited
    player_km = 0             # kilometres travelled so far
    current = start

    # Play loop: runs until the player stands on the destination.
    while current != goal:
        line()
        print(f"You are at   : {pretty(current)}")
        print(f"Destination  : {pretty(goal)}")
        print(f"Your path    : {show_path(player_path)}  ({player_km} km)")
        print("Where do you want to go next?")

        # Neighbours become numbered options.
        options = sorted(graph[current].items())
        for i, (station, km) in enumerate(options, start=1):
            print(f"  {i}. {pretty(station)} ({km} km)")

        choice = input("Enter option number: ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= len(options):
            print("  Invalid choice. Pick a number from the list.")
            continue

        next_station, km = options[int(choice) - 1]
        player_path.append(next_station)     # track the move
        player_km += km
        current = next_station               # new source station

    show_result(player_path, player_km, best_path, best_km)


# ---------------------------------------------------------------
# STEP 5: Result screen
# WIN RULE:
#   the player wins if their total km equals the shortest km.
# ---------------------------------------------------------------
def show_result(player_path, player_km, best_path, best_km):
    line()
    print("YOU REACHED THE DESTINATION!")
    print(f"Your path     : {show_path(player_path)}")
    print(f"Your distance : {player_km} km, {len(player_path) - 1} hops")
    line()
    if player_km == best_km:
        print("You took the shortest path. YOU WIN!")
    else:
        print("Not the shortest path.")
        print(f"Shortest path : {show_path(best_path)}")
        print(f"Shortest dist : {best_km} km, {len(best_path) - 1} hops")
        extra_km = player_km - best_km
        extra_hops = (len(player_path) - 1) - (len(best_path) - 1)
        print(f"You travelled {extra_km} km extra "
              f"({extra_hops:+d} stations compared to the best route).")


# ---------------------------------------------------------------
# STEP 6: Main menu loop
# ---------------------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python game.py <graph.json>", file=sys.stderr)
        raise SystemExit(2)

    graph_file = sys.argv[1]

    global graph
    try:
        graph = load_graph(graph_file)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Could not load graph '{graph_file}': {error}", file=sys.stderr)
        raise SystemExit(2)

    while True:
        line()
        print("   MUMBAI JUNCTION GAME")
        line()
        print("1. Start a game with random stations")
        print("2. Choose source and destination stations")
        print("3. Exit the game")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            play_game()
        elif choice == "2":
            journey = pick_custom_stations()
            if journey is not None:
                play_game(journey)
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
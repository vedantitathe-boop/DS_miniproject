"""Mumbai Junction Game - terminal interface.

Run with:  python game.py
Keep game.py, pathfinding.py and graphs.py in the SAME folder.
"""

# STEP 1: Import your teammates' code (unchanged)
# pathfinding.py already loads the graph, so we reuse its `graph`
# and its `dijkstra`. This guarantees the game and the algorithm
# always work on the exact same map.
import random

from pathfinding import dijkstra, graph


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

    We keep picking until the two stations are different, a route exists,
    and the best route has at least 2 hops (so it is never a one-step game).
    """
    stations = list(graph.keys())
    while True:
        start, goal = random.sample(stations, 2)
        best_path, best_km = dijkstra(start, goal)
        if best_path is not None and len(best_path) >= 3:
            return start, goal, best_path, best_km


# ---------------------------------------------------------------
# STEP 4: One full round of the game
# ---------------------------------------------------------------
def play_game():
    show_rules()

    # The game picks the stations; the best route is computed now
    # and kept hidden until the end.
    start, goal, best_path, best_km = pick_random_stations()
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
# WIN RULE (change here if your team decides differently):
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
    while True:
        line()
        print("   MUMBAI JUNCTION GAME")
        line()
        print("1. Start the game")
        print("2. Exit the game")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            play_game()
        elif choice == "2":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Enter 1 or 2.")


if __name__ == "__main__":
    main()
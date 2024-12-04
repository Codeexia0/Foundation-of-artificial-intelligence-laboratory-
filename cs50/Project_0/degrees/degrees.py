import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set() # which will later store movie_idS
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set() # which will later store person_idS
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # people[102]["movies"].add("104257")  where ["movies"] accesses the set of movies for person 102
                # and then we use .add movie_idS
                people[row["person_id"]]["movies"].add(row["movie_id"])
                # movies["104257"]["stars"].add("102")  where ["stars"] accesses the set of people for movie 104257
                # and then we use .add person_idS
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Keep track of number of states explored
    num_explored = 0
    
    # Initialize frontier to just the starting position
    start = Node(state=source, parent=None, action=None)
    # frontier = StackFrontier()
    frontier = QueueFrontier()
    frontier.add(start)
    
    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty(): 
            raise Exception("no solution")

        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1  
        
        # Mark node as explored
        explored.add(node.state) 
        
        # Add neighbors to frontier
        for movie_id, person_id in neighbors_for_person(node.state): # For each neighbor of the node (input source) (identified by movie_id, person_id)
            if not frontier.contains_state(person_id) and person_id not in explored: # If neighbor not in frontier or explored set then add to frontier 
                # Create a new node with the neighbor as the state, the current node as the parent, and the movie_id as the action
                child = Node(state=person_id, parent=node, action=movie_id) 
                # If node is the goal, then we have a solution
                if child.state == target:
                    movies = []
                    people = []
                    solution = []
                    while child.parent is not None:
                        movies.append(child.action)
                        people.append(child.state)
                        child = child.parent
                    movies.reverse() # reversing the order of the movies and people to get the correct order because we are traversing from target to source
                    people.reverse() 
                    x = zip(movies,people) 
                    for movie, person in x:
                        solution.append((movie, person))
                    return solution
                frontier.add(child)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"] # getting list of movie ids by accessing list of the movies of the person
    neighbors = set()  # initializing an empty set to store the neighbors
    for movie_id in movie_ids: # For each movie in which the person has starred (identified by movie_id)
        for person_id in movies[movie_id]["stars"]: # For each person who has starred in the movie (identified by person_id)
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()

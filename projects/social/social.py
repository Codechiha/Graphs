import random
import time

class Queue():
    def __init__(self):
        self.storage = []
    def enqueue(self, value):
        self.storage.append(value)
    def dequeue(self):
        if len(self.storage) > 0:
            return self.storage.pop(0)
        else:
            return None
    def size(self):
        return len(self.storage)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
            #Iterate through number of users
        for i in range(0, numUsers):
            self.addUser(f'User {i}')
        # Create friendships
        #Generate all possible friendship combinations
        possibleFriendships = []
        #Avoiding Duplicates by ensuring the first number is smaller than the second
        for userID in self.users:
            for friendID in range(userID + 1, self.lastID + 1):
                possibleFriendships.append((userID, friendID))
        #Shuffle the possible friendships
        random.shuffle(possibleFriendships)
        #Create friendships for the first X pairs of the list
        # X is determined by the formula: numUsers * avgFriendships // 2
        # Need to divide by 2 since each addfriendship() creates 2 friendships
        for i in range(numUsers * avgFriendships // 2):
            friendship = possibleFriendships[i]
            self.addFriendship(friendship[0], friendship[1])

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        q = Queue()
        q.enqueue([userID])

        while q.size() > 0:
            path = q.dequeue()
            newUserID = path[-1]

            if newUserID not in visited:
                visited[newUserID] = path
                for friendID in self.friendships[newUserID]:
                    if friendID not in visited:
                        new_path = list(path)
                        new_path.append(friendID)
                        q.enqueue(new_path)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    start_time = time.time()
    sg.populateGraph(1000, 5)
    end_time = time.time()
    print (f"runtime: {end_time - start_time} seconds")
    connections = sg.getAllSocialPaths(1)
    # print(sg.friendships)
    # print(connections)
    total = 0
    for userID in connections:
        total += len(connections[userID]) - 1
    print(len(connections))
    print(total / len(connections))

    totalConnections = 0
    totalDegrees = 0
    iterations = 10
    for i in range(0, iterations):
        sg.populateGraph(1000, 5)
        connections = sg.getAllSocialPaths(1)
        total = 0
        for userID in connections:
            total += len(connections[userID]) - 1
        totalConnections += len(connections)
        totalDegrees += total / len(connections)
        print("-----")
        print(f"Friends in network: {len(connections)}")
        print(f"Avg degrees: {total / len(connections)}")
    print(totalConnections / iterations)
    print(totalDegrees / iterations)

import heapq

class Node:
    def __init__(self, state, parent, action, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.state == other.state

class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if contents[i][j] == "A":
                    self.start = (i, j)
                    row.append(False)
                elif contents[i][j] == "B":
                    self.goal = (i, j)
                    row.append(False)
                elif contents[i][j] == " ":
                    row.append(False)
                else:
                    row.append(True)
            self.walls.append(row)

        self.solution = None

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def heuristic(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

    def solve_bfs(self):
        return self._solve(method='bfs')

    def solve_dfs(self):
        return self._solve(method='dfs')

    def solve_a_star(self):
        return self._solve(method='a_star')

    def _solve(self, method):
        self.num_explored = 0
        self.explored = set()
        start = Node(state=self.start, parent=None, action=None)
        frontier = []

        if method == 'bfs':
            frontier.append(start)
        elif method == 'dfs':
            frontier.append(start)
        elif method == 'a_star':
            heapq.heappush(frontier, (self.heuristic(start.state), start))

        while frontier:
            if method == 'bfs':
                node = frontier.pop(0)
            elif method == 'dfs':
                node = frontier.pop()
            elif method == 'a_star':
                _, node = heapq.heappop(frontier)

            self.num_explored += 1

            if node.state == self.goal:
                self.reconstruct_solution(node)
                return

            self.explored.add(node.state)

            for action, state in sorted(self.neighbors(node.state), key=lambda x: x[0]):
                if state not in self.explored:
                    cost = node.cost + 1
                    child = Node(state=state, parent=node, action=action, cost=cost)
                    
                    if method == 'a_star':
                        heapq.heappush(frontier, (cost + self.heuristic(state), child))
                    else:
                        frontier.append(child)

        raise Exception("No solution")

    def reconstruct_solution(self, node):
        actions = []
        cells = []
        while node.parent is not None:
            actions.append(node.action)
            cells.append(node.state)
            node = node.parent
        actions.reverse()
        cells.reverse()
        self.solution = (actions, cells)


from collections import deque

class Pathfinder():
    def __init__(self,start,end,map):
        self.startPoint = start
        self.endPoint = end
        self.map = map
        self.path = []
        self.workingPath = set()
        self.obstacles = []
        self.maxCols = len(self.map)
        self.maxRows = len(self.map[0])

    def calculatePath(self):
        path = self.bfs(self.startPoint)
        return path
    
    def isValid(self,row,col):
        if row < self.maxRows and col < self.maxCols and row >= 0 and col >= 0:
            return self.map[row][col] not in self.obstacles
        else:
            return False
    
    def setObstacle(self,obstacle):
        self.obstacles.append(obstacle)

    def bfs(self,start):
        queue = deque([(start, [])])
        visited = set()

        while queue:
            current, path = queue.popleft()
            row, col = current

            if current == self.endPoint:
                return path + [current]
            
            if current in visited:
                continue

            visited.add(current)

            for r, c in [(0,1), (1,0), (0,-1), (-1,0)]:
                newR, newC = row + r, col + c
                nextPos = (newR, newC)

                if self.isValid(newR, newC):
                    queue.append((nextPos, path + [current]))

        return None

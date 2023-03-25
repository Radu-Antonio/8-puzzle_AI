import pygame, random, heapq, copy, time

pygame.init()
WIDTH, HEIGHT = 750, 750
DONE = False
moves, offset = 0, 125
pygame.display.set_caption('8-puzzle')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(pygame.font.get_default_font(), 68)

class Node:
    def __init__(self, info, parent=None, g=0, h=0):
        self.info = info
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def root_path(self):
        path = []
        while self:
            path.append(self)
            self = self.parent
        return path[::-1]

    def __lt__(self, node):
        if self.f == node.f:
            return self.g < node.g
        return self.f < node.f

class Graph:
    def __init__(self, start=[], end=((1,2,3),(4,5,6),(7,8,0))):
        self.start = start
        self.end = end
    
    def generate(self):
        arr = list(range(9))
        random.shuffle(arr)
        while True:
            inversions = 0
            for idx, cell in enumerate(arr):
                for cell2 in arr[idx+1:]:
                    if cell == 0 or cell2 == 0:
                        continue
                    if cell > cell2:
                        inversions += 1
            if inversions % 2 == 0:
                self.start = []
                for i in range(3):
                    self.start.append(tuple(arr[i * 3:(i + 1) * 3]))
                self.start = tuple(map(tuple, self.start))
                return
            random.shuffle(arr)

    def estimate_h(self, state):
        if self.scope(state):
            return 0

        coord_start = dict()
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    continue
                coord_start[state[i][j]] = (i, j)
        coord_end = dict()
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    continue
                coord_end[state[i][j]] = (i, j)
        cost = 0
        for num in range(1, 9):
            x1, y1, x2, y2 = *coord_start[num], *coord_end[num]
            cost += abs(x1-x2) + abs(y1-y2)
        return cost
            
    def scope(self, info):
        return info == self.end

    def successors(self, node):
        succ = []
        state = node.info
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    empty = (i, j)
                    break

        for i, j in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            x, y = empty[0] + i, empty[1] + j            
            if 0 <= x < 3 and 0 <= y < 3:
                new_state = list(map(list, copy.deepcopy(state)))
                new_state[empty[0]][empty[1]] = new_state[x][y]
                new_state[x][y] = 0
                new_state = tuple(map(tuple, new_state))
                succ.append(Node(new_state, node, node.g + 1, self.estimate_h(new_state)))
        return succ

def a_star(graph: Graph):
    start = time.time()
    start_node = Node(graph.start)
    heap = [(0, start_node)]
    visited = set()

    while heap:
        curr_state = heapq.heappop(heap)[1]
        visited.add(curr_state.info)

        if graph.scope(curr_state.info):
            print(f"{time.time() - start:.2f} sec")
            return curr_state

        for next_state in graph.successors(curr_state):
            if next_state.info not in visited:
                heapq.heappush(heap, (next_state.f, next_state))
                visited.add(next_state.info)

def loading(board):
    screen.fill((216, 220, 221))
    textSize = 250
    for i in range(3):
        for j in range(3):
            index = board[i][j]
            if index == 0:
                continue
            square_rect = pygame.Rect(textSize * j + offset - 117, textSize * i + offset - 117, 235, 235)
            pygame.draw.rect(screen, (72, 162, 219), square_rect)
            text = font.render(str(index), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (textSize * j + offset, textSize * i + offset)
            screen.blit(text, textRect)

    text = pygame.font.Font(pygame.font.get_default_font(), 55).render('Generating Solution...', True, (34, 139, 34))
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2 - 100)
    screen.blit(text, textRect)
    pygame.display.update()

def draw(board):
    screen.fill((216, 220, 221))
    textSize = 250
    for i in range(3):
        for j in range(3):
            index = board[i][j]
            if index == 0:
                continue
            square_rect = pygame.Rect(textSize * j + offset - 117, textSize * i + offset - 117, 235, 235)
            pygame.draw.rect(screen, (72, 162, 219), square_rect)
            text = font.render(str(index), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (textSize * j + offset, textSize * i + offset)
            screen.blit(text, textRect)

def num_moves():
    text = pygame.font.Font(pygame.font.get_default_font(), 27).render(f"moves: {moves}", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (80, 25)
    screen.blit(text, textRect)

def drawWin():
    text = pygame.font.Font(pygame.font.get_default_font(), 90).render('Finished', True, (34, 139, 34))
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2 - 100)
    screen.blit(text, textRect)

def main():
    global moves
    graph = Graph()
    graph.generate()
    # graph.start = ((8, 6, 7), (2, 5, 4), (3, 0, 1)) # 31 moves to solve
    loading(graph.start)
    ans = a_star(graph).root_path()

    for state in ans:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.time.wait(1000)
        draw(state.info)
        num_moves()
        pygame.display.update()
        moves += 1

    moves -= 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        draw(state.info)
        num_moves()
        drawWin()
        pygame.display.update()

if __name__ == '__main__':
    main()
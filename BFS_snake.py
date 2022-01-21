import pygame, random, operator
from time import time
from queue import Queue
from matplotlib import pyplot as plt

pygame.init()

WIN_DIMENSION = 480

BKGCOLOUR = (141, 168, 32)
FONT = pygame.font.SysFont(None, 25)

GRIDSIZE = 20
WALL_DIMENSION = WIN_DIMENSION + GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
NB = 0
PATH_EXIST = False

class Snake():

    def __init__(self):
        self.steps = []
        self.scores = []
        self.score = 0
        self.step = 0
        self.length = 3
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.coordinates = [((WIN_DIMENSION / 2), (WIN_DIMENSION / 2))]        
        self.colour = (0, 0, 0)        

    def turn(self, point):
        if (point[0] * - 1, point[1] * - 1) == self.direction:
            return
        else:
            self.direction = point
          
    def get_head_position(self):
        return self.coordinates[0]  
                  
    def move(self):
        current = self.get_head_position()
        
        x, y = self.direction
        new = (((current[0] + (x * GRIDSIZE)) % WALL_DIMENSION), (current[1] + (y * GRIDSIZE)) % WALL_DIMENSION)
        if new:
            self.step += 1
        if new in self.coordinates[0:]:
            self.reset()
        else:
            self.coordinates.insert(0, new)
            if len(self.coordinates) > self.length:
                self.coordinates.pop()

    def reset(self):
        global PATH_EXIST
        global NB
        global GRAPH
        self.scores.append(self.score)
        self.steps.append(self.step)
        self.length = 3
        self.coordinates = [((WIN_DIMENSION / 2), (WIN_DIMENSION / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.step = 0
        GRAPH = create_graph(SNAKE.coordinates)
        PATH_EXIST = False 
        NB = 0 
        
    def draw(self, surface):
        for p in self.coordinates:
            snake = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.colour, snake)
            
class Apple():

    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        self.colour = (0, 0, 0)

    def randomize_position(self, coordinates=[]):     
        Xs = [item[0] for item in coordinates]
        Ys = [item[1] for item in coordinates]       
        try:   
            x_choice = random.choice([i for i in range(20, 440, 20) if i not in Xs])
            y_choice = random.choice([i for i in range(20, 440, 20) if i not in Ys])         
        except:
            x_choice = random.choice([i for i in range(20, 440, 20)])
            y_choice = random.choice([i for i in range(20, 440, 20)]) 
        
        self.position = (x_choice, y_choice)

    def draw(self, surface):               
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.colour, r)
        
SNAKE = Snake()
APPLE = Apple()

path = []

def addition_tuple(a, b):
    return tuple(map(operator.add, a, b))

def create_graph(coordinates = []):
    UP = (0, -20)
    DOWN = (0, 20)
    LEFT = (-20, 0)
    RIGHT = (20, 0)
    graph = {}
    
    for x in range(0, 461 ,20):
        for y in range(0, 461, 20):
            point = (x, y)
            if(x == 0):
                go_right = addition_tuple(point, RIGHT)
                if(y == 0):                
                    go_down = addition_tuple(point, DOWN)
                    if(go_right in coordinates):
                        if(go_down in coordinates):
                            graph[point] = []
                        else:
                            graph[point] = [go_down]
                    elif(go_down in coordinates):
                        graph[point] = [go_down]
                    else:
                        graph[point] = [go_right, go_down]


                elif(y == 460):                
                    go_up = addition_tuple(point, UP)
                    if(go_right in coordinates):
                        if(go_up in coordinates):
                            graph[point] = []
                        else:
                            graph[point] = [go_up]
                    elif(go_up in coordinates):
                        graph[point] = [go_up]
                    else:
                        graph[point] = [go_right, go_up]
                else:
                    if(go_right in coordinates):
                        graph[point] = []
                    else:
                        graph[point] = [go_right]
            elif(x == 460):
                go_left = addition_tuple(point, LEFT)                
                if(y == 0):
                    go_down = addition_tuple(point, DOWN)
                    if(go_left in coordinates):
                        if(go_down in coordinates):
                            graph[point] = []
                        else:
                            graph[point] = [go_down]
                    elif(go_down in coordinates):
                        graph[point] = [go_down]
                    else:
                        graph[point] = [go_left, go_down]
                    graph[point] = [go_left, go_down]
                elif(y == 460):
                    go_up = addition_tuple(point, UP)
                    if(go_left in coordinates):
                        if(go_up in coordinates):
                            graph[point] = []
                        else:
                            graph[point] = [go_up]
                    elif(go_up in coordinates):
                        graph[point] = [go_up]
                    else:
                        graph[point] = [go_left, go_up]
                    graph[point] = [go_left, go_up]
                else:
                    if(go_left in coordinates):
                        graph[point] = []
                    else:
                        graph[point] = [go_left]                    
            elif(y == 0):
                go_down = addition_tuple(point, DOWN)
                if(go_down in coordinates):
                    graph[point] = []
                else:                
                    graph[point] = [go_down]
            elif(y == 460):
                go_up = addition_tuple(point, UP)
                if(go_up in coordinates):
                    graph[point] = []
                else:                
                    graph[point] = [go_up]                
            else:
                go_up = addition_tuple(point, UP)
                go_down = addition_tuple(point, DOWN)
                go_left = addition_tuple(point, LEFT)
                go_right = addition_tuple(point, RIGHT)
                
                to_check = [go_down, go_up, go_left, go_right]
                to_add = []

                for item in to_check:
                    if item not in coordinates:
                        to_add.append(item)
                
                graph[point] = to_add
    
    return graph

GRAPH = create_graph()

def BFS(adj_list, start_node, target_node):
    visited = set()
    queue = Queue()

    queue.put(start_node)
    visited.add(start_node)

    parent = dict()
    parent[start_node] = None

    path_found = False
    while not queue.empty():
        current_node = queue.get()
        if current_node == target_node:
            path_found = True
            break

        for next_node in adj_list[current_node]:
            if next_node not in visited:
                queue.put(next_node)
                parent[next_node] = current_node
                visited.add(next_node)

    path = []
    new_path = []
    if path_found:
        path.append(target_node)
        while parent[target_node] is not None:
            path.append(parent[target_node]) 
            target_node = parent[target_node]
        path.reverse()
      
    for k in range(len(path) - 1):
        new_path.append(tuple(map(lambda i, j: int((i - j)/20),path[k+1],path[k])))
    return new_path

def collide():
    try:
        x = SNAKE.get_head_position()[0]
        y = SNAKE.get_head_position()[1]
    except:
        print(SNAKE.get_head_position())
    
    if x > WIN_DIMENSION - GRIDSIZE or x < 0 or y > WIN_DIMENSION - GRIDSIZE or y < 0:
        SNAKE.reset()

def eat():
    global PATH_EXIST
    global NB
    global GRAPH
    if SNAKE.get_head_position() == APPLE.position:
        SNAKE.length += 1
        SNAKE.score += 1
        APPLE.randomize_position(SNAKE.coordinates)
        GRAPH = create_graph(SNAKE.coordinates)
        PATH_EXIST = False 
        NB = 0           

def draw_grid(surface):
    pygame.draw.rect(surface, BKGCOLOUR, pygame.Rect(0, 0, WIN_DIMENSION, WIN_DIMENSION))
    x = 0
    y = 0
    for l in range(WIN_DIMENSION):
        x = x + GRIDSIZE
        y = y + GRIDSIZE
        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, WIN_DIMENSION))
        pygame.draw.line(surface, (0, 0, 0), (0, y), (WIN_DIMENSION, y))

def redraw_window():
    surface = pygame.Surface((WIN.get_size()))
    surface = surface.convert()
    draw_grid(surface)
    SNAKE.draw(surface)
    APPLE.draw(surface)
    scoreboard = FONT.render("Score {0}".format(SNAKE.score), 1, (0, 0, 0))
    surface.blit(scoreboard, (1, 1))
    WIN.blit(surface, (0, 0))
    pygame.display.flip()
    pygame.display.update()
               
def main():
    global WIN
    global NB
    global PATH_EXIST

    WIN = pygame.display.set_mode((WIN_DIMENSION, WIN_DIMENSION))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    fps = 300


    run = True
    while run == True:  
                                      
        clock.tick(fps)

        redraw_window()  

        if(PATH_EXIST == False):
            start = time()

            apple = APPLE.position            
            path = BFS(GRAPH, SNAKE.get_head_position(), apple)

            end = time()
        
        if path!=[]:            
            PATH_EXIST = True            
            
        if(PATH_EXIST == True):      
            try:
                direction = path[NB]
            except:
                PATH_EXIST = False
                NB = 0
                continue

            SNAKE.turn(direction)
            NB += 1
            
        SNAKE.move()
                
        collide()
        eat()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                

    pygame.quit()
    plt.scatter(SNAKE.steps, SNAKE.scores)
    plt.xlabel("Steps")
    plt.ylabel("Score")


if __name__ == "__main__":
    main()
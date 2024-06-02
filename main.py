import random
import heapq

class Pole:
    def __init__(self, x, y):
        self.y = int(y)
        self.x = int(x)
        self.wsp = 0


class Agent:
    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def a_star(walls, start, goal):
        rows, cols = len(walls), len(walls[0])
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}
        f_score = {start: Agent.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            neighbors = [
                (current[0] + 1, current[1]),
                (current[0] - 1, current[1]),
                (current[0], current[1] + 1),
                (current[0], current[1] - 1)
            ]

            for neighbor in neighbors:
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and walls[neighbor[0]][neighbor[1]] == 0:
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + Agent.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    @staticmethod
    def get_directions(walls, start, goal):

        directions = list()
        tiles = Agent.a_star(walls, start, goal)
        if tiles is None:
            return None
        previous = tiles[0]
        for tile in tiles[1:]:
            dir = (tile[0]-previous[0], tile[1] - previous[1])
            previous = tile
            if dir[1] == 1:
                directions.append('r')
            if dir[1] == -1:
                directions.append('l')
            if dir[0] == -1:
                directions.append('d')
            if dir[0] == 1:
                directions.append('u')
        return directions

    def __init__(self):
        self.pola = [[0 for _ in range(12)] for _ in range(10)]
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                self.pola[poziom][pole] = Pole(pole, poziom)

    def get_value_of_tile(self, game_state, player_state, walls, location):
        if not game_state.is_in_bounds(location):
            return -1000
        if walls[location[1]][location[0]] == 1:
            return -1000
        w = self.pola[location[1]][location[0]].wsp
        return w

    def next_move(self, game_state, player_state):
        self.przelicz_wszystkie_wspolczyniki_pol(game_state, player_state)
        walls = [[0 for _ in range(12)] for _ in range(10)]

        for block in game_state.all_blocks:
            walls[block[1]][block[0]] = 1
        for bomb in game_state.bombs:
            walls[bomb[1]][bomb[0]] = 1
        for opponent in game_state.opponents(player_state.id):
            walls[opponent[1]][opponent[0]] = 1
        location = player_state.location

        current_value = self.get_value_of_tile(game_state, player_state, walls, location)

        if player_state.ammo > 0 and not game_state.entity_at(location) == "b":
            if game_state.tick_number < 700:
                if current_value >= 10:
                    return 'p'
            else:
                if current_value >= 5:
                    return 'p'

        if player_state.ammo == 0:
            self.przelicz_defensywnie(game_state, player_state)
        possible_moves = dict()
        r = 4
        for x in range(-r, r + 1):
            for y in range(-r, r + 1):
                possible_moves[(location[0] + x, location[1] + y)] = self.get_value_of_tile(game_state, player_state, walls, (location[0] + x, location[1] + y))

        possible_moves = dict(sorted(possible_moves.items(), key=lambda item: item[1], reverse=True))
        for move in possible_moves:
            dirs = self.get_directions(walls, (location[1], location[0]), (move[1], move[0]))
            if move == location:
                return ''
            if dirs is not None:
                return dirs[0]
        return ''

    def przelicz_wszystkie_wspolczyniki_pol(self, game_state, player_state):
        for poziom in self.pola:
            for pole in poziom:
                pole.wsp = 0
        for i in game_state.soft_blocks:
            if 4 >= i[0] - player_state.location[0] >= -4 and 4 >= i[1] - player_state.location[1] >= -4:
                for X in range(-2, 3):
                    if game_state.is_in_bounds((i[0] + X, i[1])):
                        (self.pola[i[1]][i[0] + X]).wsp += 7
                for Y in range(-2, 3):
                    if game_state.is_in_bounds((i[0], i[1] + Y)):
                        self.pola[i[1] + Y][i[0]].wsp += 7
                        print(f'Dodaję 5 do pola: ({[i[0]]},{[i[1] + Y]}) za {i[0]}, {i[1]}')
        for i in game_state.ore_blocks:
            if 4 >= i[0] - player_state.location[0] >= -4 and 4 >= i[1] - player_state.location[1] >= -4:
                for X in range(-2, 3):
                    if game_state.is_in_bounds((i[0] + X, i[1])):
                        (self.pola[i[1]][i[0] + X]).wsp += 4
                        print(f'Dodaję 3 do pola: ({[i[0] + X]},{[i[1]]}) za {i[0]}, {i[1]}')
                for Y in range(-2, 3):
                    if game_state.is_in_bounds((i[0], i[1] + Y)):
                        self.pola[i[1] + Y][i[0]].wsp += 4
                        print(f'Dodaję 3 do pola: ({[i[0]]},{[i[1] + Y]}) za {i[0]}, {i[1]}')
        for i in game_state.ammo:
            if 4 >= i[0] - player_state.location[0] >= -4 and 4 >= i[1] - player_state.location[1] >= -4:
                if game_state.is_in_bounds((i[0], i[1])):
                    self.pola[i[1]][i[0]].wsp += 40
                    print(f'Dodaję 20 do pola: ({[i[0]]},{[i[1]]}) za {i[0]}, {i[1]}')
        for i in game_state.indestructible_blocks:
            if 4 >= i[0] - player_state.location[0] >= -4 and 4 >= i[1] - player_state.location[1] >= -4:
                for X in range(-1, 2):
                    if game_state.is_in_bounds((i[0] + X, i[1])):
                        (self.pola[i[1]][i[0] + X]).wsp += -2
                        print(f'Dodaję -2 do pola: ({[i[0] + X]},{[i[1]]}) za {i[0]}, {i[1]}')
                for Y in range(-1, 2):
                    if game_state.is_in_bounds((i[0], i[1] + Y)):
                        self.pola[i[1] + Y][i[0]].wsp += -2
                        print(f'Dodaję -2 do pola: ({[i[0]]},{[i[1] + Y]}) za {i[0]}, {i[1]}')
        for i in game_state.bombs:
            if 4 >= i[0] - player_state.location[0] >= -4 and 4 >= i[1] - player_state.location[1] >= -4:
                for X in range(-2, 3):
                    if game_state.is_in_bounds((i[0] + X, i[1])):
                        (self.pola[i[1]][i[0] + X]).wsp += -30
                        print(f'Dodaję -20 do pola: ({[i[0] + X]},{[i[1]]}) za {i[0]}, {i[1]}')
                for Y in range(-2, 3):
                    if game_state.is_in_bounds((i[0], i[1] + Y)):
                        self.pola[i[1] + Y][i[0]].wsp += -30
                        print(f'Dodaję -20 do pola: ({[i[0]]},{[i[1] + Y]}) za {i[0]}, {i[1]}')
        for i in game_state.treasure:
            if 4 >= i[0] - player_state.location[0] >= -4 and 4 >= i[1] - player_state.location[1] >= -4:
                if game_state.is_in_bounds((i[0], i[1])):
                    self.pola[i[1]][i[0]].wsp += 8
                    print(f'Dodaję 8 do pola: ({[i[0]]},{[i[1]]}) za {i[0]}, {i[1]}')

        for row in self.pola[::-1]:
            for block in row:
                print("[", block.wsp, "]", end=" ")
            print()

    def przelicz_defensywnie(self, game_state, player_state):
        for poziom in self.pola:
            for pole in poziom:
                pole.wsp = 0
                print(f'Wyzerowano: {pole.wsp}')
        for i in game_state.ammo:
            if 4 >= i[0] - player_state.location[0] >= -4 and 4 >= i[1] - player_state.location[1] >= -4:
                if game_state.is_in_bounds((i[0], i[1])):
                    self.pola[i[1]][i[0]].wsp += 20
                    print(f'Dodaję 20 do pola: ({[i[0]]},{[i[1]]}) za {i[0]}, {i[1]}')
        for i in game_state.indestructible_blocks:
            if 4 >= i[0] - player_state.location[0] >= -4 and 4 >= i[1] - player_state.location[1] >= -4:
                for X in range(-1, 2):
                    if game_state.is_in_bounds((i[0] + X, i[1])):
                        (self.pola[i[1]][i[0] + X]).wsp += -2
                        print(f'Dodaję -2 do pola: ({[i[0] + X]},{[i[1]]}) za {i[0]}, {i[1]}')
                for Y in range(-1, 2):
                    if game_state.is_in_bounds((i[0], i[1] + Y)):
                        self.pola[i[1] + Y][i[0]].wsp += -2
                        print(f'Dodaję -2 do pola: ({[i[0]]},{[i[1] + Y]}) za {i[0]}, {i[1]}')
        for i in game_state.bombs:
            if 4 >= i[0] - player_state.location[0] >= -4 and 4 >= i[1] - player_state.location[1] >= -4:
                for X in range(-2, 3):
                    if game_state.is_in_bounds((i[0] + X, i[1])):
                        (self.pola[i[1]][i[0] + X]).wsp += -20
                        print(f'Dodaję -20 do pola: ({[i[0] + X]},{[i[1]]}) za {i[0]}, {i[1]}')
                for Y in range(-2, 3):
                    if game_state.is_in_bounds((i[0], i[1] + Y)):
                        self.pola[i[1] + Y][i[0]].wsp += -20
                        print(f'Dodaję -20 do pola: ({[i[0]]},{[i[1] + Y]}) za {i[0]}, {i[1]}')
        for i in game_state.treasure:
            if 4 >= i[0] - player_state.location[0] >= -4 and 4 >= i[1] - player_state.location[1] >= -4:
                if game_state.is_in_bounds((i[0], i[1])):
                    self.pola[i[1]][i[0]].wsp += 8
                    print(f'Dodaję 8 do pola: ({[i[0]]},{[i[1]]}) za {i[0]}, {i[1]}')

        for row in self.pola[::-1]:
            for block in row:
                print("[", block.wsp, "]", end=" ")
            print()


agencik = Agent()

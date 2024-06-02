import random

class Pole:
    def __init__(self, x, y):
        self.y = int(y)
        self.x = int(x)
        self.wsp = int(x)*int(y)


class Agent:
    def __init__(self):
        # self.strefy = [Strefa(0,0,5,4), Strefa(6,0,11,4), Strefa(0,5,5,9), Strefa(6,5,11,9)]
        self.pola = [[0 for _ in range(12)] for _ in range(10)]
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                self.pola[poziom][pole] = Pole(pole, poziom)
                print(f'[{self.pola[poziom][pole].wsp}]', end=' ')
            print()


    def next_move(self, game_state, player_state):
        actions = ['', 'u', 'd', 'l', 'r', 'p']
        self.przelicz_wszystkie_wspolczyniki_pol(game_state, player_state)

        return random.choice(actions)

    def wspolczynik_stref(self, game_state, player_state):
        for strefa in self.strefy:
            strefa.wsp = 0
            print(f'Wyzerowano: {strefa.wsp}')
        for i in game_state.soft_blocks:
            for strefa in self.strefy:
                if strefa.x <= i[0] <= strefa.X and strefa.y <= i[1] <= strefa.Y:
                    strefa.wsp += 5
                    print(f'Dodaję 5 do strefy: {strefa.x}, {strefa.y} za {i[0]}, {i[1]}')
        for i in game_state.ore_blocks:
            for strefa in self.strefy:
                if strefa.x <= i[0] <= strefa.X and strefa.y <= i[1] <= strefa.Y:
                    strefa.wsp += 3
                    print(f'Dodaję 3 do strefy: {strefa.x}, {strefa.y} za {i[0]}, {i[1]}')
        for i in game_state.ammo:
            for strefa in self.strefy:
                if strefa.x <= i[0] <= strefa.X and strefa.y <= i[1] <= strefa.Y:
                    strefa.wsp += 7
                    print(f'Dodaję 7 do strefy: {strefa.x}, {strefa.y} za {i[0]}, {i[1]}')
        for i in game_state.indestructible_blocks:
            for strefa in self.strefy:
                if strefa.x <= i[0] <= strefa.X and strefa.y <= i[1] <= strefa.Y:
                    strefa.wsp += -2
                    print(f'Dodaję -2 do strefy: {strefa.x}, {strefa.y} za {i[0]}, {i[1]}')

        for strefa in self.strefy:
            print(f'Współczynnik dla strefy {strefa.x}, {strefa.y}: {strefa.wsp}')
        print('\n')

    def przelicz_wszystkie_wspolczyniki_pol(self, game_state, player_state):
        for poziom in self.pola:
            for pole in poziom:
                pole.wsp = 0
                print(f'Wyzerowano: {pole.wsp}')
        for i in game_state.soft_blocks:
            for X in range(-2, 3):
                if game_state.is_in_bounds((i[0]+X,i[1])):
                    (self.pola[i[1]][i[0]+X]).wsp += 5
                    print(f'Dodaję 5 do pola: ({[i[0]+X]},{[i[1]]}) za {i[0]}, {i[1]}')
            for Y in range(-2, 3):
                if game_state.is_in_bounds((i[0],i[1]+Y)):
                    self.pola[i[1]+Y][i[0]].wsp += 5
                    print(f'Dodaję 5 do pola: ({[i[0]]},{[i[1]+Y]}) za {i[0]}, {i[1]}')
        for i in game_state.ore_blocks:
            for X in range(-2, 3):
                if game_state.is_in_bounds((i[0]+X,i[1])):
                    (self.pola[i[1]][i[0]+X]).wsp += 3
                    print(f'Dodaję 3 do pola: ({[i[0]+X]},{[i[1]]}) za {i[0]}, {i[1]}')
            for Y in range(-2, 3):
                if game_state.is_in_bounds((i[0],i[1]+Y)):
                    self.pola[i[1]+Y][i[0]].wsp += 3
                    print(f'Dodaję 3 do pola: ({[i[0]]},{[i[1]+Y]}) za {i[0]}, {i[1]}')
        for i in game_state.ammo:
            if game_state.is_in_bounds((i[0],i[1])):
                self.pola[i[1]][i[0]].wsp += 20
                print(f'Dodaję 20 do pola: ({[i[0]]},{[i[1]]}) za {i[0]}, {i[1]}')
        for i in game_state.indestructible_blocks:
            for X in range(-1, 2):
                if game_state.is_in_bounds((i[0]+X,i[1])):
                    (self.pola[i[1]][i[0]+X]).wsp += -2
                    print(f'Dodaję -2 do pola: ({[i[0]+X]},{[i[1]]}) za {i[0]}, {i[1]}')
            for Y in range(-1, 2):
                if game_state.is_in_bounds((i[0],i[1]+Y)):
                    self.pola[i[1]+Y][i[0]].wsp += -2
                    print(f'Dodaję -2 do pola: ({[i[0]]},{[i[1]+Y]}) za {i[0]}, {i[1]}')
        for i in game_state.bombs:
            for X in range(-2, 3):
                if game_state.is_in_bounds((i[0]+X,i[1])):
                    (self.pola[i[1]][i[0]+X]).wsp += -20
                    print(f'Dodaję -20 do pola: ({[i[0]+X]},{[i[1]]}) za {i[0]}, {i[1]}')
            for Y in range(-2, 3):
                if game_state.is_in_bounds((i[0],i[1]+Y)):
                    self.pola[i[1]+Y][i[0]].wsp += -20
                    print(f'Dodaję -20 do pola: ({[i[0]]},{[i[1]+Y]}) za {i[0]}, {i[1]}')


        for row in self.pola[::-1]:
            for block in row:
                print("[",  block.wsp,  "]", end=" ")
            print()



class Strefa:
    def __init__(self, x, y, X, Y):
        self.Y = Y
        self.X = X
        self.y = y
        self.x = x
        self.wsp = 0


agencik = Agent()

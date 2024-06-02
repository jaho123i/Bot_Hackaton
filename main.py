import random


class Pole:
    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.wsp = 0


class Agent:
    def __init__(self):
        self.strefy = [Strefa(0,0,5,4), Strefa(6,0,11,4), Strefa(0,5,5,9), Strefa(6,5,11,9)]
        self.pola = [[0]*12]*10
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                self.pola[poziom][pole] = Pole(pole, poziom)
                print(f'[{self.pola[poziom][pole].wsp}]', end=' ')
            print()


    def next_move(self, game_state, player_state):
        actions = ['', 'u', 'd', 'l', 'r', 'p']
        self.wspolczynik_stref(game_state, player_state)
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

    def wspolczynik_pola(self, game_state, player_state):
        for pole in self.strefy:
            pole.wsp = 0
            print(f'Wyzerowano: {pole.wsp}')
        for i in game_state.soft_blocks:
            for pole in self.strefy:
                if pole.x <= i[0] <= pole.X and pole.y <= i[1] <= pole.Y:
                    pole.wsp += 5
                    print(f'Dodaję 5 do strefy: {pole.x}, {pole.y} za {i[0]}, {i[1]}')
        for i in game_state.ore_blocks:
            for pole in self.strefy:
                if pole.x <= i[0] <= pole.X and pole.y <= i[1] <= pole.Y:
                    pole.wsp += 3
                    print(f'Dodaję 3 do strefy: {pole.x}, {pole.y} za {i[0]}, {i[1]}')
        for i in game_state.ammo:
            for pole in self.strefy:
                if pole.x <= i[0] <= pole.X and pole.y <= i[1] <= pole.Y:
                    pole.wsp += 7
                    print(f'Dodaję 7 do strefy: {pole.x}, {pole.y} za {i[0]}, {i[1]}')
        for i in game_state.indestructible_blocks:
            for pole in self.strefy:
                if pole.x <= i[0] <= pole.X and pole.y <= i[1] <= pole.Y:
                    pole.wsp += -2
                    print(f'Dodaję -2 do strefy: {pole.x}, {pole.y} za {i[0]}, {i[1]}')

        for pole in self.strefy:
            print(f'Współczynnik dla strefy {pole.x}, {pole.y}: {pole.wsp}')
        print('\n')


class Strefa:
    def __init__(self, x, y, X, Y):
        self.Y = Y
        self.X = X
        self.y = y
        self.x = x
        self.wsp = 0


agencik = Agent()

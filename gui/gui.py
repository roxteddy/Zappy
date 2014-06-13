from connexions import Sock
from stuff import log

class Game(object):
    teams = {}
    map = {}
    def __init__(self, Sock):
        self.s = Sock

    def welcome(self):
        self.s.send("GRAPHIC")

    def coordinate(self, x, y, o = None):
        if x > self.x or y > self.y or (o is not None and (o > 4 or o <= 0)) or x < 0 or y < 0:
            return False
        else:
            return True
    def print_map(self):
        for key in self.map:
            print key, self.map[key]

    def msz(self, message):
        """
        0 = nourriture
        1 = linemate
        2 = deraumere
        3 = sibur
        4 = mendiane
        5 = phiras
        6 = thystame
        """
        try:
            if len(message) != 2:
                raise Exception("wrong parameters")
            self.x = int(message[0])
            self.y = int(message[1])
        except Exception, e:
            log(e)
            return None
        for i in range(0, self.y):
            self.map[i] = {}
            for j in range(0, self.x):
                self.map[i][j] = []

    def bct(self, message):
        from object_map import ObjectFactory
        try:
            message = tuple(
                [int(integer) for integer in message]
            )
            if len(message) != 9:
                raise Exception("wrong parameters")
            if not self.coordinate(*message[0:2]):
                raise Exception("bad coordinates %d/%d" % (message[0], message[1]))
            x, y, l = message[0], message[1], message[2:]
            for i in range(0, len(l)):
                if l[i]:
                    if l[i] > 1 or l[i] < 0:
                        raise Exception("bad number of object %d" % i)
                    else:
                        self.map[y][x].append(ObjectFactory(i, x, y))
        except Exception, e:
            return log(e)
        
    @classmethod
    def tna(cls, message):
        if message[0] in cls.teams:
            return log("team %s already exists" % message[0])
        cls.teams[message[0]] = []

    def eht(self, message):
        try:
            if message[0][0] != '#':
                raise Exception("bad number")
            message = int(message[0][1:])
        except Exception, e:
            return log(e)
        from object_map import Egg
        for i in self.map:
            for x in self.map[i]:
                for t in self.map[i][x]:
                    if isinstance(t, Egg) and t.e == message:
                        if t.o == 1:
                            return log("egg %d has already hatched out" % message)
                        else:
                            index = self.map[i][x].index(t)
                            self.map[i][x][index].o = 1
                            return log("egg %d has hatched out" % message)
        return log("egg %d not found" % message[0])

    def edi(self, message):
        from object_map import Egg
        try:
            if message[0][0] != '#':
                raise Exception("bad number")
            message[0] = int(message[0][1:])
        except Exception, e:
            return log(e)
        for i in self.map:
            for x in self.map[i]:
                for t in self.map[i][x]:
                    if isinstance(t, Egg) and message[0] == t.e:
                        if t.o == 0:
                            return log("egg %d has not hatched out, it cannot die" % message[0])
                        self.map[i][x].remove(t)
                        return log("egg %d died" % message[0])
        return log("egg %d not found" % message[0])        

    def enw(self, message):
        from object_map import Egg
        try:
            if len(message) != 4:
                raise Exception("wrong parameters")
            if message[1][0] != '#' or message[0][0] != '#':
                raise Exception("bad player number")
            message[1] = message[1][1:]
            message[0] = message[0][1:]
            message = tuple(
                [int(integer) for integer in message]
            )
            e = Egg(*message)
            if not self.coordinate(message[2], message[3]):
                raise Exception("bad coordinates %d / %d" % (message[2], message[3]))
            for i in self.map:
                for x in self.map[i]:
                    for t in self.map[i][x]:
                        if isinstance(t, Egg):
                            raise Exception ("egg %d already exist" % message[0])
            for t in self.__class__.teams.keys():
                for player in self.__class__.teams[t]:
                    if message[1] == player.n:
                        self.map[message[2]][message[3]].append(e)
                        return None
            raise Exception("player %d does not exist" % message[1])
        except Exception, e:
            return log(e)

    def smg(self, message):
        log("server says " + message[0])

    def pnw(self, message):
        from object_map import Player
        try:
            if len(message) != 6:
                raise Exception("wrong parameters")
            team = message.pop(5)
            if not team in self.__class__.teams:
                raise Exception("team %s does not exist" % team)
            if message[0][0] != '#':
                raise Exception("bad player number")
            message[0] = message[0][1:]
            message = tuple(
                [int(integer) for integer in message]
            )
            if not self.coordinate(*message[1:3]):
                raise Exception("bad coordinates %d / %d / %d" % (message[1], message[2], message[3]))
            p = Player(team, *message[0:5])
            for t in self.__class__.teams.keys():
                for player in self.__class__.teams[t]:
                    if p == player:
                        raise Exception("player %d already exists" % p.n)
        except Exception, e:
            return log(e)
        self.__class__.teams[team].append(p)

    
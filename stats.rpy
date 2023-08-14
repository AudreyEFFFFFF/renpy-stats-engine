init -100 python:

    import random

    # defines some stuff that applies to all stats 
    # maybe stat sets can also contain other stat sets
    class stat_set(object):

        def __init__(self, dice, sides, stats*, stats_values**):
            self.stats = []
            for s in stats:
                self.stats.append(stat(s, 0, dice, sides))

            for s, val in stats_values:
                self.stats.append(stat(s, val, dice, sides))


    class stat(object):

        def __init__(self, name, base, dice, sides):
            self.name = name
            self.base = base
            self.num_dice = dice
            self.sides = sides


        def set_base(self, base):
            self.base = base


        def check(self, threshold):
            rolls = [random.randint(0, self.sides) for d in range(self.num_dice)]

            return sum(rolls) >= threshold
            

    def define_stat(name, base=0, dice=2, sides=6):
        # TODO check dice for string representation (ie 2d6) and take that as well
        return stat(name, base, dice, sides)


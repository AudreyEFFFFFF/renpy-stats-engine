init -100 python:

    # defines some stuff that applies to all stats 
    # maybe stat sets can also contain other stat sets
    class stat_set(object):

        def __init__(self, dice, stats*):
            self.stats = []
            #for stat in stats


    class stat(object):

        def __init__(self, name, base, dice, sides):
            self.name = name
            self.base = base
            self.num_dice = dice
            self.sides = sides


        def set_base(base):
            self.base = base


        def check(threshold):
            score = base
            for i in range(num_dice):
                score = score + random.randint(0, sides)

            return score >= threshold
            

    def define_stat(name, base=0, dice=2, sides=6):
        # TODO check dice for string representation (ie 2d6) and take that as well
        return new stat(name, base, dice, sides)


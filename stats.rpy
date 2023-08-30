init -100 python:

    import random

    # defines some stuff that applies to all stats 
    # TODO maybe stat sets can also contain other stat sets
    class stat_set(object):

        def __init__(self, dice, sides, stats_names, stats_values):
            self.stats = {}
            for s in stats_names:
                self.stats[s] = stat(s, 0, dice, sides)

            for s, val in stats_values:
                self.stats[s] = stat(s, val, dice, sides)

        def check(self, stat_name, threshold):
            """Makes a dice-roll check against stat named "stat_name", then returns True for success, False for fail"""
            return self.stats[stat_name].check(threshold)



    class stat(object):

        def __init__(self, name, base, dice, sides):
            self.name = name
            self.base = base
            self.num_dice = dice
            self.sides = sides


        def set_base(self, base):
            """Alters the base value of the stat"""
            self.base = base



        def check(self, threshold):
            """Makes a dice-roll check against this stat, then returns True for success, False for fail"""
            rolls = [random.randint(0, self.sides) for d in range(self.num_dice)]

            return sum(rolls) >= threshold


        def increment(self, amount=1):
            self.base = self.base + amount


        def decrement(self, amount=1):
            self.base = self.base - amount
            

    #TODO add checks on passed-in values, throw useful errors
    def define_stat(name, base=0, dice=0, sides=0):
        # TODO check dice for string representation (ie 2d6) and take that as well
        return stat(name, base, dice, sides)


    def define_stat_set(dice=0, sides=0, *stat_names, **stat_values):
        return stat_set(dice, sides, stat_names, stat_values)


screen stats_sidebar(stats):
    frame:
        xalign 1.0
        yalign 0.0
        use display_stats(stats)


screen display_stats(stats):            
    frame:      
        vbox:
            text "These are your stats" yalign 0.0 xalign 0.5
            vbox:
                for s in stats.stats.values():
                    hbox:                                                 
                        label s.name
                        label (" %d" % (s.base,)) xalign 1.0


screen customize_stats(stats):
    modal True
    sensitive True
    frame:      
        vbox:
            text "Customize your stats" yalign 0.0 xalign 0.5
            vbox:
                for s in stats.stats.values():
                    vbox:                                                 
                        label s.name
                        hbox:
                            textbutton "-" action Function(s.decrement)
                            label (" %d " % (s.base,))
                            textbutton "+" action Function(s.increment)
            textbutton "Done" action Hide()
                                    


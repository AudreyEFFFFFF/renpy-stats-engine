init -100 python:

    import random

    # defines some stuff that applies to all stats 
    # TODO maybe stat sets can also contain other stat sets
    class stat_set(object):

        def __init__(self, dice, sides, minimum, maximum, stats_names, stats_values):
            self.stats = {}
            for s in stats_names:
                self.stats[s] = stat(s, 0, dice, sides, minimum, maximum)

            for s, val in stats_values:
                self.stats[s] = stat(s, val, dice, sides, minimum, maximum)

            self.available_skillpoints = None

        def check(self, stat_name, threshold):
            """Makes a dice-roll check against stat named "stat_name", then returns True for success, False for fail"""
            return self.stats[stat_name].check(threshold)


        def allot_skillpoints(self, points):
            if self.available_skillpoints is None:
                self.available_skillpoints = 0
            self.available_skillpoints += points


        def increment(self, stat_name, amount=1):
            if self.stats[stat_name].increment(amount) and self.available_skillpoints is not None:
                self.available_skillpoints -= 1


        def decrement(self, stat_name, amount=1):
            if self.stats[stat_name].decrement(amount) and self.available_skillpoints is not None:
                self.available_skillpoints += 1


        def lock(self):
            for s in self.stats.values():
                s.lock()


        def clear_skillpoints():
            self.available_skillpoints = None



    class stat(object):

        def __init__(self, name, base, dice, sides, minimum, maximum):
            self.name = name
            self.base = base
            self.num_dice = dice
            self.sides = sides
            self.minimum = minimum
            self.maximum = maximum


        def set_base(self, base):
            """Alters the base value of the stat"""
            self.base = base



        def check(self, threshold):
            """Makes a dice-roll check against this stat, then returns True for success, False for fail"""
            rolls = [random.randint(0, self.sides) for d in range(self.num_dice)]

            return sum(rolls) >= threshold


        def increment(self, amount=1):
            if self.maximum is not None and (self.base + amount) > self.maximum:
                return False
            self.base += amount
            return True


        def decrement(self, amount=1):
            if self.minimum is not None and (self.base - amount) < self.minimum:
                return False
            self.base -= amount
            return True


        def lock(self):
            self.minimum = self.base



    #TODO add checks on passed-in values, throw useful errors
    def define_stat(name, base=0, dice=0, sides=0, minimum=None, maximum=None):
        # TODO check dice for string representation (ie 2d6) and take that as well
        return stat(name, base, dice, sides, minimum, maximum)


    def define_stat_set(dice=0, sides=0, minimum=None, maximum=None, *stat_names, **stat_values):
        return stat_set(dice, sides, minimum, maximum, stat_names, stat_values)


label customize_stats(stat_set, points, locking=True, use_it_or_lose_it=False):
    $ stat_set.allot_skillpoints(points)
    show screen customize_stats(stat_set)
    if locking:
        $ stat_set.lock()
    if use_it_or_lose_it:
        $ stat_set.clear_skillpoints()
    return


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
                        text s.name
                        text (" %d" % (s.base,)) xalign 1.0


screen customize_stats(stats):
    modal True
    sensitive True
    zorder 10
    frame:      
        vbox:
            text "Customize your stats" yalign 0.0 xalign 0.5
            if stats.available_skillpoints is not None:
                text ("Points remaining: %d" % stats.available_skillpoints) yalign 0.0 xalign 0.5

            vbox:
                for s_name, s in stats.stats.items():
                    vbox:                                                 
                        text s_name
                        hbox:
                            textbutton "-" action Function(stats.decrement, s_name)
                            text (" %d " % (s.base))
                            textbutton "+" action Function(stats.increment, s_name)
            textbutton "Done" action Hide()
                                    


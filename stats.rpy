init -100 python:

    import random

    # This class defines a set of stats that apply to a single character
    class stat_set(object):

        def __init__(self, dice, sides, minimum, maximum, stats_names, stats_values):
            self.stats = {}
            for s in stats_names:
                self.stats[s] = stat(s, 0, dice, sides, minimum, maximum)

            for s, val in stats_values:
                self.stats[s] = stat(s, val, dice, sides, minimum, maximum)

            self.available_skillpoints = None

        def check(self, stat_name, threshold, passive=False):
            """Makes a check against stat named 'stat_name', then returns True for success, False for fail"""
            if passive:
                return self.stats[stat_name].passive_check(threshold)
            return self.stats[stat_name].check(threshold)


        def get_value(self, stat_name):
            """Returns the base value of a stat with name 'stat_name'"""
            return self.stats[stat_name].get_base()


        def allot_skillpoints(self, points):
            if self.available_skillpoints is None:
                self.available_skillpoints = 0
            self.available_skillpoints += points


        def increment(self, stat_name, amount=1):
            if self.available_skillpoints is not None:
                if self.available_skillpoints > 0 and self.stats[stat_name].increment(amount):
                    self.available_skillpoints -= 1
            else:
                self.stats[stat_name].increment(amount)


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


        def get_base(self):
            """Returns the base value of the stat"""
            return self.base


        def check(self, threshold):
            """Makes a dice-roll check against this stat, then returns True for success, False for fail"""
            rolls = [random.randint(0, self.sides) for d in range(self.num_dice)]

            return sum(rolls) >= threshold


        def passive_check(self, threshold):
            """Checks stat base value against threshold, then returns True for success, False for fail"""
            return self.get_base() >= threshold


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



    def define_stat(name, base=0, dice=0, sides=0, minimum=None, maximum=None):
        return stat(name, base, dice, sides, minimum, maximum)


    def define_stat_set(dice=0, sides=0, minimum=None, maximum=None, *stat_names, **stat_values):
        return stat_set(dice, sides, minimum, maximum, stat_names, stat_values)


# Call this label to show the player a screen that lets them assign skill points to their stats
# Parameters:
#   - stat_set - the set of stats to customize
#   - points - the number of skills points available
#   - locking - set to "True" to prevent the player from reassigning skillpoints they have already assigned
#   - use_it_or_lose_it - set to "True" to throw out leftover skill points once the player exits the screen
#                       - "False" allows player to bank skill points for future use
label customize_stats(stat_set, points, locking=True, use_it_or_lose_it=False):
    $ stat_set.allot_skillpoints(points)
    show screen customize_stats(stat_set)

    if locking:
        $ stat_set.lock()
    if use_it_or_lose_it:
        $ stat_set.clear_skillpoints()
    return

# Call this label to make a skill check
# Parameters:
#   - stat_name - the name of the stat being checked
#   - threshold - Score equal to or higher than this number to succeed
#   - on_success - the name of the label to call on a successful role, can be None
#   - on_failure - the name of the label to call on a failed role, can be None
#   - passive - set to "True" to check against the stat's base value, without rolling
# Return:
#   - "True" if the check was successful, "False" otherwise
label skill_check(stat_name, threshold, on_success=None, on_failure=None, passive=False):
    $ success = check(stat_name, threshold, passive)
    if success and on_success is not None:
        call expression on_success
    elif not success and on_failure is not None:
        call expression on_failure
    return success


# Display the stats as a sidebar
screen stats_sidebar(stats):
    frame:
        xalign 1.0
        yalign 0.0
        use display_stats(stats)


# Displays the stats, intended for use inside other screens
screen display_stats(stats):                  
    vbox:
        vbox:
            for s in stats.stats.values():
                hbox:                                                 
                    text s.name
                    text (" %d" % (s.base,)) xalign 1.0


# A screen to let the player assign skillpoints to their stats
# Intended to be used by the 
screen customize_stats(stats):
    modal True
    sensitive True
    zorder 10
    tag menu
    add gui.game_menu_background
    frame:
        xalign 0.5
        yalign 0.5
        xmargin 20
        ymargin 20
        xfill True
        yfill True
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.1
            text "Customize your stats" yalign 0.1 xalign 0.5
            if stats.available_skillpoints is not None:
                text ("Points remaining: %d" % stats.available_skillpoints) yalign 0.1 xalign 0.5

            hbox:
                spacing 100
                xalign 0.5
                for s_name, s in stats.stats.items():
                    vbox:                                                 
                        text s_name
                        hbox:
                            xalign 0.5
                            textbutton "-" action Function(stats.decrement, s_name)
                            text (" %d " % (s.base))
                            textbutton "+" action Function(stats.increment, s_name)
            hbox:
                xalign 0.5
                textbutton "Done" action Hide()

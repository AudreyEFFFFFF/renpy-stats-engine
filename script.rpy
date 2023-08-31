# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")

init python:   
    CHA = "charisma"
    STR = "strength"
    INT = "intelligence"
    my_stats = define_stat_set(2, 6, None, None, CHA, STR, INT)


label start:

    scene bg room

    call customize_stats(my_stats, 6)

    show screen stats_sidebar(my_stats)

    "Making a [CHA] check."

    $ success = my_stats.check(CHA, 7)

    if success:
        "Check successful"
    else:
        "Check failed"


    "Making an easy [CHA] check."

    $ success = my_stats.check(CHA, 0)

    if success:
        "Check successful"
    else:
        "Check failed"


    "Making a hard [CHA] check."

    $ success = my_stats.check(CHA, 12)

    if success:
        "Check successful"
    else:
        "Check failed"
        

    "Making an impossible [CHA] check."

    $ success = my_stats.check(CHA, 13)

    if success:
        "Check successful"
    else:
        "Check failed"


    return

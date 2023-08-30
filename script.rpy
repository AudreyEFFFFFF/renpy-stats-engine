# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")

init python:   
    CHA = "charisma"
    STR = "strength"
    INT = "intelligence"
    my_stats = define_stat_set(2, 6, CHA, STR, INT)
    cha = define_stat("charisma", 0, 2, 6)


label start:

    scene bg room

    show screen customize_stats(my_stats)

    show screen stats_sidebar(my_stats)

    "Making a [CHA] check."

    $ check = my_stats.check(CHA, 7)

    if check:
        "Check successful"
    else:
        "Check failed"


    "Making an easy [CHA] check."

    $ check = my_stats.check(CHA, 0)

    if check:
        "Check successful"
    else:
        "Check failed"


    "Making a hard [CHA] check."

    $ check = my_stats.check(CHA, 12)

    if check:
        "Check successful"
    else:
        "Check failed"
        

    "Making an impossible [CHA] check."

    $ check = my_stats.check(CHA, 13)

    if check:
        "Check successful"
    else:
        "Check failed"


    return

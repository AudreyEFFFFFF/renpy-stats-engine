# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")

init python:
    cha = define_stat("charisma", 0, 2, 6)


label start:

    scene bg room

    $check = cha.check(6)

    if check:
        "Check successful"
    else:
        "Check failed"


    return

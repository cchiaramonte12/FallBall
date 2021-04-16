#  Cameron Chiaramonte (ccc7sej)
#  Michael Richwine (mnr2cwc)

import pygame
import gamebox
import random

game_on = False

camera = gamebox.Camera(800, 600)

ball = gamebox.from_image(400, 200, "ball.png")
ball.size = [30, 30]

x_coord1 = random.randint(0, 600)
x_coord2 = random.randint(0, 600)
x_coord3 = random.randint(0, 600)
x_coord4 = random.randint(0, 600)

walls = [gamebox.from_color(x_coord1, 100, "#F10AD8", 700, 20),
         gamebox.from_color(x_coord1 + 800, 100, "#F10AD8", 700, 20),
         gamebox.from_color(x_coord2, 300, "#F10AD8", 700, 20),
         gamebox.from_color(x_coord2 + 800, 300, "#F10AD8", 700, 20),
         gamebox.from_color(x_coord3, 500, "#F10AD8", 700, 20),
         gamebox.from_color(x_coord3 + 800, 500, "#F10AD8", 700, 20),
         gamebox.from_color(x_coord4, 700, "#F10AD8", 700, 20),
         gamebox.from_color(x_coord4 + 800, 700, "#F10AD8", 700, 20)]

coins = [gamebox.from_image(300, 300, "coin.png")]
for coin in coins:
    coin.size = [20, 20]

coin_counter = 0

ceiling = gamebox.from_color(400, camera.y - 300, "black", 1000, 1)

game = gamebox.from_text(camera.x, 250, "Fall-Ball", 35, "Red")
start = gamebox.from_text(camera.x, 400, "Press Space to Begin", 24, "Green")
names = gamebox.from_text(camera.x, 350, "Cameron Chiaramonte (ccc7sej), Michael Richwine (mnr2cwc)", 24, "white")
instructions = gamebox.from_text(camera.x, 375, "Use Left and Right Arrows to move the ball.  Don't let the top of the"
                                                "screen catch you!", 24, "Blue")

score = 0

ticks = 10000

score_partial = 0


def tick(keys):
    """
    This game is a ball that is moved only left or right with arrow keys and the goal is
    to get it to go though a narrow gap in bars that go across the screen.
    This will be a scrolling level game with a background that moves up the screen since the ball
    will constantly be falling downwards.  If the top of the screen touches the ball then the game is over.
    The bars that go across the screen will have their gap be the same size every time but randomly placed
    as the ball falls down.  There will be a timer in the top right corner going up that denotes score.
    In addition there will be coins to pick up with a coin counter.
    These coins will not benefit the score of the player but rather will act
    as a distraction because the player will attempt to get coins and lose track of how close they are getting
    to the top of the screen.  The ball will be allowed to wrap from side to side.
    The levels will go continuously there will be no stop to get to the next level.  Levels are denoted by a change in
    color of the bars as well as a gradual increase in speed of the level.
    :param keys: This is the user input.
    :return: This function returns nothing.
    """

    global game_on, score, score_partial, coin_counter, ticks

    camera.clear("black")

    ticks -= 1

    if game_on is False and score != 0:
        camera.draw(gamebox.from_text(camera.x, 100, "Game Over! Score: " + str(score), 40, "black", bold=False))
        if pygame.K_SPACE in keys:
            for wall in walls:
                wall.y += 300
                ball.y += 20
                wall.color = "#F10AD8"
            for coin in coins:
                coin.y += 300
            score = 0
            coin_counter = 0
            game_on = True

    if game_on is False:
        camera.draw(game)
        camera.draw(names)
        camera.draw(start)
        camera.draw(instructions)
        if pygame.K_SPACE in keys:
            game_on = True

    if game_on:
        n = 20
        for i in range(n):
            ball.y += .05
            ball.yspeed += .05
            for wall in walls:
                if ball.bottom_touches(wall):
                    ball.move_to_stop_overlapping(wall)
                    ball.yspeed = 0
        ball.y = ball.y + ball.yspeed-1

    for wall in walls:
        if ball.bottom_touches(wall):
            ball.move_to_stop_overlapping(wall)
            ball.yspeed = 0
        if wall.y <= camera.y-400:
            wall.y = camera.y+400
        camera.draw(wall)

    if pygame.K_LEFT in keys and game_on:
        ball.x -= 12
    if pygame.K_RIGHT in keys and game_on:
        ball.x += 12

    if game_on:
        camera.y += 6 + score/25
        ball.y += 3
        score_partial += 1
        if score_partial % 30 == 0:
            score += 1

    if ball.x > 800:
        ball.x = 0
    if ball.x < 0:
        ball.x = 800

    for coin in coins:
        if ball.touches(coin):
            coin_counter += 1
            coins.remove(coin)
        camera.draw(coin)
        for wall in walls:
            coin.move_to_stop_overlapping(wall)

    if game_on is True and ticks % ticks_per_second == 0:
        coin_x = random.randint(50, 750)
        for wall in walls:
            coin_y = wall.y
        coins.append(gamebox.from_image(coin_x, coin_y, "coin.png"))
        for coin in coins:
            coin.size = [20, 20]

    for wall in walls:
        if score >= 25:
            wall.color = '#EB1212'
        if score >= 50:
            wall.color = '#D312EB'
        if score >= 75:
            wall.color = '#ECF009'
        if score >= 100:
            wall.color = '#FF9600'
        if score >= 125:
            wall.color = '#82FF00'
        if score >= 150:
            wall.color = '#00FFF3'
        if score >= 175:
            wall.color = '#00FF79'
        if score >= 200:
            wall.color = '#FF0000'
        if score >= 225:
            wall.color = '#0014FF'
        if score >= 250:
            wall.color = '#9600FF'

    if ball.y >= camera.y + 300:
        ball.yspeed = 0
    if ball.y < camera.y - 300:
        ball.yspeed = 0
        camera.draw(gamebox.from_text(400, camera.y, "Game Over! Score: " + str(score), 40, "white", bold=False))
        game_on = False
        camera.draw(ceiling)

    camera.draw(gamebox.from_text(700, camera.y - 275, "Score: " + str(score), 40, "white", bold=True))
    camera.draw(gamebox.from_text(65, camera.y - 245, str(coin_counter), 40, "white", bold=True))
    camera.draw(gamebox.from_text(65, camera.y - 275, "Coins", 40, "white", bold=True))
    camera.draw(ball)
    camera.display()


ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)

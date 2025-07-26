import math  # type: ignore
from time import time  # type: ignore

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
# from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore

def doPassNearAllly(field: fld.Field, actions: list[Action], idFrom = const.GK):
    points = field.active_allies()
    exclude = [field.allies[idFrom].get_pos()]
    pointFrom = exclude.get_pos()
    enemys = field.active_enemies()
    pointToPass = -1

    maybePassPoints = fld.find_nearest_robots(pointFrom, points, avoid=exclude)
    for nearestR in maybePassPoints:
        maybePassPoint = nearestR.get_pos()
        for enemyR in enemys:
            if aux.dist(aux.closest_point_on_line(pointFrom, maybePassPoint, enemyR.get_pos()), enemyR.get_pos()) < 200:
                break
        else:
            rToPass = nearestR
            pointToPass = maybePassPoint
            break

    if pointToPass != -1:
        """if enemy r dont prevent pass """
        actions[idFrom] =  Actions.Kick(pointToPass, is_pass=True)# do checking enemy
        actions[rToPass.r_id] = Actions.BallGrab(field.allies[idFrom]-field.allies[idFrom].get_pos().arg())
    # else: # consider this case

def GK(field: fld.Field, actions: list[Action]):
    field.allies[const.GK].set_dribbler_speed(0)

    oldBallPos = field.ball_start_point
    ballPos = field.ball.get_pos()
    GKPos = field.allies[const.GK].get_pos()

    nearestEnemyRToBall = fld.find_nearest_robot(ballPos, field.active_enemies())
    enemyRGrabBall = field.is_ball_in(nearestEnemyRToBall)

    if field.is_ball_moves_to_goal() and not enemyRGrabBall:
        if not aux.is_point_on_line(GKPos, oldBallPos, ballPos, "R"):
            """ intersept ball"""
            interseptBallPoint = aux.closest_point_on_line(oldBallPos, ballPos, GKPos, "R")
            actions[const.GK] = Actions.GoToPoint(interseptBallPoint)
        else:
            """grab intersepted ball and pass nearly ally"""
            # actions[const.GK] = Actions.BallGrab((ballPos-GKPos).arg)
            doPassNearAllly(field, actions)
    # elif field.is_ball_in(field.allies[const.GK]):
    #     """"""
    #     doPassNearAllly(field, actions)
    else:
        # if enemyRGrabBall:
        """block maybe kick"""
        pointForGK = aux.nearest_point_in_poly(ballPos, field.ally_goal.hull)
        actions[const.GK] = Actions.GoToPoint(pointForGK, (ballPos-GKPos).arg)
        field.allies[const.GK].set_dribbler_speed(1)
        # else:

# def attacker(field: fld.Field, actions: list[Action], idx):
    
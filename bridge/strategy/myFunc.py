import math  # type: ignore
from time import time  # type: ignore

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
# from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore

def doPassNearAllly(field: fld.Field, actions: list[Action], idFrom = const.GK):
    points = field.allies
    exclude = field.allies[idFrom]
    pointFrom = exclude.get_pos()
    pointToPass = points[0]
    min_dist = 10e10
    for _, point in enumerate(points):
        if point in exclude:
            continue
        if aux.dist(pointFrom, point) < min_dist:
            min_dist = aux.dist(pointFrom, point)
            pointToPass = point
    actions[idFrom] =  Actions.Kick(pointToPass, is_pass=True)# do checking enemy


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
            """grab intersepted ball"""
            actions[const.GK] = Actions.BallGrab((ballPos-GKPos).arg)
    elif field.is_ball_in(field.allies[const.GK]):
        doPassNearAllly(field, actions)
    else:
        if enemyRGrabBall:
            """block maybe kick"""
            pointForGK = aux.nearest_point_in_poly(ballPos, field.ally_goal.hull)
            actions[const.GK] = Actions.GoToPoint(pointForGK, (ballPos-GKPos).arg)
            field.allies[const.GK].set_dribbler_speed(1)
        # else:
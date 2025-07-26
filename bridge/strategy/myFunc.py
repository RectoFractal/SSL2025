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
        actions[idFrom] =  Actions.Kick(pointToPass, is_pass=True)
        if not field.is_ball_in(field.allies[idFrom]):
            """getting a pass"""
            actions[rToPass.r_id] = Actions.BallGrab(field.allies[idFrom]-field.allies[idFrom].get_pos().arg())
    # else: # consider this case

def GK(field: fld.Field, actions: list[Action]):# do consider ball
    field.allies[const.GK].set_dribbler_speed(0)

    oldBallPos = field.ball_start_point
    ballPos = field.ball.get_pos()
    GKPos = field.allies[const.GK].get_pos()

    nearestEnemyRToBall = fld.find_nearest_robot(ballPos, field.active_enemies())
    enemyRGrabBall = field.is_ball_in(nearestEnemyRToBall)

    if field.is_ball_moves_to_goal() and not enemyRGrabBall:
        if not aux.is_point_on_line(GKPos, oldBallPos, ballPos, "R"):
            interseptBallPoint = aux.closest_point_on_line(oldBallPos, ballPos, GKPos, "R")
            if interseptBallPoint != ballPos:
                """ intersept ball"""
                actions[const.GK] = Actions.GoToPoint(interseptBallPoint)
            else:
                """grab ball if it maybe in hull and we cant intersept him"""
                actions[const.GK] = Actions.BallGrab((ballPos-GKPos).arg())
        else:
            """grab intersepted ball and pass nearly ally"""
            # actions[const.GK] = Actions.BallGrab((ballPos-GKPos).arg)
            doPassNearAllly(field, actions)
    # elif field.is_ball_in(field.allies[const.GK]):
    #     """"""
    #     doPassNearAllly(field, actions)
    elif aux.is_point_inside_poly(ballPos, field.ally_goal.hull):
        """knock out the ball from hull"""
        doPassNearAllly(field, actions)
    else:
        # if enemyRGrabBall:
        """block maybe kick"""
        pointForGK = aux.nearest_point_in_poly(ballPos, field.ally_goal.hull)
        actions[const.GK] = Actions.GoToPoint(pointForGK, (ballPos-GKPos).arg)
        field.allies[const.GK].set_dribbler_speed(1)
        # else:

def findPointForScore(field: fld.Field, pointFrom):#WORK!!!
    """
    Find the nearest point to a given point (center) from a list, optionally excluding some points.

    Args:
        center (Point): The reference point.
        points (list[Point]): The list of candidate points.
        exclude (Optional[list[Point]]): Points to ignore during the search (default is None).

    Returns:
        Point: The closest point to `center` that is not in `exclude`.
    """
    qPoint = 10
    d = field.enemy_goal.up.y - field.enemy_goal.down.y
    points = [aux.Point(field.enemy_goal.up.x, field.enemy_goal.up.y-(d/qPoint*i)) for i in range(1, qPoint)]
    enemys = field.active_enemies(True)
    closest = None
    min_dist = 10e10
    for _, point in enumerate(points):
        if aux.dist(pointFrom, point) < min_dist:
            if all(len(aux.line_circle_intersect(pointFrom, point, enemyR.get_pos(), const.ROBOT_R*1.2, "S")) == 0 for enemyR in enemys):
                """if noone enemy r prevent this kick"""
                min_dist = aux.dist(pointFrom, point)
                closest = point
    return closest
    if closest != None:
        field.strategy_image.draw_line(pointFrom, closest, color=(0, 255, 0))
    else:
        field.strategy_image.draw_circle(pointFrom, color=(0, 0, 0), size_in_mms=100)

def attacker(field: fld.Field, actions: list[Action], idx):
    enemys = field.active_enemies(True)
    allies = field.allies
    thisR = allies[idx]
    if actions[idx] == None:
        # print(1)
        """if we dont send command on this robot"""
        allR = enemys.copy() + allies.copy()
        nearestRToBall = fld.find_nearest_robot(field.ball.get_pos(), allR)
        if nearestRToBall == thisR:
            # print(2)
            """if nearest to ball bot this"""
            if field.is_ball_in(thisR):
                # print(3)
                """if this robot have ball"""
                pointForScore = findPointForScore(field, thisR.get_pos())
                if pointForScore != None:
                    # print(4)
                    """try do score if r can"""
                    actions[idx] = Actions.Kick(pointForScore)
                else:
                    """do pass or come closer to enemy goal"""
            else:
                actions[idx] = Actions.BallGrab((field.enemy_goal.center - field.ball.get_pos()).arg())  
        else:
            """if nearest R our open for pass"""
            """if nearest R enenmy intersept maybe pass or try take ball"""
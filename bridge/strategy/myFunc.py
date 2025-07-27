import math  # type: ignore
from time import time  # type: ignore

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
# from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore

def doPassNearAllly(field: fld.Field, actions: list[Action], Strategy, idFrom = const.GK):
    points = field.active_allies()
    exclude = [idFrom]
    pointFrom = field.allies[idFrom].get_pos()
    enemys = field.active_enemies()
    pointToPass = None

    maybePassPoints = fld.find_nearest_robot(pointFrom, points, avoid=exclude)
    nearestR = maybePassPoints
    # for nearestR in maybePassPoints:
    maybePassPoint = nearestR.get_pos()
    for enemyR in enemys:
        if aux.dist(aux.closest_point_on_line(pointFrom, maybePassPoint, enemyR.get_pos()), enemyR.get_pos()) < 200:
            break
    else:
        rToPass = nearestR
        pointToPass = maybePassPoint
        # break

    if pointToPass != None:
        """if enemy r dont prevent pass """
        field.strategy_image.send_telemetry("status pass", "have point")
        # field.strategy_image.draw_line(pointFrom, pointToPass, color=(255, 0, 0))
        field.strategy_image.draw_circle(pointToPass, color=(255, 0, 0), size_in_mms=1000)
        actions[idFrom] =  Actions.Kick(pointToPass, is_pass=True)
        if not field.is_ball_in(field.allies[idFrom]):
            """getting a pass"""
            Strategy.idGettingPass = rToPass.r_id
            # actions[rToPass.r_id] = Actions.BallGrab(field.allies[idFrom]-field.allies[idFrom].get_pos().arg())
    else:
        field.strategy_image.send_telemetry("status pass", "dont have point")
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
            if all(len(aux.line_circle_intersect(pointFrom, point, enemyR.get_pos(), const.ROBOT_R*1.5, "S")) == 0 for enemyR in enemys):
                """if noone enemy r prevent this kick"""
                min_dist = aux.dist(pointFrom, point)
                closest = point
    if closest != None:
        field.strategy_image.draw_line(pointFrom, closest, color=(0, 255, 0))
    else:
        field.strategy_image.draw_circle(pointFrom, color=(0, 0, 0), size_in_mms=100)
    return closest

def attacker(field: fld.Field, actions: list[Action], idxThisR, idxOtherAttacker):
    enemys = field.active_enemies(True)
    allies = field.allies
    thisR = allies[idxThisR]
    otherAttackerR = allies[idxOtherAttacker]
    if actions[idxThisR] == None:
        """if we dont send command on this robot"""
        allR = enemys.copy() + allies.copy()
        nearestRToBall = fld.find_nearest_robot(field.ball.get_pos(), allR)
        if nearestRToBall == thisR:
            """if nearest to ball bot this"""
            if field.is_ball_in(thisR):
                """if this robot have ball"""
                pointForScore = findPointForScore(field, thisR.get_pos())
                if pointForScore != None:
                    """try do score if r can"""
                    field.strategy_image.send_telemetry("status", "try do score if r can")
                    actions[idxThisR] = Actions.Kick(pointForScore)
                else:
                    pointForScoreForOtherAttacker = findPointForScore(field, otherAttackerR.get_pos())
                    if pointForScoreForOtherAttacker != None:
                        doPassNearAllly(field, actions, idxThisR)
                        field.strategy_image.send_telemetry("status", "do pass or come closer to enemy goal")
                    """do pass or come closer to enemy goal"""
                    # DONT DONE
            else:
                """if this r is nearest to ball, but dont grab him, grab ball"""
                field.strategy_image.send_telemetry("status", "if this r is nearest to ball, but dont grab him, grab ball")
                actions[idxThisR] = Actions.BallGrab((field.ball.get_pos() - thisR.get_pos()).arg())  
        else:
            field.strategy_image.send_telemetry("status", "if nearest R our open for pass")
            # DONT DONE
            """if nearest R our open for pass"""
            """if nearest R enenmy intersept maybe pass or try take ball, depend from dist"""
import math  # type: ignore
from time import time  # type: ignore

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
# from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore

def goToNearestScorePoint(field: fld.Field, actions: list[Action], idFrom: int, idOtherAttacker: int | None):
    field.allies[idFrom].set_dribbler_speed(15)
    rCircle = 1100
    thisR = field.allies[idFrom]
    enemysGoalCenter = field.enemy_goal.center
    if idOtherAttacker != None:
        aimForLookPos = field.allies[idOtherAttacker].get_pos()
    else:
        aimForLookPos = enemysGoalCenter
    # field.strategy_image.draw_circle(enemysGoalCenter, (255, 255, 255), 1000)
    pointsForScore = []
    # if aux.is_point_inside_circle(thisR.get_pos(), enemysGoalCenter, rCircle+150):
    # vectFromCenterToR = (thisR.get_pos()-enemysGoalCenter)
    vectFromCenterToR = field.enemy_goal.eye_forw*rCircle
    # field.strategy_image.draw_line(vectFromCenterToR, enemysGoalCenter)
    for angel in range(-180, 180+1, 10):
        angelInRad = angel/180*math.pi
        maybeScorePoint = aux.rotate(vectFromCenterToR, angelInRad)+enemysGoalCenter
        argVectFromCenterToMaybeScorePoint = aux.wind_down_angle((maybeScorePoint-enemysGoalCenter).arg())
        if field.polarity == 1:
            # field.strategy_image.draw_circle(thisR.get_pos(), size_in_mms=500)
            
            # print(aux.wind_down_angle(maybeScorePoint.arg()))
            if -math.pi/2 >= argVectFromCenterToMaybeScorePoint or argVectFromCenterToMaybeScorePoint >= math.pi/2:
                continue
        else:
            if -math.pi/2 <= argVectFromCenterToMaybeScorePoint <= math.pi/2:
                continue
        field.strategy_image.draw_circle(maybeScorePoint)
        pointForScore = findPointForScore(field, maybeScorePoint)
        # field.strategy_image.draw_line(maybeScorePoint, enemysGoalCenter, (200, 0, 0), 100)
        # field.strategy_image.draw_line(pointForScore, enemysGoalCenter)
        if pointForScore != None:
            pointsForScore.append(maybeScorePoint)
            field.strategy_image.draw_circle(maybeScorePoint)
            # field.strategy_image.draw_line(maybeScorePoint, enemysGoalCenter, (200, 0, 0), 100)
    nearestScorePoint = aux.find_nearest_point(thisR.get_pos(), pointsForScore)
    field.strategy_image.draw_circle(nearestScorePoint, (0, 0, 255), 50)
    actions[idFrom] = Actions.GoToPoint(nearestScorePoint, (aimForLookPos-thisR.get_pos()).arg())
    # else:
    #     nearestPoint = aux.nearest_point_on_circle(thisR.get_pos(), enemysGoalCenter, rCircle)
    #     actions[idFrom] = Actions.GoToPoint(nearestPoint, (aimForLookPos-thisR.get_pos()).arg())


def openForPass(field: fld.Field, idRWhichOpen: int, actions: list[Action]):
    field.allies[idRWhichOpen].set_dribbler_speed(0)
    ballPos = field.ball.get_pos()
    # enemysR = field.enemies
    enemysR = field.active_enemies(True)
    rPos = field.allies[idRWhichOpen].get_pos()
    rWhichPreventPass = None
    pointToGo = None
    vectFromRToBall = ballPos - rPos
    for enemyR in enemysR: # NORM CODE
        if len(aux.line_circle_intersect(ballPos, rPos, enemyR.get_pos(), const.ROBOT_R, "S")) != 0:
            rWhichPreventPass = enemyR
            field.strategy_image.draw_circle(enemyR.get_pos(), (0, 255, 200), 50)
    # if len(aux.line_circle_intersect(ballPos, rPos, enemysR[3].get_pos(), const.ROBOT_R, "S")) != 0: # HARD CODE!!!
    #     rWhichPreventPass = enemysR[3]
    if rWhichPreventPass != None:
        # if aux.get_angle_between_points(rWhichPreventPass.get_pos(), ballPos, rPos) > 0:
        vectL = aux.rotate(vectFromRToBall.unity(), -math.pi/2)
        pointToGoL = vectL*700 + rPos
        if pointToGoL.x*field.polarity > 0:
            pointToGoL = aux.rotate(vectL, math.pi)*700 + rPos

        vectR = aux.rotate(vectFromRToBall.unity(), math.pi/2)
        pointToGoR = vectR*700 + rPos
        if pointToGoR.x*field.polarity > 0:
            pointToGoR = aux.rotate(vectR, math.pi)*700 + rPos

        futurePointL = vectL*700*2 + rPos
        futurePointR = vectR*700*2 + rPos
        field.strategy_image.draw_circle(futurePointL, (255, 0, 0))
        field.strategy_image.draw_circle(futurePointR, (0, 255, 0))
        weAreOpenInFutureL = all((len(aux.line_circle_intersect(futurePointL, rPos, enemyR.get_pos(), const.ROBOT_R*1.2, "S")) != 0) for enemyR in enemysR)
        weAreOpenInFutureR = all((len(aux.line_circle_intersect(futurePointR, rPos, enemyR.get_pos(), const.ROBOT_R*1.2, "S")) != 0) for enemyR in enemysR)
        # print(weAreOpenInFutureL)
        if aux.dist(pointToGoL, field.enemy_goal.center) < aux.dist(pointToGoR, field.enemy_goal.center):
            """open to left"""
            if not weAreOpenInFutureL and not weAreOpenInFutureR:
                if aux.is_point_inside_poly(futurePointL, field.hull):
                    pointToGo = pointToGoL
                else:
                    pointToGo = pointToGoR
            else:
                if not weAreOpenInFutureL:
                    pointToGo = pointToGoL
                else:
                    pointToGo = pointToGoR
        else:
            """open to right"""
            if not weAreOpenInFutureL and not weAreOpenInFutureR:
                if aux.is_point_inside_poly(futurePointR, field.hull):
                    pointToGo = pointToGoR
                else:
                    pointToGo = pointToGoL
            else:
                if not weAreOpenInFutureR:
                    pointToGo = pointToGoR
                else:
                    pointToGo = pointToGoL
        field.strategy_image.draw_line(pointToGo, rPos, (255, 255, 255), 20)
        actions[idRWhichOpen] = Actions.GoToPoint(pointToGo, (ballPos-pointToGo).arg())
        # field.allies[idRWhichOpen].set_dribbler_speed(1)
    else:
        field.strategy_image.draw_circle(rPos, (0, 0, 0), 50)
        # actions[idRWhichOpen] = Actions.GoToPoint(rPos, (ballPos-rPos).arg())
        actions[idRWhichOpen] = Actions.BallGrab((ballPos-rPos).arg())

def getPointToPassAndRToPass(field: fld.Field, actions, maybePassPoints, enemys, pointFrom, idFrom = const.GK):
    rToPass = None
    pointToPass = None
    if idFrom != const.GK:
        nearestR = maybePassPoints
        # for nearestR in maybePassPoints:
        maybePassPoint = nearestR.get_pos()

        for enemyR in enemys:
            if aux.dist(aux.closest_point_on_line(pointFrom, maybePassPoint, enemyR.get_pos()), enemyR.get_pos()) < 200:
                break
        else:
            rToPass = nearestR
            pointToPass = maybePassPoint
        if rToPass == None:
            openForPass(field, nearestR.r_id, actions)

    else:
        for nearestR in maybePassPoints:
            if nearestR == field.allies[const.GK]:
                field.strategy_image.draw_circle(field.allies[const.GK].get_pos(), (0, 200, 255), 50)
                continue
            maybePassPoint = nearestR.get_pos()

            for enemyR in enemys:
                if aux.dist(aux.closest_point_on_line(pointFrom, maybePassPoint, enemyR.get_pos()), enemyR.get_pos()) < 200:
                    break
            else:
                rToPass = nearestR
                pointToPass = maybePassPoint
                break
        if rToPass == None:
            openForPass(field, maybePassPoints[0].r_id, actions)
    return [rToPass, pointToPass]

def doPassNearAllly(field: fld.Field, actions: list[Action], idFrom = const.GK):
    points = field.active_allies()
    exclude = [idFrom]
    # pointFrom = field.allies[idFrom].get_pos()
    pointFrom = field.ball.get_pos()
    enemys = field.active_enemies()
    pointToPass = None
    rToPass = None

    if len(points) != 0:
        if idFrom == const.GK:
            maybePassPoints = fld.find_nearest_robots(pointFrom, points)
            # maybePassPoints = maybePassPoints.remove(field.allies[idFrom])
        else:
            maybePassPoints = fld.find_nearest_robot(pointFrom, points, avoid=exclude)
        
        rToPass, pointToPass = getPointToPassAndRToPass(field, actions, maybePassPoints, enemys, pointFrom, idFrom)

        if pointToPass != None:
            """if enemy r dont prevent pass """
            field.strategy_image.send_telemetry("status pass", "have point")
            # field.strategy_image.draw_line(pointFrom, pointToPass, color=(255, 0, 0))
            # field.strategy_image.draw_circle(pointToPass, color=(255, 0, 0), size_in_mms=1000)
            actions[idFrom] =  Actions.Kick(pointToPass, is_pass=True)
        else:
            field.strategy_image.send_telemetry("status pass", "dont have point")
    if rToPass != None:
        return rToPass.r_id
    else:
        return None
    # else: # consider this case

def GK(field: fld.Field, actions: list[Action], oldGKState):
    GKState = None

    field.allies[const.GK].set_dribbler_speed(0)

    oldBallPos = field.ball_start_point
    ballPos = field.ball.get_pos()
    GKPos = field.allies[const.GK].get_pos()
    enenmies = field.active_enemies().copy()
    allies = field.active_allies(True).copy()
    allR = enenmies+allies

    nearestEnemyRToBall = fld.find_nearest_robot(ballPos, field.active_enemies())
    nearestRToBall = fld.find_nearest_robot(ballPos, allR)
    # field.strategy_image.draw_circle(nearestRToBall.get_pos(), color=(0, 255, 0), size_in_mms=50)
    enemyRGrabBall = field.is_ball_in(nearestEnemyRToBall)

    if nearestRToBall == field.allies[const.GK] and oldGKState != "Intersept":
        # field.strategy_image.send_telemetry("GK State", "Pass")
        GKState = "Pass"
        doPassNearAllly(field, actions)
    elif field.is_ball_moves_to_goal() and not enemyRGrabBall:
        if not aux.is_point_on_line(GKPos, oldBallPos, ballPos, "R"):
            interseptBallPoint = aux.closest_point_on_line(oldBallPos, ballPos, GKPos, "R")
            field.strategy_image.draw_circle(interseptBallPoint, color=(255, 0, 0), size_in_mms=50)
            # field.strategy_image.draw_line(GKPos, interseptBallPoint, color=(0, 0, 200), size_in_pixels=20)
            if interseptBallPoint != ballPos:
                # field.strategy_image.send_telemetry("GK State", "Intersept")
                GKState = "Intersept"
                """ intersept ball"""
                actions[const.GK] = Actions.GoToPointIgnore(interseptBallPoint, (ballPos-interseptBallPoint).arg())
            else:
                GKState = "Grab ball"
                # field.strategy_image.send_telemetry("GK State", "Grab ball")
                """grab ball if it maybe in hull and we cant intersept him"""
                actions[const.GK] = Actions.BallGrab((ballPos-GKPos).arg())
        else:
            GKState = "Pass interstpted ball"
            # field.strategy_image.send_telemetry("GK State", "Pass interstpted ball")
            """grab intersepted ball and pass nearly ally"""
            # actions[const.GK] = Actions.BallGrab((ballPos-GKPos).arg)
            doPassNearAllly(field, actions)
    # elif field.is_ball_in(field.allies[const.GK]):
    #     """"""
    #     doPassNearAllly(field, actions)
    elif aux.is_point_inside_poly(ballPos, field.ally_goal.hull):
        GKState = "Knock out ball"
        # field.strategy_image.send_telemetry("GK State", "Knock out ball")
        """knock out the ball from hull"""
        doPassNearAllly(field, actions)
    else:
        GKState = "block maybe kick"
        # field.strategy_image.send_telemetry("GK State", "Block maybe kick")
        # if enemyRGrabBall:
        """block maybe kick"""
        # pointForGK = aux.nearest_point_on_poly(ballPos, field.ally_goal.hull)
        mostLikelyPointForScore = aux.closest_point_on_line(field.ally_goal.up, field.ally_goal.down, ballPos)
        pointForGK = aux.segment_poly_intersect(ballPos, mostLikelyPointForScore, field.ally_goal.hull)
        field.strategy_image.draw_circle(pointForGK, color=(0, 0, 255), size_in_mms=50)
        # print(pointForGK)
        actions[const.GK] = Actions.GoToPointIgnore(pointForGK, (ballPos-GKPos).arg())
        field.allies[const.GK].set_dribbler_speed(15)
        # else:
    field.strategy_image.send_telemetry("GK State", GKState)
    return GKState

def findPointForScore(field: fld.Field, pointFrom = None, draw: bool = True):#WORK!!!
    """
    Find the nearest point to a given point (center) from a list, optionally excluding some points.

    Args:
        center (Point): The reference point.
        points (list[Point]): The list of candidate points.
        exclude (Optional[list[Point]]): Points to ignore during the search (default is None).

    Returns:
        Point: The closest point to `center` that is not in `exclude`.
    """
    if pointFrom == None:
        pointFrom = field.ball.get_pos()
    qPoint = 8
    qPoint +=2
    d = field.enemy_goal.up.y - field.enemy_goal.down.y
    points = [aux.Point(field.enemy_goal.up.x, field.enemy_goal.up.y-(d/qPoint*i)) for i in range(1, qPoint)]
    enemys = field.active_enemies(True)
    enemys = field.enemies
    closest = None
    min_dist = 10e10
    for _, point in enumerate(points):
        if aux.dist(pointFrom, point) < min_dist:
            if all(len(aux.line_circle_intersect(pointFrom, point, enemyR.get_pos(), const.ROBOT_R*1.5, "S")) == 0 for enemyR in enemys):
                """if noone enemy r prevent this kick"""
                min_dist = aux.dist(pointFrom, point)
                closest = point
    if draw:
        if closest != None:
            field.strategy_image.draw_line(pointFrom, closest, color=(0, 255, 0))
        else:
            field.strategy_image.draw_circle(pointFrom, color=(0, 0, 0), size_in_mms=100)
    return closest
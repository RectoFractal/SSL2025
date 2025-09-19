import math  # type: ignore
from time import time
from typing import Optional  # type: ignore

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
# from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore

#TODO do comments
def goToNearestScorePoint(field: fld.Field, actions: list[Optional[Action]], idFrom: int, idOtherAttacker: int | None) -> None:
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

#TODO do comments
def filterPointsForPass(field: fld.Field, points: list[aux.Point]) -> list[aux.Point]:
    filteredPointsForPass = []
    enemysR = field.active_enemies(True)
    ballPos = field.ball.get_pos()
    pointForScore = findPointForScore(field, ballPos)

    for maybePassPoint in points:
        rPreventPass = False
        for enemyR in enemysR:#depenf from distans from r to maybe pass point
            if aux.dist(enemyR.get_pos(), ballPos) < 100: 
                k = 1.0
            else:
                k = 1 + 0.15 * aux.dist(enemyR.get_pos(), ballPos)/const.ROBOT_R
            # if len(aux.line_circle_intersect(ballPos, maybePassPoint, enemyR.get_pos(), const.ROBOT_R*k, "S")) > 0:
            if aux.is_point_inside_circle(maybePassPoint, enemyR.get_pos(), const.ROBOT_R*k):
                rPreventPass = True
                field.strategy_image.draw_circle(enemyR.get_pos(), (0, 255, 200), const.ROBOT_R*k)
                field.strategy_image.draw_circle(maybePassPoint, (0, 0, 0))
        # field.strategy_image.draw_line(points, ballPos, (200, 0, 0), 100)
        # field.strategy_image.draw_line(pointForScore, ballPos) 
        distToEnemyHull = aux.dist(maybePassPoint, aux.nearest_point_in_poly(maybePassPoint, field.enemy_goal.hull))
        distToAllyHull = aux.dist(maybePassPoint, aux.nearest_point_in_poly(maybePassPoint, field.ally_goal.hull))
        if pointForScore != None:
            clPoint = aux.closest_point_on_line(ballPos, pointForScore, maybePassPoint)
            thisRPreventScore = aux.dist(clPoint, maybePassPoint) < 150
            if thisRPreventScore:
                field.strategy_image.draw_circle(maybePassPoint, (200, 0, 255))
        else:
            thisRPreventScore = False
        if rPreventPass == False and aux.is_point_inside_poly(maybePassPoint, field.hull) and distToEnemyHull > 150 and distToAllyHull > 150 and not thisRPreventScore:
            filteredPointsForPass.append(maybePassPoint)
            field.strategy_image.draw_circle(maybePassPoint, (0, 255, 0))
            # field.strategy_image.draw_line(points, ballPos, (200, 0, 0), 100)
    return filteredPointsForPass

#TODO do comments
def openForPass(field: fld.Field, idRWhichOpen: int, actions: list[Optional[Action]]) -> None:  
    ballPos = field.ball.get_pos()
    thisR = field.allies[idRWhichOpen]
    thisRPos = thisR.get_pos()
    maybePointsForOpening = []
    vectFromBallToR = thisRPos-ballPos
    vectFromBallToRUnity = vectFromBallToR.unity()
    step = 200
    for i in range(step, int(vectFromBallToR.mag()), step):
        maybePointsForOpening.append(ballPos+(vectFromBallToRUnity*i))
        # field.strategy_image.draw_circle(ballPos+(vectFromBallToRUnity*i))
    
    if vectFromBallToR.mag() < 700:
        vectFromBallToR = vectFromBallToRUnity * 700
    isBallOnOurPartOfField = ballPos.x*field.polarity > 0

    for angel in range(-180, 180+1, 10):
        angelInRad = angel/180*math.pi
        point = aux.rotate(vectFromBallToR, angelInRad)+ballPos
        maybePointsForOpening.append(point)
        # field.strategy_image.draw_circle(point)
        # pointForScore = findPointForScore(field, maybePassPoint)

    pointsForOpening = filterPointsForPass(field, maybePointsForOpening)
        
    # print(pointsForOpening, field.ball.get_pos())
    if len(pointsForOpening) != 0:
        if isBallOnOurPartOfField:
            nearestPointForOpening = aux.find_nearest_point(thisRPos, pointsForOpening)
        else:
            nearestPointForOpening = aux.find_nearest_point(field.enemy_goal.center, pointsForOpening)
        field.strategy_image.draw_circle(nearestPointForOpening, (0, 0, 255), 50)
        # field.strategy_image.draw_line(ballPos, nearestPointForOpening, (0, 0, 0), 20)
        actions[idRWhichOpen] = Actions.GoToPoint(nearestPointForOpening, (ballPos-thisR.get_pos()).arg())    

#TODO do comments
def getPointToPassAndRToPass(field: fld.Field, actions: list[Optional[Action]], maybePassPoints: list[rbt.Robot], enemys: list[rbt.Robot], pointFrom: aux.Point, idFrom: int = const.GK) -> tuple[rbt.Robot | None, aux.Point | None]:
    rToPass: Optional [rbt.Robot] = None
    pointToPass = None
    ballPos = field.ball.get_pos()
    if len(maybePassPoints) == 1:
        if len(enemys) == 0:
            rToPass = maybePassPoints[0]
            pointToPass = rToPass.get_pos()
        else:
            nearestR = maybePassPoints[0]
            # for nearestR in maybePassPoints:
            maybePassPoint = nearestR.get_pos()

            for enemyR in enemys:
                if aux.dist(enemyR.get_pos(), ballPos) < 100: 
                    k = 1.0
                else:
                    k = 1 + 0.15 * aux.dist(enemyR.get_pos(), ballPos)/const.ROBOT_R
                    if k > 15:
                        k = 1
                if aux.dist(aux.closest_point_on_line(pointFrom, maybePassPoint, enemyR.get_pos()), enemyR.get_pos()) < const.ROBOT_R*k:
                    break
            else:
                rToPass = nearestR
                pointToPass = maybePassPoint
            if rToPass == None:
                openForPass(field, nearestR.r_id, actions)

    else:
        if len(enemys) == 0:
            rToPass = maybePassPoints[0]
            pointToPass = rToPass.get_pos()
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
    return (rToPass, pointToPass)

def doPassNearAllly(field: fld.Field, actions: list[Optional[Action]], idFrom: int = const.GK) -> int | None:
    points = field.active_allies()
    exclude = [idFrom]
    # pointFrom = field.allies[idFrom].get_pos()
    pointFrom = field.ball.get_pos()
    enemys = field.active_enemies(True)
    pointToPass = None
    rToPass = None

    if len(points) != 0:
        if idFrom == const.GK:
            maybePassPoints = fld.find_nearest_robots(pointFrom, points)
            # maybePassPoints = maybePassPoints.remove(field.allies[idFrom])
        else:
            maybePassPoints = [fld.find_nearest_robot(pointFrom, points, avoid=exclude)]
        
        rToPass, pointToPass = getPointToPassAndRToPass(field, actions, maybePassPoints, enemys, pointFrom, idFrom)

        if pointToPass != None:
            """if enemy r dont prevent pass """
            field.strategy_image.send_telemetry("status pass", "have point")
            # field.strategy_image.draw_line(pointFrom, pointToPass, color=(255, 0, 0))
            # field.strategy_image.draw_circle(pointToPass, color=(255, 0, 0), size_in_mms=1000)
            actions[idFrom] =  Actions.Kick(pointToPass, is_pass=True)
        else:
            field.strategy_image.send_telemetry("status pass", "dont have point")
    if actions[idFrom] == None:
        actions[idFrom] = Actions.GoToPoint(field.allies[idFrom].get_pos(), (field.ball.get_pos()-field.allies[idFrom].get_pos()).arg())
    if rToPass != None:
        return rToPass.r_id
    else:
        return None
    # else: # consider this case

#TODO do comments
def GK(field: fld.Field, actions: list[Optional[Action]], oldGKState: str | None) -> str:#TODO change string variable on enum class
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
        if pointForGK != None:
            field.strategy_image.draw_circle(pointForGK, color=(0, 0, 255), size_in_mms=50)
            # print(pointForGK)
            actions[const.GK] = Actions.GoToPointIgnore(pointForGK, (ballPos-GKPos).arg())
            field.allies[const.GK].set_dribbler_speed(15)#TODO check in real
        else:
            """err"""
            print("ERROR IN GK")
    field.strategy_image.send_telemetry("GK State", GKState)
    return GKState

def findPointForScore(field: fld.Field, pointFrom: None | aux.Point = None, draw: bool = True, k: float = 1.5, reverse: bool = False) -> aux.Point | None:#TODO do comments
    if pointFrom == None:
        pointFrom = field.ball.get_pos()
    qPoint = 8
    qPoint +=2
    if not reverse:
        d = field.enemy_goal.up.y - field.enemy_goal.down.y
        points = [aux.Point(field.enemy_goal.up.x, field.enemy_goal.up.y-(d/qPoint*i)) for i in range(1, qPoint)]
        enemys = field.active_enemies(True)
    else:
        d = field.ally_goal.up.y - field.ally_goal.down.y
        points = [aux.Point(field.ally_goal.up.x, field.ally_goal.up.y-(d/qPoint*i)) for i in range(1, qPoint)]
        enemys = field.active_allies(True)
    # enemys = field.enemies
    closest = None
    min_dist = 10e10
    for _, point in enumerate(points):
        if aux.dist(pointFrom, point) < min_dist:
            if all(len(aux.line_circle_intersect(pointFrom, point, enemyR.get_pos(), const.ROBOT_R*k, "S")) == 0 for enemyR in enemys) or len(enemys) == 0:
                """if no one enemy r prevent this kick"""
                min_dist = aux.dist(pointFrom, point)
                closest = point
    if draw:
        if closest != None:
            field.strategy_image.draw_line(pointFrom, closest, color=(0, 255, 0))
        else:
            field.strategy_image.draw_circle(pointFrom, color=(0, 0, 0), size_in_mms=50)
    return closest

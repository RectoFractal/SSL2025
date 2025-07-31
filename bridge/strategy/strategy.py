"""High-level strategy code"""

# !v DEBUG ONLY
import math  # type: ignore
from bridge.strategy.myFunc import *
from time import time  # type: ignore
from typing import Optional

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore




class Strategy:
    """Main class of strategy"""

    def __init__(
        self
    ) -> None:
        self.we_active = False
        self.state = 1
        self.idGettingPass = None
        self.idDoPass = None
        self.GKLastState = None

    def process(self, field: fld.Field) -> list[Optional[Action]]:
        """Game State Management"""
        if field.game_state not in [GameStates.KICKOFF, GameStates.PENALTY]:
            if field.active_team in [const.Color.ALL, field.ally_color]:
                self.we_active = True
            else:
                self.we_active = False

        actions: list[Optional[Action]] = []
        for _ in range(const.TEAM_ROBOTS_MAX_COUNT):
            actions.append(None)

        if field.ally_color == const.COLOR:
            text = str(field.game_state) + "  we_active:" + str(self.we_active)
            field.strategy_image.print(aux.Point(600, 780), text, need_to_scale=False)
        match field.game_state:
            case GameStates.RUN:
                self.run(field, actions)
            case GameStates.TIMEOUT:
                pass
            case GameStates.HALT:
                return [None] * const.TEAM_ROBOTS_MAX_COUNT
            case GameStates.PREPARE_PENALTY:
                pass
            case GameStates.PENALTY:
                pass
            case GameStates.PREPARE_KICKOFF:
                pass
            case GameStates.KICKOFF:
                pass
            case GameStates.FREE_KICK:
                pass
            case GameStates.STOP:
                # The router will automatically prevent robots from getting too close to the ball
                self.run(field, actions)

        return actions



    def run(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        """
        ONE ITERATION of strategy
        NOTE: robots will not start acting until this function returns an array of actions,
              if an action is overwritten during the process, only the last one will be executed)

        Examples of getting coordinates:
        - field.allies[8].get_pos(): aux.Point -   coordinates  of the 8th  robot from the allies
        - field.enemies[14].get_angle(): float - rotation angle of the 14th robot from the opponents

        - field.ally_goal.center: Point - center of the ally goal
        - field.enemy_goal.hull: list[Point] - polygon around the enemy goal area


        Examples of robot control:
        - actions[2] = Actions.GoToPoint(aux.Point(1000, 500), math.pi / 2)
                The robot number 2 will go to the point (1000, 500), looking in the direction π/2 (up, along the OY axis)

        - actions[3] = Actions.Kick(field.enemy_goal.center)
                The robot number 3 will hit the ball to 'field.enemy_goal.center' (to the center of the enemy goal)

        - actions[9] = Actions.BallGrab(0.0)
                The robot number 9 grabs the ball at an angle of 0.0 (it looks to the right, along the OX axis)
        """

        """go to enemy and look on ball"""
        # idx = 3
        # rPos = field.allies[idx].get_pos()
        # ballPos = field.ball.get_pos()
        # actions[idx] = Actions.GoToPointIgnore(field.enemies[idx].get_pos(), (ballPos - rPos).arg())

        """do ellips"""
        # idx = 3
        # posR = field.allies[idx].get_pos()
        # if self.state == 1:
        #     """go to high yell point"""
        #     a = math.pi/2
        #     vect = aux.rotate(aux.RIGHT * 300, a) + field.enemies[0].get_pos()
        #     if aux.dist(posR, vect) < 100:
        #         self.startTime = time()
        #         self.state = 2
        #     else:
        #         actions[idx] = Actions.GoToPointIgnore(vect, 0)
        # if self.state == 2:
        #     """go around yell point"""
        #     a = math.pi/2 + time() - self.startTime
        #     if a < math.pi *2:
        #         vect = aux.rotate(aux.RIGHT * 300, a) + field.enemies[0].get_pos()
        #         actions[idx] = Actions.GoToPointIgnore(vect, 0)
        #     else:
        #         self.state = 3
        # if self.state == 3:
        #     """go to low blue point"""
        #     a = math.pi *3/2
        #     vect = aux.UP * -300 + field.allies[0].get_pos()
        #     if aux.dist(posR, vect) < 100:
        #         self.startTime = time()
        #         self.state = 4
        #     else:
        #         actions[idx] = Actions.GoToPointIgnore(vect, 0)
        # if self.state == 4:
        #     """go around blue point"""
        #     a = math.pi *3/2 + time() - self.startTime - math.pi*2
        #     if a >= math.pi/2*3 and a < math.pi*2:
        #         self.state = 1
        #     else:
        #         vect = aux.rotate(aux.UP * -300, a) + field.allies[0].get_pos()
        #         actions[idx] = Actions.GoToPointIgnore(vect, 0)
        # print(self.state)

        # field.strategy_image.draw_line(field.allies[const.GK].get_pos(), field.ball.get_pos(), (0, 0, 200))

        """go to ball then to nearest hull"""
        # idx = 3
        # rPos = field.allies[idx].get_pos()
        # ballPos = field.ball.get_pos()
        # match self.state:
        #     case 1:
        #         actions[idx] = Actions.GoToPointIgnore(ballPos, 0)
        #         if aux.dist(rPos, ballPos) < 100:
        #             self.state += 1
        #     case 2:
        #         nearestPointAllyHull = aux.nearest_point_in_poly(rPos, field.ally_goal.hull)
        #         nearestPointEnemyHull = aux.nearest_point_in_poly(rPos, field.enemy_goal.hull)
        #         dist2AllyHull = aux.dist(rPos, nearestPointAllyHull)
        #         dist2EnemyHull = aux.dist(rPos, nearestPointEnemyHull)
        #         if dist2AllyHull < dist2EnemyHull:
        #             actions[idx] = Actions.GoToPointIgnore(nearestPointAllyHull, 0)
        #             if aux.dist(rPos, nearestPointAllyHull) < 100:
        #                 self.state += 1
        #         else:
        #             actions[idx] = Actions.GoToPointIgnore(nearestPointEnemyHull, 0)
        #             if aux.dist(rPos, nearestPointEnemyHull) < 100:
        #                 self.state += 1
        #     case 3:
        #         self.state = 1

        """do giving interstction medians of triangel """
        # yRobot = field.enemies[0]
        # yRobot4 = field.enemies[4]
        # bRobot = field.allies[0]
        # yVect = aux.rotate(aux.RIGHT, yRobot.get_angle())*1000 + yRobot.get_pos()
        # y4Vect = aux.rotate(aux.RIGHT, yRobot4.get_angle())*1000 + yRobot4.get_pos()
        # bVect = aux.rotate(aux.RIGHT, bRobot.get_angle())*1000 + bRobot.get_pos()
        # intersectPoint1 = aux.get_line_intersection(yRobot.get_pos(), yVect, bRobot.get_pos(), bVect, "LL")
        # intersectPoint2 = aux.get_line_intersection(yRobot.get_pos(), yVect, yRobot4.get_pos(), y4Vect, "LL")
        # intersectPoint3 = aux.get_line_intersection(yRobot4.get_pos(), y4Vect, bRobot.get_pos(), bVect, "LL")
        # # field.strategy_image.draw_line(yRobot.get_pos(), yVect, (200, 200, 0))
        # # field.strategy_image.draw_line(bRobot.get_pos(), bVect, (0, 0, 200))
        # # if intersectPoint1 != None:
        # #     field.strategy_image.draw_line(yRobot.get_pos(), intersectPoint1, (200, 200, 200))
        # #     field.strategy_image.draw_line(bRobot.get_pos(), intersectPoint1, (200, 200, 200))
        # # if intersectPoint2 != None:
        # #     field.strategy_image.draw_line(yRobot.get_pos(), intersectPoint2, (0, 0, 0))
        # #     field.strategy_image.draw_line(bRobot.get_pos(), intersectPoint2, (0, 0, 0))
        # # if intersectPoint3 != None:
        # #     field.strategy_image.draw_line(yRobot.get_pos(), intersectPoint3, (0, 0, 0))
        # #     field.strategy_image.draw_line(bRobot.get_pos(), intersectPoint3, (0, 0, 0))
        # if intersectPoint1 != None and intersectPoint2 != None and intersectPoint3 != None:
        #     field.strategy_image.draw_line(intersectPoint1, intersectPoint2, (0, 0, 0))
        #     field.strategy_image.draw_line(intersectPoint2, intersectPoint3, (0, 0, 0))
        #     field.strategy_image.draw_line(intersectPoint3, intersectPoint1, (0, 0, 0))
        #     field.strategy_image.draw_circle((intersectPoint2 + intersectPoint1 + intersectPoint3)/3, color=(0, 255, 0), size_in_mms=30)

        """intersept maybe pass"""
        # idx = 5
        # rPos = field.allies[idx].get_pos()
        # ballPos = field.ball.get_pos()
        # enemyRPos = field.allies[3].get_pos()
        # # pointGo = aux.closest_point_on_line(enemyRPos, ballPos, rPos, "R")
        # pointGo = aux.point_on_line(ballPos, enemyRPos, 300)
        # actions[idx] = Actions.GoToPoint(pointGo, 0)

        """patrul enemy hull for test findPointForScore"""
        # idx = 3
        # rPos = field.allies[idx].get_pos()
        # findPointForScore(field, rPos)
        # actions[idx] = Actions.GoToPointIgnore(field.enemy_goal.frw, 0)
        # # actions[idx] = Actions.GoToPointIgnore(aux.Point(0, 0), 0)
        # # print(len(aux.line_circle_intersect(rPos, field.enemy_goal.center, field.enemies[const.ENEMY_GK].get_pos(), const.ROBOT_R*1.2, "S")))
        # # print([robot.r_id for robot in field.active_enemies(True)])
        # if self.state == 1:
        #     actions[idx] = Actions.GoToPointIgnore(field.enemy_goal.frw_up, 0)
        #     if aux.dist(rPos, field.enemy_goal.frw_up) < 100:
        #         self.state = 2
        # if self.state == 2:
        #     actions[idx] = Actions.GoToPointIgnore(field.enemy_goal.frw_down, 0)
        #     if aux.dist(rPos, field.enemy_goal.frw_down) < 100:
        #         self.state = 1

        """intersept maybe pass for 2 enemy R"""
        # idx = 3
        # rPos = field.allies[idx].get_pos()
        # ballPos = field.ball.get_pos()
        # enemyRWithBall = field.allies[0]
        # enemyRWhatMaybeHavePass1 = field.enemies[0]
        # enemyRWhatMaybeHavePass2 = field.enemies[5]
        # enemyRWithBallPos = enemyRWithBall.get_pos()
        # # pointGo = aux.closest_point_on_line(enemyRPos, ballPos, rPos, "R")
        # if abs(enemyRWithBall.get_angle() - enemyRWhatMaybeHavePass1.get_angle()) < abs(enemyRWithBall.get_angle() - enemyRWhatMaybeHavePass2.get_angle()):
        #     enemyRWhatHavePass = enemyRWhatMaybeHavePass1
        # else:
        #     enemyRWhatHavePass = enemyRWhatMaybeHavePass2
        # pointGo = aux.point_on_line(enemyRWithBallPos, enemyRWhatHavePass.get_pos(), 300)
        # actions[idx] = Actions.GoToPoint(pointGo, 0)
        # # actions[0] = Actions.GoToPoint(aux.Point(0, 0), 0)

        """open for pass"""
        # idx = 3
        # ballPos = field.ball.get_pos()
        # enemysR = field.active_enemies(True)
        # rPos = field.allies[idx].get_pos()
        # rWhichPreventPass = None
        # vectFromRToBall = ballPos - rPos
        # # for enemyR in enemysR: # NORM CODE
        # #     if len(aux.line_circle_intersect(ballPos, rPos, enemyR.get_pos(), const.ROBOT_R, "S")) != 0:
        # #         rWhichPreventPass = enemyR
        # if len(aux.line_circle_intersect(ballPos, rPos, field.allies[5].get_pos(), const.ROBOT_R, "S")) != 0: # HARD CODE!!!
        #     rWhichPreventPass = field.allies[5]
        # if rWhichPreventPass != None:
        #     if aux.get_angle_between_points(rWhichPreventPass.get_pos(), ballPos, rPos) > 0:
        #         """open to left"""
        #         vect = aux.rotate(vectFromRToBall.unity(), -math.pi/2)
        #         pointToGo = vect*700 + rPos
        #         if pointToGo.x*field.polarity > 0:
        #             pointToGo = aux.rotate(vect, math.pi)*700 + rPos
        #     else:
        #         """open to right"""
        #         vect = aux.rotate(vectFromRToBall.unity(), math.pi/2)
        #         pointToGo = vect*700 + rPos
        #         if pointToGo.x*field.polarity > 0:
        #             pointToGo = aux.rotate(vect, math.pi)*700 + rPos
        #     actions[idx] = Actions.GoToPoint(pointToGo, 0)
        # else:
        #     actions[idx] = Actions.GoToPoint(field.allies[idx].get_pos(), 0)

        """test score goal"""
        # actions[0] = Actions.Kick(findPointForScore(field, field.allies[0].get_pos()))#WORK!!!
        play = False
        if len(field.active_allies(True)) != 0 and len(field.active_enemies(True)) != 0:
            if field.ally_color == const.Color.BLUE:
                """code for blue"""
                thisR = field.allies[0]
                enemies = field.active_enemies(True)
                nearestEnemyR = fld.find_nearest_robot(field.ball.get_pos(), enemies)
                otherAttackerR = field.allies[2]
                ballPos = field.ball.get_pos()
                actions[0] = Actions.BallGrab((nearestEnemyR.get_pos()-ballPos).arg())

                if play:
                    self.attacker(field, actions, 0, 2)
                    self.attacker(field, actions, 2, 0)
                    if field.allies[const.GK].is_used():
                        self.GKLastState = GK(field, actions, self.GKLastState) 
                # goToNearestScorePoint(field, actions, 0, 2)
                # goToNearestScorePoint(field, actions, 2, 0)
                # print(len(field.active_enemies()), [r.r_id for r in field.active_enemies()])
                # if len(field.active_enemies()) == 2:
                #     idx = 0
                #     rPos = field.allies[idx].get_pos()
                #     ballPos = field.ball.get_pos()
                #     # enemyRPos = field.allies[3].get_pos() # HARD CODE
                #     enemyRsPos = field.active_enemies().copy()
                #     # print(len(enemyRsPos))
                #     enemyRsPos.remove(fld.find_nearest_robot(ballPos, enemyRsPos))
                #     enemyRPos = enemyRsPos[0]
                #     # pointGo = aux.closest_point_on_line(enemyRPos, ballPos, rPos, "R")
                #     pointGo = aux.point_on_line(ballPos, enemyRPos.get_pos(), 300)
                #     actions[idx] = Actions.GoToPoint(pointGo, 0)
                # goToNearestScorePoint(field, actions, 0, 2)
                # self.attacker(field, actions, 0, 2)
                # if field.is_ball_in(field.allies[1]):
                #     actions[1] = Actions.GoToPoint(field.enemy_goal.center, (field.enemy_goal.center-field.allies[1].get_pos()).arg(), ignore_ball=True)
                #     field.allies[1].set_dribbler_speed(1)
                # else:
                #     actions[1] = Actions.BallGrab((field.enemy_goal.center-field.allies[1].get_pos()).arg())
                # self.attacker(field, actions, 2, 0)
                
                # p = findPointForScore(field) # for change koef
                # if p != None:
                #     actions[2] = Actions.Kick(p)
                # self.GKLastState = GK(field, actions, self.GKLastState) # for change koef
                # openForPass(field, 2, actions)
                # self.attacker(field, actions, 0, 2)
                # if not field.is_ball_in(field.allies[0]):
                #     actions[0] = Actions.BallGrab((field.ball.get_pos() - field.allies[0].get_pos()).arg())
                # else:
                #     field.strategy_image.draw_circle(field.allies[0].get_pos(), (255, 255, 255), 50)
                # self.attacker(field, actions, 1, 0)
                # """do pass"""
                # if self.idGettingPass != None:
                #     if not field.is_ball_in(field.allies[self.idGettingPass]):
                #         field.strategy_image.send_telemetry("status pass", "getting pass")
                #         actions[self.idGettingPass] = Actions.BallGrab((field.ball.get_pos()-field.allies[self.idGettingPass].get_pos()).arg())
                #     else:
                #         field.strategy_image.send_telemetry("status pass", "get pass")
                #         self.idDoPass = self.idGettingPass
                #         self.idGettingPass = None
                # # actions[0] = Actions.GoToPoint(aux.Point(0, 0), 0)
                # # findPointForScore(field, field.ball.get_pos())
                # # attacker(field, actions, 0, 1)
                
                # if field.is_ball_in(field.allies[self.idDoPass]):
                #     """do pass"""
                #     # field.strategy_image.send_telemetry("status", "pass")
                #     self.idGettingPass = doPassNearAllly(field, actions, self.idDoPass)
                # elif self.idGettingPass == None:
                #     """grab ball"""
                #     # field.strategy_image.send_telemetry("status", "grab")
                #     actions[self.idDoPass] = Actions.BallGrab((field.ball.get_pos() - field.allies[self.idDoPass].get_pos()).arg())  
                # else:
                #     """pass done"""
                #     # actions[self.idDoPass] = Actions.GoToPoint(aux.Point(0, 0), 0)  
                # # actions[0] = Actions.BallGrab((field.enemy_goal.center - field.ball.get_pos()).arg())  
                # # print(actions[0])
                # # actions[0] = Actions.Kick(field.enemy_goal.center)
            else:
                """code for yellow"""
                # findNearestScorePoint(field, actions, 0, 2)
                
                if play:
                    if field.allies[const.GK].is_used():
                        self.GKLastState = GK(field, actions, self.GKLastState) 
                    self.attacker(field, actions, 0, 2)
                    self.attacker(field, actions, 2, 0)
                # now = time()%8//4 # for change koef
                # match now:
                #     case 0:
                #         # pointF = field.ally_goal.center_down
                #         pointF = aux.Point(0, 200)
                #         field.strategy_image.draw_circle(aux.Point(0, 200), (200, 0, 0), 50)
                #         # print("1")
                #     case 1:
                #         # pointF = field.ally_goal.frw_down
                #         pointF = aux.Point(0, 0)
                #         field.strategy_image.draw_circle(aux.Point(0, 0), (200, 0, 0), 50)
                #         # print(2)
                # actions[const.GK] = Actions.GoToPointIgnore(aux.Point(pointF.x+100, pointF.y), 0)

                # actions[const.GK] = Actions.GoToPoint(aux.Point(0, 0), 0)/
                
                # pointForGK = aux.nearest_point_on_poly(field.ball.get_pos(), field.ally_goal.hull)
                # field.strategy_image.draw_line(pointForGK, field.ball.get_pos(), color=(200, 0, 200), size_in_pixels=20)
                # actions[const.GK] = Actions.GoToPointIgnore(pointForGK, (field.ball.get_pos()-field.allies[const.GK].get_pos()).arg())
                # field.allies[const.GK].set_dribbler_speed(1)

                # rPos = field.allies[1].get_pos()
                # nearestScorePoint = None
                # firstScorePoint = aux.Point(const.FIELD_DX/2*-field.polarity, const.FIELD_DY/2)
                # secondScorePoint = aux.Point(const.FIELD_DX/2*-field.polarity, -const.FIELD_DY/2)
                # if aux.dist(rPos, firstScorePoint) < aux.dist(rPos, secondScorePoint):
                #     field.strategy_image.draw_line(rPos, firstScorePoint, color = (0, 0, 0), size_in_pixels = 20)
                # else:
                #     field.strategy_image.draw_line(rPos, secondScorePoint, color = (0, 0, 0), size_in_pixels = 20)

                # openForPass(field, 7, actions)
                # self.GKLastState = GK(field, actions, self.GKLastState)
                # actions[const.GK] =  Actions.Kick(aux.Point(0, 0), is_pass=True)
                # self.attacker(field, actions, 0, 2)
                # self.attacker(field, actions, 2, 0)
        else:
            print("WE HAVENT ROBOTS")

    def doPass(self, field, actions, idxThisR):
        if field.is_ball_in(field.allies[self.idDoPass]):
            """do pass"""
            self.idGettingPass = doPassNearAllly(field, actions, idxThisR)
        elif self.idGettingPass == None:
            """grab ball"""
            actions[self.idDoPass] = Actions.BallGrab((field.ball.get_pos() - field.allies[self.idDoPass].get_pos()).arg())  
        else:
            self.idDoPass = None
            """pass done"""

    def gettingPass(self, field: fld.Field, actions, idxThisR):
        thisR = field.allies[self.idGettingPass]
        if self.idDoPass != None:
            actions[self.idGettingPass] = Actions.GoToPoint(thisR.get_pos(), (field.allies[self.idDoPass].get_pos()-thisR.get_pos()).arg())
        elif not field.is_ball_in(field.allies[self.idGettingPass]):
            # field.strategy_image.send_telemetry("status pass", "getting pass")
            """getting pass"""
            actions[self.idGettingPass] = Actions.BallGrab((field.ball.get_pos()-field.allies[self.idGettingPass].get_pos()).arg())
        else:
            """get pass"""
            # field.strategy_image.send_telemetry("status pass", "get pass")
            # actions[idxThisR] = Actions.Kick(findPointForScore(field))
            # self.idDoPass = self.idGettingPass
            self.idGettingPass = None

    def attacker(self, field: fld.Field, actions: list[Action], idxThisR, idxOtherAttacker):
        status = None
        enemies = field.active_enemies(True)
        enemysRsWithoutGK = field.active_enemies()
        allies = field.active_allies(True)
        # alliesWithoutGK = allies.copy()
        # alliesWithoutGK.remove(field.allies[const.GK])
        alliesRWithoutGK = field.active_allies()
        alliesWithoutGK = [r.get_pos() for r in alliesRWithoutGK]
        thisR: rbt.Robot = allies[idxThisR]
        thisRPos = thisR.get_pos()
        otherAttackerR = allies[idxOtherAttacker]
        ballPos = field.ball.get_pos()

        field.allies[idxThisR].set_dribbler_speed(0)

        if not field.allies[idxOtherAttacker].is_used():
            """if this attacker alone on field"""
            nearestEnemyR = fld.find_nearest_robot(field.ball.get_pos(), enemies)
            if ballPos.x*field.polarity > 0: # TODO need test
                """if ball on our part of field"""
                status = "if ball on our part of field"
                # TODO try replace ball from our part of field
                if not field.is_ball_in(thisR):
                    mostLikelyPointForScore = aux.closest_point_on_line(field.ally_goal.up, field.ally_goal.down, ballPos)
                    pointForR = aux.closest_point_on_line(ballPos, mostLikelyPointForScore, thisR.get_pos())
                    if not aux.is_point_on_line(thisR.get_pos(), ballPos, mostLikelyPointForScore, "S"):
                        """if this r not block maybe score, block"""
                        actions[idxThisR] = Actions.GoToPoint(pointForR, (ballPos-thisR.get_pos()).arg())
                        field.allies[idxThisR].set_dribbler_speed(15)
                    else:
                        """if this r block maybe score, try grab ball"""
                        # nearestEnemyR = fld.find_nearest_robot(field.ball.get_pos(), enemys)
                        actions[idxThisR] = Actions.BallGrab((nearestEnemyR.get_pos()-ballPos).arg())
            else:
                """if ball on other part of field"""
                if field.is_ball_in(thisR):
                    pointForScore = findPointForScore(field, ballPos)
                    if pointForScore != None:
                        """if this r can do score, he do"""
                        actions[idxThisR] = Actions.Kick(pointForScore)
                    else:
                        newPointForScore = findPointForScore(field, ballPos, k = 1)
                        if newPointForScore != None:
                            """if this r can do score, he try do do another score"""
                            actions[idxThisR] = Actions.Kick(newPointForScore)
                        else:
                            """if this r cant do score, he kick to GK or do upper"""
                            if len(enemysRsWithoutGK) != 0:
                                actions[idxThisR] = Actions.Kick(fld.find_nearest_robot(thisRPos, enemysRsWithoutGK), is_upper=True)
                            else:
                                actions[idxThisR] = Actions.Kick(field.enemies[const.ENEMY_GK].get_pos())
                else:
                    actions[idxThisR] = Actions.BallGrab((nearestEnemyR.get_pos()-ballPos).arg())
        elif self.idDoPass == idxThisR:
            """if thid R do pass"""
            status = "1"
            self.doPass(field, actions, idxThisR)
        elif idxThisR == self.idGettingPass:
            """if this R getting pass"""
            status = "2"
            self.gettingPass(field, actions, idxThisR)
        elif actions[idxThisR] == None:
            """if we dont send command on this robot"""
            allR = enemies.copy() + allies.copy()
            nearestRToBall = fld.find_nearest_robot(field.ball.get_pos(), allR)
            field.strategy_image.draw_circle(nearestRToBall.get_pos(), (200, 0, 255), 50)
            if nearestRToBall == thisR: # TODO if nearest R to ball - enemy GK
                """if nearest to ball bot this"""
                if field.is_ball_in(thisR):
                    # field.strategy_image.draw_circle(thisR.get_pos(), (255, 255, 255), 50)
                    """if this robot have ball"""
                    pointForScore = findPointForScore(field)
                    if pointForScore != None:
                        """try do score if r can"""
                        # field.strategy_image.send_telemetry("status", "try do score if r can")
                        status = "try do score if r can"
                        actions[idxThisR] = Actions.Kick(pointForScore)
                    else:
                        """if this r cant do score"""
                        # nearestEnemyRToThisAttacker = fld.find_nearest_robot(thisR.get_pos(), enemys)
                        # nearestEnemyRToOtherAttacker = fld.find_nearest_robot(otherAttackerR.get_pos(), enemys)

                        # pointForScoreForOtherAttacker = findPointForScore(field, otherAttackerR.get_pos())
                        status = "if this r cant do score"
                        self.idGettingPass = doPassNearAllly(field, actions, idxThisR)
                        # if pointForScoreForOtherAttacker != None:
                        #     """if other attacker can do score, pass other attacker"""
                        #     status = "if other attacker can do score, pass other attacker"
                        #     self.idGettingPass = doPassNearAllly(field, actions, idxThisR)
                        # else:
                        #     """if both attackers cant do score try do score: change position"""
                        #     status = "if both attackers cant do score try do score: change position"
                        #     goToNearestScorePoint(field, actions, 0, None)
                else:
                    if self.idGettingPass == None:
                        """if this r is nearest to ball, but dont grab him, grab ball"""
                        # field.strategy_image.send_telemetry("status", "if this r is nearest to ball, but dont grab him, grab ball")
                        status = "if this r is nearest to ball, but dont grab him, grab ball"
                        # actions[idxThisR] = Actions.BallGrab((field.ball.get_pos() - thisR.get_pos()).arg())
                        actions[idxThisR] = Actions.BallGrab((-field.ball.get_pos() + field.enemy_goal.center).arg())#TEST
                    else:
                        """do do pass and wait for result"""
                        status = "do do pass and wait for result"
                        actions[idxThisR] = Actions.GoToPoint(aux.Point(0, 0), (field.allies[idxOtherAttacker].get_pos()-thisR.get_pos()).arg())
            elif nearestRToBall == field.allies[idxOtherAttacker]:
                    """if other attacker have ball"""
                    status = "if other attacker have ball"
                    goToNearestScorePoint(field, actions, idxThisR, idxOtherAttacker)
            elif nearestRToBall == field.allies[const.GK]:
                """if GK have ball"""
                status = "if GK have ball"
                # print(alliesWithoutGK, field.allies)
                nearestRToGK = aux.find_nearest_point(field.ball.get_pos(), alliesWithoutGK)
                if nearestRToGK == field.allies[idxThisR]:
                    """if this R nearest to GK"""
                    openForPass(field, idxThisR, actions)
                else:
                    """if not this r nearest to GK"""
                    actions[idxThisR] = Actions.GoToPoint(aux.Point(0, 0), 0)
            elif nearestRToBall == field.enemies[const.GK]:
                """if nearest r to ball is enemy GK"""
                status = "if nearest r to ball is enemy GK"
                enemyRsPos = field.active_enemies().copy()
                enemyRsPos.remove(fld.find_nearest_robot(ballPos, enemyRsPos))
                enemyRPos = enemyRsPos[0]
                pointGo = aux.point_on_line(ballPos, enemyRPos.get_pos(), 300)
                actions[idxThisR] = Actions.GoToPoint(pointGo, (thisRPos-enemyRPos.get_pos()).arg())
                field.allies[idxThisR].set_dribbler_speed(15)
            elif ballPos.x*field.polarity > 0: # TODO need test
                """if ball on our part of field"""
                status = "if ball on our part of field"
                dist2BallFromThisR = aux.dist(ballPos, thisR.get_pos())
                dist2BallFromOtherR = aux.dist(ballPos, otherAttackerR.get_pos())
                if dist2BallFromThisR < dist2BallFromOtherR:
                    """if this attacker nearest to ball then other"""
                    mostLikelyPointForScore = aux.closest_point_on_line(field.ally_goal.up, field.ally_goal.down, ballPos)
                    pointForR = aux.closest_point_on_line(ballPos, mostLikelyPointForScore, thisR.get_pos())
                    if not aux.is_point_on_line(thisR.get_pos(), ballPos, mostLikelyPointForScore, "S"):
                        """if this r not block maybe score, block"""
                        actions[idxThisR] = Actions.GoToPoint(pointForR, (ballPos-thisR.get_pos()).arg())
                        field.allies[idxThisR].set_dribbler_speed(15)
                    else:
                        """if this r block maybe score, try grab ball"""
                        nearestEnemyR = fld.find_nearest_robot(field.ball.get_pos(), enemies)
                        actions[idxThisR] = Actions.BallGrab((nearestEnemyR.get_pos()-ballPos).arg())
                else:
                    """if nearest attacker for ball other, block maybe pass"""
                    # enemyRPos = field.allies[3].get_pos() # HARD CODE
                    enemyRsPos = field.active_enemies().copy()
                    enemyRsPos.remove(fld.find_nearest_robot(ballPos, enemyRsPos))
                    enemyRPos = enemyRsPos[0]
                    # pointGo = aux.closest_point_on_line(enemyRPos, ballPos, rPos, "R")
                    pointGo = aux.point_on_line(ballPos, enemyRPos.get_pos(), 300)
                    actions[idxThisR] = Actions.GoToPoint(pointGo, (thisRPos-enemyRPos.get_pos()).arg())
                    field.allies[idxThisR].set_dribbler_speed(15)
            else:
                """if ball not on our part of field"""
                status = "if ball not on our part of field"
                # enemyRsPos = field.active_enemies().copy()
                # enemyRsPos.remove(fld.find_nearest_robot(ballPos, enemyRsPos))
                # enemyRPos = enemyRsPos[0]
                # enemies = field.active_enemies(True)
                enemyRPos = fld.find_nearest_robot(ballPos, enemies)
                dist2BallFromThisR = aux.dist(ballPos, thisR.get_pos())
                dist2BallFromOtherR = aux.dist(ballPos, otherAttackerR.get_pos())
                if dist2BallFromThisR < dist2BallFromOtherR:
                    """if this attacker nearest to ball then other, take ball"""
                    actions[idxThisR] = Actions.BallGrab((enemyRPos.get_pos()-ballPos).arg())
                else:
                    """if nearest attacker for ball other, block maybe pass"""
                    # enemyRPos = field.allies[3].get_pos() # HARD CODE
                    # pointGo = aux.closest_point_on_line(enemyRPos, ballPos, rPos, "R")
                    pointGo = aux.point_on_line(ballPos, enemyRPos.get_pos(), 300)
                    actions[idxThisR] = Actions.GoToPoint(pointGo, (thisRPos-enemyRPos.get_pos()).arg())
                    field.allies[idxThisR].set_dribbler_speed(15)
        # print(status, idxThisR)
        field.strategy_image.send_telemetry("statusAttacker"+str(idxThisR), status)
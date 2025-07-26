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
        self.startTime = 0

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

        # rPos = field.allies[const.GK]
        # ballPos = field.ball.get_pos()
        # print((rPos+ballPos)/2)

        # for i in range(4):
        #     print(field.ally_goal.hull[i], end="***")
        # actions[0] = Actions.GoToPoint(aux.Point(500, 500), math.pi / 2)

        # vect = (field.ball.get_pos()-field.allies[0].get_pos())/2
        # print(vect + field.allies[0].get_pos())
        # print(aux.get_line_intersection(field.allies[0].get_pos(), field.allies[1].get_pos(), field.ball.get_pos(), field.enemies[0].get_pos(), "LL"))
        # print(aux.closest_point_on_line(field.ball.get_pos(), field.ally_goal.center, field.allies[1].get_pos()))

        # idx = 3
        # rPos = field.allies[idx].get_pos()
        # ballPos = field.ball.get_pos()
        # actions[idx] = Actions.GoToPointIgnore(field.enemies[idx].get_pos(), (ballPos - rPos).arg())

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
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
    
    def doPassNearAllly(field: fld.Field, actions: list[Action], idFrom = const.GK):
        pass


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

        idx = 3
        rPos = field.allies[idx].get_pos()
        ballPos = field.ball.get_pos()
        actions[idx] = Actions.GoToPointIgnore(field.enemies[idx].get_pos(), (ballPos - rPos).arg())
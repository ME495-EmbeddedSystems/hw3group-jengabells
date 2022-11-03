import numpy as np
import rclpy
from moveit_msgs.action import MoveGroup
from rclpy.action import ActionClient
from moveit_msgs.srv import GetPositionIK
from rclpy.callback_groups import ReentrantCallbackGroup


class PlanAndExecute:
    def __init__(self, node):
        self.node = node
        # Create a client
        self.node._action_client = ActionClient(self,
                                                MoveGroup,
                                                '/move_action')
        # Make it so we can call the IK service
        self.cbgroup = ReentrantCallbackGroup()
        self.node.IK = self.node.create_client(GetPositionIK,
                                               "compute_ik",
                                               callback_group = self.cbgroup)

    def plan_to_position(self, start_pose, end_pos):
        """Returns MoveGroup action from a start pose to an end end position"""
        mvg = MoveGroup()
        # 1. Call GetPositionIK.srv to get the joint states of final position 
        # Something like this? await self.node.IK.call_async(end_pos) except idk how to get res
        # 2. Wait for service response (await?)
        # 3. Receive RobotState soln. soln.joint_state gives joint_state type msg
        # 4. Plug this into mvg.request.goal_constraints.joint_constraints (joint_state type)
        # 5. Return mvg action
        return mvg
    def plan_to_orientation(self, start_pose, end_orientation):
        """Returns MoveGroup action from a start pose to an end orientation"""
        mvg = MoveGroup()
        return mvg
    def plan_to_pose(self,start_pose, end_pose):
        """Returns MoveGroup action from a start pose to an end pose (position + orientation)"""
        mvg = MoveGroup()
        return mvg
    def execute(self, mvg):
        """Takes a MoveGroup object, sends it through the client"""
        pass
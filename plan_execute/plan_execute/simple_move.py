import rclpy
from rclpy.node import Node
from enum import Enum, auto
from plan_execute_interface.srv import GoHere
from plan_execute.plan_and_execute import PlanAndExecute
from moveit_msgs.action import MoveGroup
from geometry_msgs.msg import Point, Quaternion, Pose
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
class State(Enum):
    """
    Current state of the system.

    Determines what the main timer function should be doing on each iteration
    """
    START = auto(),
    IDLE = auto(),
    CALL = auto()


class Test(Node):
    """
    Keep track of enviroment components and do calculations.

    This node publishes to the visualization_marker, text_marker, goal_pose, move_robot,
    and tilt. it also has parammeters for gravity and velocity.
    """

    def __init__(self):
        super().__init__('simple_move')
        # Start timer
        self.freq = 100.
        self.cbgroup = MutuallyExclusiveCallbackGroup()
        self.timer = self.create_timer(1./self.freq, self.timer_callback, callback_group=self.cbgroup)
        self.movegroup = None # Fill this in later lol
        self.go_here = self.create_service(GoHere, 'go_here', self.go_here_callback)
        self.PlanEx = PlanAndExecute(self)

        self.state = State.START
        self.ct = 0
        self.goal_pose = Pose()
        self.future = None

    def go_here_callback(self, request, response):
        self.start_pose = request.start_pose
        self.goal_pose = request.goal_pose
        self.execute = request.execute
        
        if len(self.start_pose) > 1:
            self.get_logger().info('Enter either zero or one initial poses.')
            self.state = State.IDLE
            response.success = False
        else:
            self.state = State.CALL
            response.success = True
        return response

    async def timer_callback(self):
        if self.state == State.START:
            # add a bit of a time buffer so js can be read in
            if self.ct==100:
                self.state = State.IDLE
            else:
                self.ct += 1
        if self.state == State.CALL: 
            self.state = State.IDLE
            start = []
            self.future = await self.PlanEx.plan_to_orientation(self.start_pose, self.goal_pose, self.execute)
            print(type(self.future))
            print("MAIN LOOP:", self.future)
        # self.get_logger().info("test")


def test_entry(args=None):
    rclpy.init(args=args)
    node = Test()
    rclpy.spin(node)
    rclpy.shutdown()
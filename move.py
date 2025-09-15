import grpc
from example_policies.robot_deploy.robot_io.robot_service import (
    robot_service_pb2,
    robot_service_pb2_grpc,
)
from example_policies.robot_deploy.robot_io.robot_interface import RobotInterface

server = "localhost:50051"
channel = grpc.insecure_channel(server)
stub = robot_service_pb2_grpc.RobotServiceStub(channel)

# Use RobotInterface for convenience
robot_interface = RobotInterface(stub, cfg=None)  # cfg can be None for manual commands

# Example: move forward with manual command
action = robot_service_pb2.RobotAction()
action.linear_velocity = 0.5  # m/s
action.angular_velocity = 0.0  # rad/s

robot_interface.send_action(action, mode="direct")  # "direct" mode ignores ML translation

# -*- coding: cp936 -*-
# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import matplotlib.pyplot as plt

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleanTiles = {}
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        p = (int(pos.getX()), int(pos.getY()))
        if p in self.cleanTiles:
            return
        self.cleanTiles[p] = True

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        pos = (int(m), int(n))
        return pos in self.cleanTiles
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleanTiles.keys())

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.uniform(0, self.width), random.uniform(0, self.height))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return pos.getX() >= 0 and pos.getX() < self.width and pos.getY() >= 0 and pos.getY() < self.height


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.pos = self.room.getRandomPosition()
        self.room.cleanTileAtPosition(self.pos)
        self.direction = random.randint(0, 360)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPos = self.pos.getNewPosition(self.direction, self.speed)
        self.setRobotPosition(newPos)
        self.room.cleanTileAtPosition(self.pos)
        


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos = self.pos.getNewPosition(self.direction, self.speed)
        if not  self.room.isPositionInRoom(pos):
            self.setRobotDirection(random.randint(0, 360))
        else:
            Robot.updatePositionAndClean(self)

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    time_steps = []
    for t in range(num_trials):
        room = RectangularRoom(width, height)
        step = simOne(num_robots, speed, room, min_coverage, robot_type)
        
        time_steps.append(step)
    return sum(time_steps) / float(len(time_steps))

def simOne(num_robots, speed, room, min_coverage, robot_type):
    coverage = calc_coverage(room)
    robots = []
    # anim = ps6_visualize.RobotVisualization(num_robots, room.width, room.height)
    for n in range(num_robots):
        robots.append(robot_type(room, speed))
    steps = 0
    while coverage < min_coverage:
        for robot in robots:
            robot.updatePositionAndClean()
        coverage = calc_coverage(room)
        steps += 1
        # anim.update(room, robots)
    # anim.done()
    return steps

def calc_coverage(room):
    return float(room.getNumCleanedTiles()) / float(room.getNumTiles())


# === Problem 4
#
# 1) How long does it take to clean 80% of a 20��20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20��20, 25��16, 40��10, 50��8, 80��5, and 100��4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    num_robots = range(1, 11)
    steps = []
    for n in num_robots:
        step = runSimulation(n, 1.0, 20, 20, 0.8, 10, StandardRobot)
        steps.append(step)
    plt.plot(num_robots, steps)
    plt.xlabel('number of robots')
    plt.ylabel('steps/time')
    plt.legend(loc='best')
    plt.suptitle('time to clean 80% of a 20 * 20 square room, for various robot number')
    plt.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    room_sizes = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    steps = []
    ratios = []
    for xy in room_sizes:
        step = runSimulation(2, 1.0, xy[0], xy[1], 0.8, 50, StandardRobot)
        steps.append(step)
        ratios.append(float(xy[0]/xy[1]))
    
    plt.plot(ratios, steps)
    plt.xlabel('ratios of width to heigh')
    plt.ylabel('mean time to clean 80% of room with two robots')
    plt.legend(loc='best')
    plt.suptitle('time to clean 80% of a room with 2 robots, for various width to height ratio')
    plt.show()
    

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos = self.pos.getNewPosition(self.direction, self.speed)
        if not  self.room.isPositionInRoom(pos):
            self.setRobotDirection(random.randint(0, 360))
        else:
            Robot.updatePositionAndClean(self)
            self.setRobotDirection(random.randint(0, 360))
    


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    num_robots = range(1, 11)
    step_standard = []
    step_random = []
    for n in num_robots:
        step_standard.append(runSimulation(n, 1.0, 20, 20, 0.8, 10, StandardRobot))
        step_random.append(runSimulation(n, 1.0, 20, 20, 0.8, 10, RandomWalkRobot))
    plt.plot(num_robots, step_standard, label='standard robot')
    plt.plot( num_robots, step_random, label='random walk robot')
    plt.xlabel('number of robot')
    plt.ylabel('mean time to clean 80% of room')
    plt.legend(loc='best')
    plt.suptitle('time to clean 80% of a room with different robot, for various robots number')
    plt.show()

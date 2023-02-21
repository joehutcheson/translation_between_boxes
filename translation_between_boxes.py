import math
import numpy as np

def find_translation(first_box, second_box):
    """
    Finds the distance between two boxes with 4 corners.
    Positions are given as a list of [x, y] positions.

    :param first_box: List of positions of corners for first box
    :param second_box: List of positions of corners for second box
    :return: Array [x, y] of minimum translation between boxes
    """

    first_box = np.array(first_box)
    second_box = np.array(second_box)

    # Adapted from Grumdrig's answer to
    # https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
    def length_between_line_and_point(points, line):
        if math.dist(line[0], line[1]) == 0:
            return math.dist(line[0], points)
        l_squared = np.linalg.norm(line[0] - line[1]) ** 2
        t = max(0, min(1, np.dot(points - line[0], (line[1] - line[0]) / l_squared)))
        projection_ = line[0] + (t * (line[1] - line[0]))
        return math.dist(points, projection_), projection_

    # find min distance between corners and edges of the boxes
    min_dist, projection = length_between_line_and_point(first_box[0], second_box[0:2])
    min_trans = projection - first_box[0]
    for i in range(4):
        p1 = first_box[i]
        p2 = first_box[(i + 1) % 4]
        l = np.array([p1, p2])
        for j in range(4):
            p = second_box[j]
            dist, projection = length_between_line_and_point(p, l)
            if dist < min_dist:
                min_dist = dist
                min_trans = p - projection

    for i in range(4):
        p1 = second_box[i]
        p2 = second_box[(i + 1) % 4]
        l = np.array([p1, p2])
        for j in range(4):
            p = first_box[j]
            dist, projection = length_between_line_and_point(p, l)
            if dist < min_dist:
                min_dist = dist
                min_trans = projection - p

    return min_trans

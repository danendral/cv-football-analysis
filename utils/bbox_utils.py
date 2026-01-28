def get_center_of_bbox(bbox):
    """
    Given a bounding box in the format [x1, y1, x2, y2],
    return the center coordinates (x_center, y_center).
    """
    x1, y1, x2, y2 = bbox
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    return int(x_center), int(y_center)

def get_width_of_bbox(bbox):
    """
    Given a bounding box in the format [x1, y1, x2, y2],
    return the width of the bounding box.
    """
    x1, y1, x2, y2 = bbox
    return x2 - x1

def measure_distance(p1, p2):
    """
    Measure Euclidean distance between two points p1 and p2.
    Each point is a tuple (x, y).
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def measure_xy_distance(p1, p2):
    """
    Measure the distance in x and y directions between two points p1 and p2.
    Each point is a tuple (x, y).
    Returns a tuple (dx, dy).
    """
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return dx, dy
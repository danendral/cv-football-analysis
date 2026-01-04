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
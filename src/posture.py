# POSTURE - this module contains the classify_posture function, 
# which takes the coordinates of a bounding box (x1, y1, x2, y2) and classifies the posture of the detected person 
# based on the proportions of the bounding box. The function returns a string indicating whether the person is standing, sitting, or bending.

def classify_posture(x1, y1, x2, y2):
    """
    Classify posture using bounding box proportions.

    Returns:
        Standing / Sitting / Bending
    """

    height = y2 - y1
    width = x2 - x1

    if width == 0:
        return "Unknown"

    ratio = height / width

    if ratio > 1.6:
        return "Standing"
    elif ratio > 1.1:
        return "Sitting"
    else:
        return "Bending"

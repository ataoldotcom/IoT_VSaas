# detection_filters.py

def is_target_detection(class_name, target_classes):
    """
    Returns True if the detected class is in the target set.

    :param class_name: str (e.g., "dog", "person")
    :param target_classes: set or list of target class names
    :return: bool
    """
    if not target_classes:
        return True
    return class_name in target_classes


def filter_detections(detections, target_classes):
    """
    Filters a list of detection dicts to only include target classes.

    :param detections: list of dicts
        Example:
        [
            {"class_name": "dog", "box": box},
            {"class_name": "chair", "box": box}
        ]
    :param target_classes: set or list
    :return: filtered list
    """
    if not target_classes:
        return detections
    return [
        d
        for d in detections
        if d.get("normalized_class_name", d.get("class_name", "")).strip().lower() in target_classes
    ]

# metrics.py

import numpy as np

# ============================
# Metric Calculation Functions
# ============================

def accuracy(y_true, y_pred):
    """
    Calculates the accuracy of predictions.

    Args:
        y_true (list or np.array): True labels.
        y_pred (list or np.array): Predicted labels.

    Returns:
        float: Accuracy score.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.sum(y_true == y_pred) / len(y_true)

def precision(y_true, y_pred):
    """
    Calculates the precision of predictions.

    Args:
        y_true (list or np.array): True labels.
        y_pred (list or np.array): Predicted labels.

    Returns:
        float: Precision score.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    return tp / (tp + fp) if tp + fp > 0 else 0.0

def recall(y_true, y_pred):
    """
    Calculates the recall of predictions.

    Args:
        y_true (list or np.array): True labels.
        y_pred (list or np.array): Predicted labels.

    Returns:
        float: Recall score.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return tp / (tp + fn) if tp + fn > 0 else 0.0

def f1_score(y_true, y_pred):
    """
    Calculates the F1 score of predictions.

    Args:
        y_true (list or np.array): True labels.
        y_pred (list or np.array): Predicted labels.

    Returns:
        float: F1 score.
    """
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2 * (p * r) / (p + r) if p + r > 0 else 0.0

def hamming_score(y_true, y_pred):
    """
    Calculates the Hamming score of predictions.

    Args:
        y_true (list or np.array): True labels.
        y_pred (list or np.array): Predicted labels.

    Returns:
        float: Hamming score.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.sum(y_true != y_pred) / len(y_true)

# ============================
# Example Usage
# ============================

if __name__ == "__main__":
    # Example true and predicted labels
    y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
    y_pred = [1, 0, 1, 0, 0, 1, 0, 1, 1, 0]

    # Calculate and print metrics
    print(f"Accuracy: {accuracy(y_true, y_pred):.4f}")
    print(f"Precision: {precision(y_true, y_pred):.4f}")
    print(f"Recall: {recall(y_true, y_pred):.4f}")
    print(f"F1 Score: {f1_score(y_true, y_pred):.4f}")
    print(f"Hamming Score: {hamming_score(y_true, y_pred):.4f}")
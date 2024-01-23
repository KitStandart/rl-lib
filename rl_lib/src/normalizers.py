import numpy as np


def normalize_m1_1(x: np.ndarray) -> np.ndarray:
    """Нормализует RGB изображение в диапазон [-1, 1]."""
    return x / 127.5 - 1


def normalize_01(x: np.ndarray) -> np.ndarray:
    """Нормализует RGB изображение в диапазон [0, 1]."""
    return x / 255.0

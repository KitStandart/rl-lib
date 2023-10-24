from tensorflow import expand_dims
from tensorflow.dtypes import int32
from tensorflow.keras.activations import softmax
from tensorflow.math import argmax, log
from tensorflow.random import categorical

from rl_lib.src.algoritms.model_free.value_based.base_algo import Base_Algo

from ..data_saver.utils import load_data, save_data
from .base_explore import Base_Explore


class Soft_Q(Base_Explore):
    """Больцмановская стратегия исследования
    a = softmax(Q/tau)

    Kwargs:
      tau: float, Больцмановская температура
      axis: int, Ось вычислений
    """

    def __init__(self, decay=0, tau=1.0, axis=-1, **kwargs):
        self.decay = decay
        self.tau = tau
        self.axis = axis
        self._name = "soft_q_strategy"

    def __call__(self, Q) -> int:
        """Возвращает действие в соответствии с стратегией исследования"""
        probability = softmax(expand_dims(Q, 0)/self.tau, axis=self.axis)
        self.tau = self.tau * self.decay
        return Base_Algo.squeeze_predict(
            categorical(
                log(probability),
                1,
                dtype=int32)
              )

    @property
    def name(self):
        return self._name

    def load(self, path) -> None:
        """Загружает какие либо внутренние переменные"""
        self.__dict__ = load_data(path+self.name)

    def reset(self, ) -> None:
        """Выполняет внутренний сброс"""
        pass

    def save(self, path) -> None:
        """Сохраняет какие либо внутренние переменные"""
        save_data(path+self.name, self.__dict__)

    def test(self, Q) -> int:
        """Возвращает действие в соответствии с стратегией тестирования"""
        return argmax(Q, axis=self.axis, output_type=int32)

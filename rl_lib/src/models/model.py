import tensorflow as tf
import abc

from .base_models import ModelNN, ModelIO, BaseModel
from ..optimizers.optimizers import get_optimizer

class Model(ModelNN, ModelIO, BaseModel, abc.ABC):
  """Абстрактный класс модели, который соединяет все методы классов ModelNN, ModelIO, BaseModel"""
  def __init__(self, **config: dict):
    super().__init__(**config)
    self.initial_model()

  def _initial_model(self):
    input_shape = self._config['model_config']["input_shape"]
    action_space =  self._config['model_config']["action_space"]
    if len(input_shape) == 1:
      return self.create_model(input_shape, action_space)
    else:
      return self.create_model_with_conv(input_shape, action_space)
  
  def initial_model(self):
    """Инициализирует модель в соответствии с типом алгоритма"""
    if str(self.config['model_config']['model']) == 'None': model = self._initial_model()
    else:  model = self.config['model_config']['model']
    optimizer = self.config.get("optimizer")
    optimizer = get_optimizer(**optimizer)
    self.model.set_new_model(model, optimizer)

  def input_spec(self):
    return self.model.layers[0].input_shape[0]

  def load(self):
    self.model = tf.keras.models.load_model(self.path+self.name+'.h5')
    
  def output_spec(self):
    return self.model.layers[-1].input_shape[0]

  def save(self):
    print(self.name)
    self.model.save(self.path+self.name+'.h5')
    
  @staticmethod
  @abc.abstractclassmethod
  def create_model(input_shape: tuple, action_space: int) -> tf.keras.Model:
     """Создает модель по умолчанию и возвращает tf.keras.Model, архитектура в соответствии с алгоритмом, начальные слои - полносвязные"""
    
  @staticmethod
  @abc.abstractclassmethod
  def create_model_with_conv(input_shape: tuple, action_space: int) -> tf.keras.Model:
    """Создает модель по умолчанию  и возвращает tf.keras.Model, архитектура в соответствии с алгоритмом, начальные слои - сверточные"""

# Standard Library
from dataclasses import dataclass
from typing import Tuple

# Third Party Library
from omegaconf import II, OmegaConf


@dataclass
class PreprocessConfig:
    target_size: Tuple[int, int] = (64, 64)
    normalize: bool = True


@dataclass
class ModelConfig:
    image_size: Tuple[int, int] = II("preprocess.target_size")
    drop_rate: float = 0.5


@dataclass
class TrainConfig:
    epochs: int = 5
    batch_size: int = 32
    learning_rate: float = 0.001


@dataclass
class ExperimentConfig:
    preprocess: PreprocessConfig = PreprocessConfig()
    model: ModelConfig = ModelConfig()
    train: TrainConfig = TrainConfig()
    logdir: str = "outputs"

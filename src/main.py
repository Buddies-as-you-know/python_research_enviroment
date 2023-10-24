# Standard Library
import os
import time

# Third Party Library
from omegaconf import OmegaConf

# First Party Library
from config import config


def preprocess(configs: config.PreprocessConfig) -> None:
    print(OmegaConf.to_yaml(configs))
    return


def build_model(configs: config.ModelConfig) -> None:
    print(OmegaConf.to_yaml(configs))
    return


def train(configs: config.TrainConfig) -> None:
    print(OmegaConf.to_yaml(configs))
    print(configs)
    return


def run(configs) -> None:
    preprocess(configs.preprocess)
    build_model(configs.model)
    train(configs.train)
    return


def main() -> None:
    base_config = OmegaConf.structured(config.ExperimentConfig)
    cli_config = OmegaConf.from_cli()
    merged_config = OmegaConf.merge(base_config, cli_config)
    path = os.getcwd()
    time_str = time.strftime("%Y-%m-%dT%H-%M-%S")

    # 'logdir' contains the full path where the files should be saved.
    logdir = f"{path}/docs/{merged_config.logdir}/{time_str}"  # 新しい変数を使用

    # Make the directory if it doesn't exist.
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    # Save the configuration files.
    # You don't need to add 'path' again here,
    # 'logdir' is already the full path.
    config_save_path = f"{logdir}/config.yaml"
    override_save_path = f"{logdir}/override.yaml"

    OmegaConf.save(merged_config, config_save_path)
    OmegaConf.save(cli_config, override_save_path)

    run(merged_config)


if __name__ == "__main__":
    main()

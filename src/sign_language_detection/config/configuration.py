from src.sign_language_detection.entity.config_entity import SignLanguageConfig
from src.sign_language_detection.logger import logger
from src.sign_language_detection.exceptions import AppException
from src.sign_language_detection.constants import *
from src.sign_language_detection.utils import read_yaml

class ConfigurationManager:
    def __init__(self, config_file_path:str = CONFIG_FILE_PATH) -> None:
        try:
            self.config=read_yaml(file_path=config_file_path)['sign_language_detection']
        except Exception as e:
            raise AppException(e) from e
    
    def get_sign_language_config(self) -> SignLanguageConfig:
        try:
            sign_language_config = SignLanguageConfig(
                camera_id=self.config["camera_id"],
                data_directory=self.config["data_directory"],
                capture_count=self.config["capture_count"],
                delay_between_captures=self.config["delay_between_captures"],
                no_of_classes=self.config["no_of_classes"],
                class_names=self.config["class_names"],
                class_colors=self.config["class_colors"],
            )
            return sign_language_config
        except Exception as e:
            raise AppException(e) from e
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SignLanguageConfig:
    camera_id: int
    data_directory: Path
    capture_count: int
    delay_between_captures: int
    no_of_classes: int
    class_names: list[str]
    class_colors: dict[str, list[int]]
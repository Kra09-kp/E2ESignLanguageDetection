from src.sign_language_detection.components.capture_image import CaptureImage
from sign_language_detection.config.configuration import ConfigurationManager
from src.sign_language_detection.logger import logger
from sign_language_detection.exceptions import AppException

def main():
    try:
        config = ConfigurationManager()
        capture_image = CaptureImage(config)

        capture_image.run(num_images=5)
        
        logger.info("Image capture process completed.")
    except AppException as e:
        logger.error(f"Application error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
import cv2 as cv
import numpy as np
import uuid
import time
import os
from src.sign_language_detection.logger import logger
from src.sign_language_detection.exceptions import AppException
from src.sign_language_detection.config.configuration import ConfigurationManager

class CaptureImage:
    def __init__(self, config: ConfigurationManager) -> None:
        try:
            self.config = config.get_sign_language_config()
            os.makedirs(self.config.data_directory, exist_ok=True)
            self.sleep_time = self.config.delay_between_captures
            logger.info("Data will be saved to: " + str(self.config.data_directory))
            self.cap = cv.VideoCapture(self.config.camera_id)

            #initialize logger
            logger.print_banner()
            logger.capture("CaptureImage component initialized.")

            # verify camera access
            if not self.cap.isOpened():
                logger.capture_error("Camera", "Failed to open camera.")
                raise Exception("Failed to open camera.")
            else:
                logger.success("Camera accessed successfully.")
        
        
        except Exception as e:
            raise AppException(e) from e

    def capture(self,class_name) -> bool:
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    raise Exception("Failed to capture image from camera.")
                    

                # Display the frame
                cv.imshow('Capture Image', frame)
                #  generate unique filename
                key = cv.waitKey(0) & 0xFF

                if key == ord(' '):   # spacebar pressed
                    continue
                
                elif key == ord('s'):  # save with s
                    filename = f"{class_name}_{str(uuid.uuid4())}.jpg"
                    filepath = os.path.join(self.config.data_directory, filename)
                    cv.imwrite(filepath, frame)
                    logger.capture(f"Image captured and saved to {filepath}")
                    return True

                elif key == ord('q'):  # quit with q
                    logger.warning("Capture interrupted by user.")
                    return False
                    

            
        except Exception as e:
            logger.capture_error(class_name, str(e))
            return False
        
    def run(self,num_images:int):
        try:
            # start capture session
            # print(self.config.class_names)
            logger.capture_session_start(self.config.class_names,num_images,self.sleep_time)
            total_images = num_images * len(self.config.class_names)
            logger.info(f"Total images to capture: {total_images}")
            total_captured = 0
            for class_name in self.config.class_names:
                logger.capture_class_start(class_name, num_images)

                # create progress bar  for this class
                with logger.create_capture_progress(num_images,class_name) as progress:
                    class_task = progress.add_task(f"[green]Capturing images for {class_name}...", total=num_images)
                    class_captured = 0
                    for i in range(num_images):
                        
                        if self.capture(class_name):
                            class_captured += 1
                            total_captured += 1

                            progress.update(class_task, advance=1)
                            logger.capture_success(class_name, i+1)
                        # time.sleep(self.sleep_time)

                    logger.success(f"Captured {class_captured}/{num_images} images for class {class_name}")
                    logger.success(f"Total images captured so far: {total_captured}/{total_images}")
                
            logger.capture_session_complete(total_captured, len(self.config.class_names))
        except Exception as e:
            raise AppException(e) from e
        finally:
            self.cap.release()
            cv.destroyAllWindows()
            logger.info("Camera released and all windows closed.")
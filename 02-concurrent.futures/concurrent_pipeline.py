import os
import time
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
import psutil
import filters

# --------------------------------
# Worker function
# --------------------------------
def process_single_image(args):
    img_path, output_folder = args
    try:
        pid = os.getpid()

        # Get CPU core info (best effort)
        try:
            core_id = psutil.Process(pid).cpu_num()
            core_info = f"CPU Core ID: {core_id}"
        except Exception:
            core_info = "CPU Core ID: N/A"

        filename = os.path.basename(img_path)
        print(f"[{core_info} PID:{pid}] Processing image {filename}")

        with Image.open(img_path) as img:
            arr = np.array(img.convert("RGB"))

            # Image processing pipeline
            arr = filters.grayscale_conversion(arr)
            arr = filters.gaussian_blur(arr)
            arr = filters.sobel_edge_detection(arr)
            arr = filters.image_sharpening(arr)
            arr = filters.brightness_adjustment(arr, 1.2)

            Image.fromarray(arr).save(
                os.path.join(output_folder, f"proc_{filename}")
            )

        return True

    except Exception as e:
        print(f"[PID {os.getpid()}] Error processing {img_path}: {e}")
        return False


# --------------------------------
# Run concurrent.futures experiment
# --------------------------------
def run_test(image_list, output_dir, num_workers):
    tasks = [(p, output_dir) for p in image_list]

    start_time = time.time()

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_single_image, task) for task in tasks]

        # Ensure all tasks complete (dynamic scheduling)
        for _ in as_completed(futures):
            pass

    return time.time() - start_time
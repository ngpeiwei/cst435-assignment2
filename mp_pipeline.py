import os
import time
import numpy as np
from PIL import Image
from multiprocessing import Pool, current_process
import filters  

# --------------------------------
# Worker function
# --------------------------------
def process_single_image(args):
    img_path, output_folder = args
    try:
        # Get OS-assigned CPU core (Linux only)
        core_id = os.sched_getcpu()  
        pid = os.getpid()
        filename = os.path.basename(img_path)

        print(f"[CPU Core ID: {core_id} PID:{pid}] Processing image {filename}")

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
# Run multiprocessing experiment
# --------------------------------
def run_test(image_list, output_dir, num_cores):
    tasks = [(p, output_dir) for p in image_list]
    start_time = time.time()
    with Pool(processes=num_cores) as pool:
        # Dynamic scheduling for excellent load balancing
        list(pool.imap_unordered(process_single_image, tasks, chunksize=1))
    return time.time() - start_time

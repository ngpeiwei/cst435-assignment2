import os
import time
import csv
import numpy as np
from PIL import Image
from multiprocessing import Pool, current_process
import filters


# --------------------------------
# Worker function (PROCESS-LEVEL)
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


# --------------------------------
# Main entry point
# --------------------------------
if __name__ == "__main__":
    # random image size with 1000 images
    INPUT_DIR = "data/images"
    OUTPUT_DIR = "output_mp"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    images = [
        os.path.join(INPUT_DIR, f)
        for f in os.listdir(INPUT_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    # Testing: limit to first 25 images
    images = images[:25]

    process_counts = [1, 2, 4, 8]
    results = []

    print(f"Starting Multiprocessing Pipeline with {len(images)} images")

    for process in process_counts:
        print("\n--------------------------")
        print(f"Running with {process} processes")
        print("--------------------------")

        duration = run_test(images, OUTPUT_DIR, process)
        results.append({"process": process, "time": duration})

    # Output results
    print("\n========================================")
    print("Multiprocessing Performance Results")
    print("========================================")
    for r in results:
        print(f"Process: {r['process']} | Time: {r['time']:.2f} seconds")

    # Save CSV
    with open("performance_results_mp.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["process", "time"])
        writer.writeheader()
        writer.writerows(results)

    print("\nResults saved to performance_results_mp.csv")


# import os
# import time
# import csv
# import numpy as np
# from PIL import Image
# from multiprocessing import Pool, current_process
# import filters


# # --------------------------------
# # Worker function (PROCESS-LEVEL)
# # --------------------------------
# def process_single_image(args):
#     img_path, output_folder = args

#     try:
#         proc = current_process()
#         proc_name = proc.name

#         filename = os.path.basename(img_path)

#         # Minimal, meaningful logging
#         print(f"[Process {proc_name} PID:{proc.pid}] Processing image {filename}")

#         with Image.open(img_path) as img:
#             arr = np.array(img.convert("RGB"))

#             # Image processing pipeline
#             arr = filters.grayscale_conversion(arr)
#             arr = filters.gaussian_blur(arr)
#             arr = filters.sobel_edge_detection(arr)
#             arr = filters.image_sharpening(arr)
#             arr = filters.brightness_adjustment(arr, 1.2)

#             Image.fromarray(arr).save(
#                 os.path.join(output_folder, f"proc_{filename}")
#             )

#         return True

#     except Exception as e:
#         print(f"[PID {os.getpid()}] Error processing {img_path}: {e}")
#         return False


# # --------------------------------
# # Run multiprocessing experiment
# # --------------------------------
# def run_test(image_list, output_dir, num_cores):
#     tasks = [(p, output_dir) for p in image_list]

#     start_time = time.time()
#     with Pool(processes=num_cores) as pool:
#         # Dynamic scheduling for excellent load balancing
#         list(pool.imap_unordered(process_single_image, tasks, chunksize=1))

#     return time.time() - start_time


# # --------------------------------
# # Main entry point
# # --------------------------------
# if __name__ == "__main__":
#     INPUT_DIR = "data/images"
#     OUTPUT_DIR = "output_mp"
#     os.makedirs(OUTPUT_DIR, exist_ok=True)

#     images = [
#         os.path.join(INPUT_DIR, f)
#         for f in os.listdir(INPUT_DIR)
#         if f.lower().endswith((".jpg", ".jpeg", ".png"))
#     ]

#     # Testing: limit to first 25 images
#     images = images[:25]

#     process_counts = [1, 2, 4, 8]
#     results = []

#     print(f"Starting Multiprocessing Pipeline with {len(images)} images")

#     for process in process_counts:
#         print("\n--------------------------")
#         print(f"Running with {process} processes")
#         print("--------------------------")

#         duration = run_test(images, OUTPUT_DIR, process)
#         results.append({"process": process, "time": duration})

#     # Output results
#     print("\n========================================")
#     print("Multiprocessing Performance Results")
#     print("========================================")
#     for r in results:
#         print(f"Process: {r['process']} | Time: {r['time']:.2f} seconds")

#     # Save CSV
#     with open("performance_results_mp.csv", "w", newline="") as f:
#         writer = csv.DictWriter(f, fieldnames=["process", "time"])
#         writer.writeheader()
#         writer.writerows(results)

#     print("\nResults saved to performance_results_mp.csv")



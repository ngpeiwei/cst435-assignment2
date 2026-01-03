import os
import time
import csv
import numpy as np
from PIL import Image
from multiprocessing import Pool
import filters  # Custom image filters module


# 1. Worker function executed by each process
def process_single_image(args):
    """
    Each worker process executes this function.
    It loads one image, applies all filters, and saves the result.
    """
    img_path, output_folder = args
    try:
        # Extract image filename
        filename = os.path.basename(img_path)

        # Load image and convert to NumPy array
        with Image.open(img_path) as img:
            arr = np.array(img.convert('RGB'))

            # 2. Image processing pipeline (CPU-bound)
            arr = filters.brightness_adjustment(arr, 1.2)
            arr = filters.gaussian_blur(arr)
            arr = filters.image_sharpening(arr)
            arr = filters.sobel_edge_detection(arr)

            # Convert processed array back to image and save
            result_img = Image.fromarray(arr)
            result_img.save(os.path.join(output_folder, f"proc_{filename}"))

        return True

    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return False


# 3. Run multiprocessing test with given core count
def run_test(image_list, output_dir, num_cores):
    """
    Measures total execution time of the pipeline
    using a specified number of CPU cores.
    """
    tasks = [(p, output_dir) for p in image_list]

    start_time = time.time()

    # Create a pool of worker processes
    with Pool(processes=num_cores) as pool:
        pool.map(process_single_image, tasks)

    # Return total elapsed time
    return time.time() - start_time


# 4. Main execution entry
if __name__ == "__main__":

    # Input and output directories
    INPUT_DIR = "data/images"
    OUTPUT_DIR = "output_mp"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load all image file paths
    images = [
        os.path.join(INPUT_DIR, f)
        for f in os.listdir(INPUT_DIR)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]

    # Quick test: limit number of images
    images = images[:25]

    # 5. Test different numbers of CPU cores
    core_counts = [1, 2, 4]  # Adjust based on GCP VM specs
    results = []

    print(f"Starting Multiprocessing Pipeline with {len(images)} images...")

    for c in core_counts:
        print(f"Running with {c} cores...")
        duration = run_test(images, OUTPUT_DIR, c)
        results.append({'cores': c, 'time': duration})

    # 6. Display performance results
    print("\nMultiprocessing Performance Results")
    print("----------------------------------")
    for r in results:
        print(f"Cores: {r['cores']} | Time: {r['time']:.2f} seconds")

    # 7. Save performance results to CSV (optional but recommended)
    csv_file = "performance_results_mp.csv"
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['cores', 'time'])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {csv_file}. Use this file to create Excel graphs.")

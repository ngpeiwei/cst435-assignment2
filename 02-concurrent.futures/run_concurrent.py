import os
import csv
from concurrent_pipeline import run_test

if __name__ == "__main__":

    # --------------------------------
    # Configuration
    # --------------------------------
    DATA_FOLDERS = ["random_images", "small_images"]
    OUTPUT_ROOT = "output_concurrent"
    THREAD_COUNTS = [1, 2, 4, 8] 

    os.makedirs(OUTPUT_ROOT, exist_ok=True)

    # ------------------------------------------------
    # Run concurrent.futures experiments for each folder
    # ------------------------------------------------
    for folder in DATA_FOLDERS:
        INPUT_DIR = os.path.join("data", folder)
        OUTPUT_DIR = os.path.join(OUTPUT_ROOT, folder)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        images = [
            os.path.join(INPUT_DIR, f)
            for f in os.listdir(INPUT_DIR)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        print(f"\nStarting Concurrent Futures Pipeline with {len(images)} images from folder: {folder}")
        results = []

        for num_threads in THREAD_COUNTS:
            print("\n--------------------------")
            print(f"Running with {num_threads} threads")
            print("--------------------------")

            duration = run_test(images, OUTPUT_DIR, num_threads)
            results.append({"threads": num_threads, "time": duration})

        # Output results
        print("\n" + "=" * 80)
        print(f"Concurrent Futures Performance Results ({len(images)} images in '{folder}' dataset)")
        print("=" * 80)
        for r in results:
            print(f"Threads: {r['threads']} | Time: {r['time']:.2f} seconds")

        # Save CSV per folder
        csv_file = f"performance_results_{folder}_concurrent.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["threads", "time"])
            writer.writeheader()
            writer.writerows(results)

        print(f"\nResults saved to {csv_file}")
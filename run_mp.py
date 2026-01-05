import os
from mp_pipeline import run_test  
import csv

if __name__ == "__main__":  
    # --------------------------------
    # Configuration
    # --------------------------------
    DATA_FOLDERS = ["random_images", "small_images"]
    OUTPUT_ROOT = "output_mp"
    PROCESS_COUNTS = [1, 2, 4, 8]

    os.makedirs(OUTPUT_ROOT, exist_ok=True)

    # -----------------------------------------------
    # Run multiprocessing experiments for each folder
    # -----------------------------------------------
    for folder in DATA_FOLDERS:
        INPUT_DIR = os.path.join("data", folder)
        OUTPUT_DIR = os.path.join(OUTPUT_ROOT, folder)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        images = [
            os.path.join(INPUT_DIR, f)
            for f in os.listdir(INPUT_DIR)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        print(f"\nStarting Multiprocessing Pipeline with {len(images)} images from folder: {folder}")
        results = []

        for num_proc in PROCESS_COUNTS:
            print("\n--------------------------")
            print(f"Running with {num_proc} processes")
            print("--------------------------")

            duration = run_test(images, OUTPUT_DIR, num_proc)
            results.append({"process": num_proc, "time": duration})

        # Output results
        print("\n" + "="*80)
        print(f"Multiprocessing Performance Results ({len(images)} images in '{folder}' dataset)")
        print("="*80)
        for r in results:
            print(f"Process: {r['process']} | Time: {r['time']:.2f} seconds")

        # Save CSV per folder
        csv_file = f"performance_results_{folder}.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["process", "time"])
            writer.writeheader()
            writer.writerows(results)

        print(f"\nResults saved to {csv_file}")
## Assignment Overview
This project implements a parallel image processing pipeline in Python as part of the CST435 Parallel and Cloud Computing course. Two different parallel programming paradigms are explored and compared:
1. Multiprocessing Module
2. Concurrent.futures

The datasets used are retrieved from the Food-101 dataset in Kaggle (https://www.kaggle.com/datasets/dansbecker/food-101). The datasets are separated into two:
1. 3000 random image size (151 MB)
2. 3000 small image sizes (118 MB)

Both paradigms process these datasets separately using the same sequence of image filters. Then, the they are evaluated based on execution time, speedup, and efficiency analysis when executed on Google Cloud Platform (GCP) Compute Engine virtual machines.

## 🖼️ Image Processing Pipeline
Each image is processed independently through the following five filters:
1. **Grayscale Conversion** - Convert RGB images to grayscale using luminance formula
2. **Gaussian Blur** - Apply 3×3 Gaussian kernel for smoothing
3. **Edge Detection** - Sobel filter to detect edges
4. **Image Sharpening** - Enhance edges and details
5. **Brightness Adjustment** - Increase or decrease image brightness

All filters operate on individual pixels or small neighborhoods, making them suitable for parallel processing.

## Repo Structure

```bash
cst435-Assignment2/
│
├── 01-multiprocessing-module/
│   ├── data/                     # Image datasets (random_images, small_images)
│   ├── filters.py                # Shared image filter functions
│   ├── mp_pipeline.py            # Multiprocessing pipeline implementation
│   └── run_mp.py                 # Multiprocessing experiment runner
│
├── 02-concurrent-futures/
│   ├── data/                     # Image datasets (random_images, small_images)
│   ├── concurrent_pipeline.py    # Concurrent.futures pipeline implementation
│   ├── filters.py                # Shared image filter functions
│   └── run_concurrent.py         # Concurrent.futures experiment runner
│
└── README.md
```

To guarantee modularity, clarity, and equitable performance comparison, each paradigm is implemented in its own directory.

## ⚙️ Environment Setup
This assignment is designed and tested on Google Cloud Platform (GCP) using Compute Engine virtual machines. Follow the steps below to setup the environment.

### 1. GCP VM Instance Configuration
1. Navigate to the **Compute Engine** section in the Google Cloud Console.
2. Select **Create Instance**.
3. Machine Family: Select **General** purpose, **Series E2**.
4. Machine Type: Select **e2-standard-8 (8 vCPUs, 32 GB memory)**.
5. Boot Disk: Select Debian GNU/Linux 12 (bookworm) with 10 GB storage.
6. Firewall: Default settings are sufficient.

### 2. Deployment
1. Click Create to provision the resource.
2. Once the Status indicator turns green, click SSH to establish a secure terminal.

### 3. Python Dependency Installation
The Linux environment requires specific libraries for data manipulation and system resource monitoring.
Execute the following commands to update the package manager, activate a virtual environment, and install the necessary Python libraries:

**a. Update the package manager and activate a virtual environment**
```python
$ sudo apt update
$ sudo apt install -y python3-venv python3-pip
$ python3 -m venv venv
$ source venv/bin/activate
```

You should see:
```python
(venv) username@instance-name:~$
```

**b. Install the necessary Python libraries**
```python
$ pip install numpy pillow psutil
```

Dependencies verification (optional)
```python
$ python -c "import numpy, PIL, psutil; print('OK')"
```

## 🔗 Clone GitHub Repository
After installing setting up the environment and installing the dependencies, clone the repo with the following steps:
1. Click Code → HTTPS.
2. Copy the URL.
3. In the VM, execute the following commands to clone the repo and navigate into the correct directory:
```python
$ sudo apt install -y git
$ git clone https://github.com/ngpeiwei/cst435-assignment2.git
$ cd cst435-assignment2
```

## 🔗 Executing the Paradigms

### 1. Executing the Multiprocessing Module
1. Navigate to the multiprocessing folder
```python
$ cd 01-multiprocessing-module
```

2. Execute the runner file
```python
$ python run_mp.py
```

This will execute the image processing pipeline using different process counts and output performance results are saved to CSV files.

### 2. Executing the Concurrent.futures Module
1. Navigate to the concurrent.futures folder
```python
$ cd 02-concurrent-futures
```

2. Execute the runner file
```python
$ python run_concurrent.py
```

This will execute the same pipeline using executor-based parallelism and record execution times for different worker counts.

## 📊 Performance Evaluation
1. Experiments are conducted using different worker counts (1, 2, 4, and 8).
2. Each configuration is executed three times to obtain average execution time.
3. Speedup and efficiency are calculated and analyzed using Amdahl’s Law.
4. Results are saved as CSV files for comparison.

## 🔍 Observations
1. Parallel execution significantly reduces processing time compared to sequential execution.
2. Near-linear speedup is observed at moderate worker counts.
3. Performance gains diminish at higher worker counts due to overhead and system-level constraints.
4. Multiprocessing achieves better scalability for compute-intensive workloads compared to multithreading.

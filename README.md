

# Evaluate efficiency of Triangle Inequality in Hamming distance calculation

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)

This script evaluates the effectiveness of using the **triangle inequality** to optimize the search for the **minimum Hamming distance** in a group of binary vectors. It builds on a Locality-Sensitive Hashing (LSH) framework and focuses on **reducing unnecessary Hamming distance computations**.

## 🧠 Motivation

Computing all pairwise Hamming distances in large binary datasets is computationally expensive. This script explores how **triangle inequality** logic can help eliminate some comparisons, thus improving runtime without sacrificing accuracy.

## ⚙️ How It Works

1. **Locality-Sensitive Hashing (LSH)** is used to divide the binary vectors into candidate groups.
2. Within each group, instead of brute-force comparison, **triangle inequality** is applied:
   - If the inequality condition fails, the actual Hamming distance isn't computed.
3. The script counts how many distance checks were saved and reports the ratio of saved checks to total possible checks.

## 🛠️ Getting Started

### Prerequisites
- **Python 3.7+** (check with `python --version`)
- **pip** (Python package manager)

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/bar-kalandarov/min-hamming-tri.git
   cd min-hamming-tri
   ```

2. **Install dependencies**:
   ```bash
   pip install numpy
   ```

## 💻 Usage

```bash
python min_hamming_tri.py --vectors 1000 --length 32 --iterations 10 --samples 100
```

Example Output:
```text
Skipped pair rate is 70%
```

### Arguments:
| Flag           | Description                          | Required |
|----------------|--------------------------------------|----------|
| `--vectors`    | Number of binary vectors to generate | Yes      |
| `--length`     | Bit-length of each vector            | Yes      |
| `--iterations` | Number of LSH iterations             | Yes      |
| `--samples`    | Number of datasets to compare        | Yes      |

## 📊 Benchmark Results


| Vectors | Length | Iterations | Samples | Skipped Rate |
|---------|--------|------------|---------|--------------|
| 1,000   | 32     | 1          | 1,000   | 50%          | 
| 1,000   | 32     | 10         | 1,000   | 50%          | 
| 10,000  | 32     | 1          | 100     | 60%          | 
| 10,000  | 32     | 13         | 100     | 70%          | 


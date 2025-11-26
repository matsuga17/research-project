# Strategic Management Research Hub - Installation Guide

**Complete Setup Guide for Strategic Management Research**

Version: 3.0  
Last Updated: 2025-11-01

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Python Environment Setup](#python-environment-setup)
3. [Package Installation](#package-installation)
4. [Data Source Access](#data-source-access)
5. [Verification & Testing](#verification-testing)
6. [Troubleshooting](#troubleshooting)
7. [Platform-Specific Notes](#platform-specific-notes)

---

## System Requirements

### Minimum Requirements

- **Operating System**: macOS 10.15+, Windows 10+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher (3.10+ recommended)
- **RAM**: 8 GB minimum (16 GB recommended for large datasets)
- **Storage**: 10 GB free disk space (50 GB+ for full datasets)
- **Internet**: Stable connection for API access

### Recommended Setup

- **Python**: 3.10 or 3.11
- **RAM**: 16 GB or more
- **CPU**: Multi-core processor (4+ cores)
- **Storage**: SSD with 100 GB+ free space

---

## Python Environment Setup

### Step 1: Install Python

#### macOS

Python 3 is typically pre-installed. Verify version:

```bash
python3 --version
```

If not installed or version < 3.8, install via Homebrew:

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

#### Windows

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer and **check "Add Python to PATH"**
3. Verify installation:

```cmd
python --version
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### Step 2: Create Virtual Environment

**IMPORTANT**: Always use a virtual environment to avoid package conflicts.

#### macOS/Linux

```bash
# Navigate to your research directory
cd ~/Desktop/研究

# Create virtual environment
python3 -m venv research_env

# Activate environment
source research_env/bin/activate

# Verify activation (should show (research_env) in prompt)
which python
```

#### Windows

```cmd
# Navigate to your research directory
cd C:\Users\YourName\Desktop\研究

# Create virtual environment
python -m venv research_env

# Activate environment
research_env\Scripts\activate

# Verify activation
where python
```

**Deactivating**: Run `deactivate` when done.

---

## Package Installation

### Step 3: Install Core Packages

With your virtual environment activated:

```bash
# Upgrade pip first
pip install --upgrade pip

# Install core packages
pip install pandas numpy scipy matplotlib seaborn --break-system-packages

# Install statistical packages
pip install statsmodels linearmodels --break-system-packages

# Install machine learning packages
pip install scikit-learn --break-system-packages

# Install NLP packages
pip install nltk textblob --break-system-packages

# Install network analysis
pip install networkx python-louvain --break-system-packages

# Install data collection packages
pip install requests beautifulsoup4 lxml --break-system-packages

# Install file handling
pip install openpyxl xlrd xlsxwriter python-docx PyPDF2 --break-system-packages

# Install utilities
pip install tqdm ratelimit fuzzywuzzy python-Levenshtein pyyaml --break-system-packages
```

**For macOS users**: If you encounter `error: externally-managed-environment`, add `--break-system-packages` flag (already included above).

### Step 4: Install Optional Advanced Packages

```bash
# Causal inference
pip install econml dowhy --break-system-packages

# WRDS access (if you have subscription)
pip install wrds --break-system-packages

# Topic modeling
pip install gensim --break-system-packages

# Time series analysis
pip install arch --break-system-packages

# Jupyter notebooks
pip install jupyter notebook ipykernel --break-system-packages
```

### Step 5: Install Requirements File

Alternatively, use the provided requirements.txt:

```bash
pip install -r requirements.txt --break-system-packages
```

### Step 6: Download NLTK Data

Required for text analysis:

```python
# Run in Python
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

---

## Data Source Access

### WRDS (Compustat, CRSP, etc.)

**Requirement**: Institutional subscription

#### Setup WRDS Access

1. **Register for WRDS account** (through your university)
2. **Set up connection**:

```bash
# First-time setup
python
>>> import wrds
>>> db = wrds.Connection()
# Enter username and password when prompted
```

3. **Store credentials** (optional, for automation):

```bash
# Create .pgpass file (macOS/Linux)
echo "wrds-pgdata.wharton.upenn.edu:9737:wrds:YOUR_USERNAME:YOUR_PASSWORD" >> ~/.pgpass
chmod 600 ~/.pgpass
```

**Test connection**:

```python
import wrds
db = wrds.Connection()
result = db.raw_sql("SELECT * FROM comp.funda LIMIT 10")
print(result.head())
db.close()
```

### USPTO PatentsView API

**Free, no registration required**

**Test API access**:

```python
import requests

url = "https://api.patentsview.org/patents/query"
query = {
    "q": {"_gte": {"patent_date": "2020-01-01"}},
    "f": ["patent_id", "patent_date", "patent_title"],
    "o": {"per_page": 10}
}

response = requests.post(url, json=query)
print(response.json())
```

**Rate limits**: 45 requests per minute

### EDINET (Japan FSA)

**Free, no registration required**

**API endpoint**: `https://disclosure.edinet-fsa.go.jp/api/v1/`

**Example**:

```python
import requests
from datetime import datetime

# Get document list for a specific date
date = datetime(2024, 3, 31).strftime('%Y-%m-%d')
url = f"https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date={date}&type=2"

response = requests.get(url)
documents = response.json()
print(f"Found {len(documents['results'])} documents")
```

**Rate limits**: 1 request per second recommended

### World Bank API

**Free, no registration required**

**Example**:

```python
import requests

# Get GDP data for Japan
url = "http://api.worldbank.org/v2/country/jpn/indicator/NY.GDP.MKTP.CD"
params = {
    "format": "json",
    "date": "2010:2023"
}

response = requests.get(url, params=params)
data = response.json()
print(data[1][:5])  # First 5 years
```

### SEC EDGAR

**Free, requires User-Agent header**

```python
import requests

headers = {
    "User-Agent": "Your Name your.email@university.edu"  # REQUIRED
}

# Get company CIK
url = "https://www.sec.gov/cgi-bin/browse-edgar"
params = {"action": "getcompany", "CIK": "0000320193", "type": "10-K", "output": "xml"}

response = requests.get(url, params=params, headers=headers)
print(response.text)
```

**Rate limits**: 10 requests per second maximum

---

## Verification & Testing

### Step 7: Verify Installation

Create a test script `verify_install.py`:

```python
"""
Verification script for Strategic Management Research Hub
Tests all critical packages and data source access.
"""

import sys

def test_package(package_name):
    """Test if a package can be imported."""
    try:
        __import__(package_name)
        print(f"✓ {package_name}")
        return True
    except ImportError:
        print(f"✗ {package_name} - NOT INSTALLED")
        return False

print("=" * 80)
print("VERIFYING INSTALLATION")
print("=" * 80)

print("\nCore Packages:")
print("-" * 80)
core_packages = [
    'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn',
    'statsmodels', 'linearmodels', 'sklearn'
]
core_results = [test_package(pkg) for pkg in core_packages]

print("\nNLP Packages:")
print("-" * 80)
nlp_packages = ['nltk', 'textblob']
nlp_results = [test_package(pkg) for pkg in nlp_packages]

print("\nNetwork Analysis:")
print("-" * 80)
network_packages = ['networkx']
network_results = [test_package(pkg) for pkg in network_packages]

print("\nData Collection:")
print("-" * 80)
data_packages = ['requests', 'bs4']
data_results = [test_package(pkg) for pkg in data_packages]

print("\nFile Handling:")
print("-" * 80)
file_packages = ['openpyxl']
file_results = [test_package(pkg) for pkg in file_packages]

# Summary
all_results = core_results + nlp_results + network_results + data_results + file_results
total = len(all_results)
passed = sum(all_results)

print("\n" + "=" * 80)
print(f"RESULT: {passed}/{total} packages installed successfully")
if passed == total:
    print("✓ Installation complete! Ready to start research.")
else:
    print("⚠ Some packages missing. Review installation steps above.")
print("=" * 80)
```

Run verification:

```bash
python verify_install.py
```

### Step 8: Test Sample Scripts

```bash
# Test data collectors
python scripts/data_collectors.py

# Test network analyzer
python scripts/network_analyzer.py

# Test text analyzer
python scripts/text_analyzer.py
```

---

## Troubleshooting

### Common Issues

#### Issue 1: `error: externally-managed-environment` (macOS)

**Solution**: Add `--break-system-packages` flag to pip install commands:

```bash
pip install pandas --break-system-packages
```

**Alternative**: Use virtual environment (recommended):

```bash
python3 -m venv research_env
source research_env/bin/activate
pip install pandas  # No flag needed in venv
```

#### Issue 2: `ModuleNotFoundError` after installation

**Cause**: Wrong Python interpreter or environment not activated

**Solution**:

```bash
# Check which Python you're using
which python
# Should point to your virtual environment

# Verify packages are installed in correct location
pip list

# If wrong environment, activate correct one:
source research_env/bin/activate  # macOS/Linux
research_env\Scripts\activate     # Windows
```

#### Issue 3: NLTK data not found

**Solution**:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

#### Issue 4: WRDS connection fails

**Error**: `psycopg2.OperationalError: could not connect to server`

**Solutions**:

1. **Check credentials**:
   ```python
   import wrds
   db = wrds.Connection(wrds_username='YOUR_USERNAME')
   ```

2. **Verify institutional access**:
   - Check with your university library
   - Confirm WRDS subscription is active

3. **Network issues**:
   - Try from campus network
   - Configure VPN if accessing remotely

#### Issue 5: API rate limit errors

**Error**: `429 Too Many Requests`

**Solution**: Add rate limiting:

```python
import time
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=1, period=1)  # 1 call per second
def make_api_request(url):
    return requests.get(url)
```

#### Issue 6: Memory errors with large datasets

**Error**: `MemoryError` or `Killed`

**Solutions**:

1. **Process in chunks**:
   ```python
   for chunk in pd.read_csv('large_file.csv', chunksize=10000):
       process(chunk)
   ```

2. **Use efficient data types**:
   ```python
   df = pd.read_csv('file.csv', dtype={'id': 'int32', 'value': 'float32'})
   ```

3. **Increase swap space** (Linux):
   ```bash
   sudo fallocate -l 8G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

#### Issue 7: SSL certificate errors

**Error**: `[SSL: CERTIFICATE_VERIFY_FAILED]`

**Solution** (macOS):

```bash
# Install certificates
/Applications/Python\ 3.11/Install\ Certificates.command
```

---

## Platform-Specific Notes

### macOS

**Python Location**:
- System Python: `/usr/bin/python3`
- Homebrew Python: `/usr/local/bin/python3` or `/opt/homebrew/bin/python3` (M1/M2)

**Common Issues**:
- Use `python3` and `pip3` explicitly
- Add `--break-system-packages` for system-wide installs
- Install Xcode Command Line Tools: `xcode-select --install`

**File Paths**:
```python
# Use pathlib for cross-platform compatibility
from pathlib import Path
data_path = Path.home() / 'Desktop' / '研究' / 'data'
```

### Windows

**Python Location**:
- Typically: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe`

**Common Issues**:
- Ensure "Add Python to PATH" was checked during installation
- Use `python` (not `python3`)
- File paths: Use forward slashes or raw strings
  ```python
  path = r'C:\Users\Name\Desktop\研究\data'
  # or
  path = 'C:/Users/Name/Desktop/研究/data'
  ```

**Line Endings**: Git may convert line endings. Set:
```bash
git config --global core.autocrlf true
```

### Linux

**Python Installation**:
```bash
# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv python3-pip

# Fedora/RHEL
sudo dnf install python3.11 python3-pip
```

**Permission Issues**:
- Never use `sudo pip install` (use virtual environment)
- For system packages: `sudo apt install python3-package-name`

---

## Next Steps

After successful installation:

1. **Read the Quick Start Tutorial**: `QUICKSTART_TUTORIAL.md`
2. **Review Sample Scripts**: `sample_scripts/` directory
3. **Configure Your Project**: Copy and edit `config_template.yaml`
4. **Run Example Study**: `python sample_scripts/japanese_firms_roa.py`

---

## Getting Help

### Resources

- **Documentation**: See `README.md` and `FAQ.md`
- **Sample Code**: Check `examples/` directory
- **Issue Tracker**: [GitHub Issues](https://github.com/yourusername/strategic-research-hub/issues)

### Community

- **Email Support**: your.email@university.edu
- **Slack/Discord**: [Link to community]

### Reporting Bugs

When reporting issues, include:

1. **Python version**: `python --version`
2. **Operating system**: macOS/Windows/Linux + version
3. **Package versions**: `pip list`
4. **Error message**: Full traceback
5. **Steps to reproduce**: Minimal example

---

## Appendix: Complete Package List

Full list of packages (as of 2025-11-01):

### Core Data Science

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | ≥1.5.0 | Data manipulation |
| numpy | ≥1.23.0 | Numerical computing |
| scipy | ≥1.10.0 | Scientific computing |
| matplotlib | ≥3.6.0 | Plotting |
| seaborn | ≥0.12.0 | Statistical visualization |

### Statistical Analysis

| Package | Version | Purpose |
|---------|---------|---------|
| statsmodels | ≥0.14.0 | Statistical models |
| linearmodels | ≥4.27 | Panel data models |
| scikit-learn | ≥1.2.0 | Machine learning |

### Causal Inference

| Package | Version | Purpose |
|---------|---------|---------|
| econml | ≥0.14.0 | Causal ML methods |
| dowhy | ≥0.11.0 | Causal inference |

### Text Analysis

| Package | Version | Purpose |
|---------|---------|---------|
| nltk | ≥3.8 | Natural language processing |
| textblob | ≥0.17.0 | Sentiment analysis |
| gensim | ≥4.3.0 | Topic modeling |

### Network Analysis

| Package | Version | Purpose |
|---------|---------|---------|
| networkx | ≥3.0 | Graph analysis |
| python-louvain | ≥0.16 | Community detection |

### Data Collection

| Package | Version | Purpose |
|---------|---------|---------|
| requests | ≥2.28.0 | HTTP requests |
| beautifulsoup4 | ≥4.11.0 | Web scraping |
| lxml | ≥4.9.0 | XML/HTML parser |
| wrds | ≥3.1.0 | WRDS database access |

### File Handling

| Package | Version | Purpose |
|---------|---------|---------|
| openpyxl | ≥3.1.0 | Excel files (.xlsx) |
| xlrd | ≥2.0.0 | Excel files (.xls) |
| xlsxwriter | ≥3.1.0 | Excel writing |
| python-docx | ≥1.0.0 | Word documents |
| PyPDF2 | ≥3.0.0 | PDF manipulation |

### Utilities

| Package | Version | Purpose |
|---------|---------|---------|
| tqdm | ≥4.65.0 | Progress bars |
| ratelimit | ≥2.2.1 | API rate limiting |
| fuzzywuzzy | ≥0.18.0 | Fuzzy string matching |
| python-Levenshtein | ≥0.21.0 | String distance (speedup) |
| pyyaml | ≥6.0 | YAML config files |

---

## License

This installation guide is part of the Strategic Management Research Hub.

**License**: MIT  
**Author**: Strategic Management Research Hub  
**Version**: 3.0  
**Date**: 2025-11-01

---

**Installation complete! Happy researching! 🚀**

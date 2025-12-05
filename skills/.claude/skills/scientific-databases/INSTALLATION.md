# Installation Guide - Scientific Databases

Complete setup instructions for the Scientific Databases integration toolkit.

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Detailed Setup](#detailed-setup)
- [API Keys & Authentication](#api-keys--authentication)
- [Testing Installation](#testing-installation)
- [Troubleshooting](#troubleshooting)
- [Platform-Specific Notes](#platform-specific-notes)

---

## System Requirements

### Minimum Requirements
- Python 3.9 or higher (Python 3.10+ recommended)
- 8GB RAM
- 5GB disk space
- Internet connection

### Recommended
- Python 3.10 or 3.11
- 16GB RAM (for large-scale analyses)
- SSD storage
- Stable broadband connection

### Operating Systems
- ✅ macOS (10.15+)
- ✅ Linux (Ubuntu 20.04+, other distributions)
- ✅ Windows 10/11

---

## Quick Installation

### 1. Clone or Download
```bash
# If using git
cd /path/to/your/skills/directory
# (Files should already be present if using Claude Projects)

# Or download and extract ZIP
```

### 2. Create Virtual Environment
```bash
# Navigate to scientific-databases directory
cd scientific-databases

# Create virtual environment
python3 -m venv venv

# Activate (choose your platform)
source venv/bin/activate              # macOS/Linux
venv\Scripts\activate                 # Windows
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Optional: Download NLP models
python -m nltk.downloader punkt vader_lexicon
```

### 4. Test Installation
```bash
# Run connectivity test
python tests/test_connectivity.py
```

---

## Detailed Setup

### Step 1: Verify Python Version

```bash
python3 --version
```

Should show Python 3.9 or higher. If not:

**macOS** (using Homebrew):
```bash
brew install python@3.10
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

**Windows**:
Download from [python.org](https://www.python.org/downloads/)

### Step 2: Virtual Environment Setup

**Why use virtual environment?**
- Isolates dependencies
- Prevents package conflicts
- Easy to remove/recreate

```bash
# Create
python3 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux

# Verify activation (should show venv path)
which python

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Core Dependencies

```bash
# Install all packages from requirements.txt
pip install -r requirements.txt

# This installs:
# - requests (HTTP requests)
# - biopython (biological databases)
# - pandas, numpy (data manipulation)
# - And many more...
```

### Step 4: Install Optional Components

#### For Text Analysis (PubMed, bioRxiv):
```bash
python -m nltk.downloader punkt
python -m nltk.downloader vader_lexicon
```

#### For Chemical Analysis (ChEMBL, PubChem):
```bash
pip install rdkit
# Note: RDKit can be challenging on some systems
# See Troubleshooting section if issues occur
```

#### For AlphaFold Bulk Downloads:
```bash
pip install google-cloud-bigquery gsutil
```

---

## API Keys & Authentication

### Required Registrations

#### 1. NCBI E-utilities (Recommended)
**Purpose**: PubMed, ClinVar, NCBI Gene access
**Rate limit**: 3 req/sec → 10 req/sec with key

**Setup**:
1. Create account: https://www.ncbi.nlm.nih.gov/account/
2. Navigate to Settings → API Key Management
3. Create new API key
4. Set environment variable:

```bash
# macOS/Linux - Add to ~/.bashrc or ~/.zshrc
export NCBI_API_KEY="your_key_here"

# Windows - Set via System Properties or:
setx NCBI_API_KEY "your_key_here"
```

#### 2. DrugBank (Required for DrugBank access)
**Purpose**: Drug information and interactions
**License**: Free for academic use

**Setup**:
1. Register: https://go.drugbank.com/releases/latest
2. Accept license agreement
3. Download credentials
4. Set environment variables:

```bash
# macOS/Linux
export DRUGBANK_USERNAME="your_username"
export DRUGBANK_PASSWORD="your_password"

# Windows
setx DRUGBANK_USERNAME "your_username"
setx DRUGBANK_PASSWORD "your_password"
```

### Optional Registrations

#### 3. COSMIC (Optional)
**Purpose**: Cancer genomics data
**License**: Academic or commercial license required

Register at: https://cancer.sanger.ac.uk/cosmic/register

#### 4. Ensembl (No registration)
Public API, but rate-limited. Consider running local mirror for heavy use.

---

## Testing Installation

### Quick Connectivity Test

```bash
# Test basic connectivity to key databases
python tests/test_connectivity.py
```

**Expected output**:
```
Testing Scientific Databases Connectivity...

✅ PubMed: OK
✅ UniProt: OK
✅ PDB: OK
✅ STRING: OK
✅ KEGG: OK
✅ ClinicalTrials: OK
✅ PubChem: OK

Results: 7/7 passed
```

### Detailed Testing

If pytest is installed:
```bash
# Run all tests
pytest tests/ -v

# Test specific category
pytest tests/test_proteins.py -v
```

### Manual Testing

Try individual databases:

```python
# Test PubMed
from Bio import Entrez
Entrez.email = "your@email.com"
handle = Entrez.esearch(db="pubmed", term="diabetes", retmax=5)
print(Entrez.read(handle))

# Test UniProt
import requests
r = requests.get("https://rest.uniprot.org/uniprotkb/P04637.json")
print(r.status_code)  # Should be 200

# Test STRING
r = requests.get("https://string-db.org/api/json/version")
print(r.json())
```

---

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'X'"
**Solution**: 
```bash
pip install X
# Or reinstall all dependencies
pip install -r requirements.txt
```

#### Issue: "Permission denied" on macOS/Linux
**Solution**:
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or install for user only
pip install --user -r requirements.txt
```

#### Issue: RDKit installation fails
**Solution**:

**Option 1** - Use conda (recommended for RDKit):
```bash
conda create -n scientific-db python=3.10
conda activate scientific-db
conda install -c conda-forge rdkit
pip install -r requirements.txt
```

**Option 2** - Skip RDKit (limits chemical analysis):
```bash
# Edit requirements.txt, comment out rdkit line
pip install -r requirements.txt
```

#### Issue: "SSL Certificate verification failed"
**Solution**:
```bash
# macOS - Install certificates
/Applications/Python\ 3.10/Install\ Certificates.command

# Or temporarily bypass (not recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### Issue: Slow API responses or timeouts
**Possible causes**:
1. Network connectivity issues
2. Database maintenance
3. Rate limiting (need API key)
4. Firewall blocking

**Solutions**:
- Check internet connection
- Add API keys (NCBI, etc.)
- Increase timeout values in scripts
- Check database status pages

#### Issue: "API key required" warnings
**Solution**:
Set environment variables as described in [API Keys section](#api-keys--authentication)

Verify with:
```bash
# macOS/Linux
echo $NCBI_API_KEY

# Windows
echo %NCBI_API_KEY%
```

---

## Platform-Specific Notes

### macOS

**Python installation**:
```bash
# Using Homebrew (recommended)
brew install python@3.10

# Verify
python3 --version
```

**Virtual environment location**:
```bash
# Typically in project directory
cd ~/path/to/scientific-databases
python3 -m venv venv
```

**Common issue**: SSL certificate errors
```bash
# Fix: Run certificate installer
/Applications/Python\ 3.10/Install\ Certificates.command
```

### Linux (Ubuntu/Debian)

**Python installation**:
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

**Additional dependencies**:
```bash
# For some packages
sudo apt install build-essential python3-dev
```

### Windows

**Python installation**:
1. Download from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation

**Virtual environment**:
```cmd
# Create
python -m venv venv

# Activate
venv\Scripts\activate

# Deactivate
deactivate
```

**Path issues**:
If `python` command not found:
```cmd
# Use full path
C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe
```

**PowerShell execution policy**:
If activation fails in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Advanced Configuration

### Custom Installation Locations

```bash
# Install to custom directory
pip install -r requirements.txt --target=/path/to/custom/dir

# Add to Python path
export PYTHONPATH="/path/to/custom/dir:$PYTHONPATH"
```

### Proxy Configuration

If behind corporate proxy:
```bash
# Set proxy environment variables
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="https://proxy.example.com:8080"

# Or use pip proxy
pip install --proxy=http://proxy.example.com:8080 -r requirements.txt
```

### Jupyter Notebook Integration

```bash
# Install Jupyter
pip install jupyter

# Register kernel
python -m ipykernel install --user --name=scientific-db

# Launch
jupyter notebook
```

---

## Verifying Installation

### Checklist

- [ ] Python 3.9+ installed and accessible
- [ ] Virtual environment created and activated
- [ ] All packages from requirements.txt installed
- [ ] NCBI API key set (recommended)
- [ ] DrugBank credentials set (if using)
- [ ] Connectivity test passes
- [ ] Can import key packages:
  ```python
  import requests
  import pandas
  from Bio import Entrez
  ```

### Getting Help

If issues persist:

1. **Check database status pages** - APIs may be down for maintenance
2. **Review error messages** - Often contain specific solutions
3. **Test with minimal example** - Isolate the problem
4. **Check package versions** - `pip list` to see installed versions
5. **Recreate virtual environment** - Sometimes cleanest solution

---

## Next Steps

After successful installation:

1. Read [QUICK_START.md](QUICK_START.md) for usage examples
2. Review [SKILL.md](SKILL.md) for database overview
3. Explore individual database documentation in subdirectories
4. Try the example workflows in QUICK_START.md

---

**Installation Issues?** Check the Troubleshooting section or review individual database documentation for specific requirements.

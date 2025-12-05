# Quick Start Guide - Scientific Databases

Get started with Scientific Databases in 5 minutes.

## Prerequisites

```bash
# Ensure installation is complete
pip install -r requirements.txt
python tests/test_connectivity.py  # Should pass
```

---

## 5-Minute Getting Started

### Example 1: Search Biomedical Literature (PubMed)

```python
from Bio import Entrez

# Set email (required by NCBI)
Entrez.email = "your.email@example.com"

# Search for recent diabetes papers
handle = Entrez.esearch(
    db="pubmed",
    term="diabetes mellitus[mh] AND 2024[dp]",
    retmax=10
)
results = Entrez.read(handle)

print(f"Found {results['Count']} papers")
print(f"PMIDs: {results['IdList']}")

# Get paper details
for pmid in results['IdList'][:3]:
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
    print(f"\n{handle.read()}")
```

### Example 2: Retrieve Protein Information (UniProt)

```python
import requests

# Get human TP53 protein
accession = "P04637"
url = f"https://rest.uniprot.org/uniprotkb/{accession}.json"

response = requests.get(url)
data = response.json()

# Extract key information
protein_name = data['proteinDescription']['recommendedName']['fullName']['value']
gene_name = data['genes'][0]['geneName']['value']
sequence = data['sequence']['value']

print(f"Protein: {protein_name}")
print(f"Gene: {gene_name}")
print(f"Sequence length: {len(sequence)} amino acids")
print(f"Sequence: {sequence[:50]}...")
```

### Example 3: Analyze Protein Networks (STRING)

```python
import requests
import json

# Get interaction network for TP53 and its partners
proteins = ["TP53", "MDM2", "ATM", "CHEK2"]
species = 9606  # Human

url = "https://string-db.org/api/json/network"
params = {
    "identifiers": "%0d".join(proteins),
    "species": species,
    "required_score": 700  # High confidence
}

response = requests.get(url, params=params)
network = response.json()

print(f"Found {len(network)} interactions")
for interaction in network[:5]:
    print(f"{interaction['preferredName_A']} <-> {interaction['preferredName_B']} (score: {interaction['score']})")
```

### Example 4: Search Bioactive Compounds (ChEMBL)

```python
from chembl_webresource_client.new_client import new_client

# Search for EGFR inhibitors
activity = new_client.activity

results = activity.filter(
    target_chembl_id='CHEMBL203',  # EGFR
    standard_type='IC50',
    standard_value__lte=100,  # IC50 ≤ 100 nM
    standard_units='nM'
).only(['molecule_chembl_id', 'standard_value', 'pchembl_value'])

print(f"Found {len(results)} potent EGFR inhibitors")
for result in results[:5]:
    print(f"Compound: {result['molecule_chembl_id']}, IC50: {result['standard_value']} nM")
```

### Example 5: Find Clinical Trials (ClinicalTrials.gov)

```python
import requests

# Search for recruiting diabetes trials
url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "query.cond": "diabetes",
    "filter.overallStatus": "RECRUITING",
    "pageSize": 10
}

response = requests.get(url, params=params)
data = response.json()

print(f"Found {data['totalCount']} recruiting diabetes trials")

for study in data['studies'][:5]:
    protocol = study['protocolSection']
    nct_id = protocol['identificationModule']['nctId']
    title = protocol['identificationModule']['briefTitle']
    print(f"\n{nct_id}: {title}")
```

---

## Common Workflows

### Workflow 1: Drug Target Discovery

**Goal**: Find and validate a drug target for type 2 diabetes

```python
# Step 1: Search GWAS Catalog for disease-associated genes
# (Simplified - actual implementation in gwas-database/scripts/)
disease_genes = ["TCF7L2", "PPARG", "KCNJ11"]

# Step 2: Get protein information from UniProt
import requests

proteins = {}
for gene in disease_genes:
    url = f"https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": f"gene:{gene} AND organism_id:9606",
        "format": "json",
        "size": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['results']:
        proteins[gene] = data['results'][0]['primaryAccession']

print(f"Found proteins: {proteins}")

# Step 3: Check for existing drugs (ChEMBL)
from chembl_webresource_client.new_client import new_client

target = new_client.target
activity = new_client.activity

for gene, uniprot_id in proteins.items():
    # Find ChEMBL target
    targets = target.filter(target_components__accession=uniprot_id)
    if targets:
        target_id = targets[0]['target_chembl_id']
        
        # Find drugs/compounds
        drugs = activity.filter(
            target_chembl_id=target_id,
            pchembl_value__gte=7  # High activity
        )
        print(f"\n{gene}: Found {len(drugs)} active compounds")

# Step 4: Search PubMed for recent literature
from Bio import Entrez
Entrez.email = "your@email.com"

for gene in disease_genes[:1]:  # Just first gene for example
    handle = Entrez.esearch(
        db="pubmed",
        term=f"{gene} AND diabetes AND drug target",
        retmax=5
    )
    results = Entrez.read(handle)
    print(f"\n{gene}: {results['Count']} papers on PubMed")
```

### Workflow 2: Variant Interpretation

**Goal**: Interpret a clinical genetic variant

```python
# Step 1: Get variant info from ClinVar
from Bio import Entrez
Entrez.email = "your@email.com"

# Search for variant (example: BRCA1 variant)
handle = Entrez.esearch(
    db="clinvar",
    term="BRCA1[gene] AND pathogenic[clinical significance]",
    retmax=1
)
results = Entrez.read(handle)
variant_id = results['IdList'][0]

# Get details
handle = Entrez.efetch(db="clinvar", id=variant_id, rettype="vcv", retmode="xml")
print(f"Variant ID: {variant_id}")
print(handle.read())

# Step 2: Check pharmacogenomics (simplified example)
# Real implementation would use ClinPGx database
gene = "BRCA1"
print(f"\nChecking pharmacogenomics for {gene}...")

# Step 3: Search relevant literature
handle = Entrez.esearch(
    db="pubmed",
    term=f"{gene} AND variant AND treatment",
    retmax=5
)
results = Entrez.read(handle)
print(f"Found {results['Count']} relevant papers")
```

### Workflow 3: Pathway Analysis

**Goal**: Analyze pathway enrichment for a gene list

```python
import requests

# Gene list from experiment
gene_list = ["TP53", "MDM2", "ATM", "CHEK2", "BRCA1", "BRCA2", "ATR"]

# Step 1: Get protein interactions (STRING)
url = "https://string-db.org/api/json/enrichment"
params = {
    "identifiers": "%0d".join(gene_list),
    "species": 9606
}

response = requests.get(url, params=params)
enrichment = response.json()

# Display enriched pathways
print("Enriched pathways:")
for item in enrichment[:5]:
    if item['category'] == 'KEGG':
        print(f"  {item['description']}: p-value = {item['p_value']:.2e}")

# Step 2: Get pathway details from KEGG
# (Simplified - actual implementation in kegg-database/scripts/)
pathway_id = "hsa04115"  # p53 signaling pathway
url = f"https://rest.kegg.jp/get/path:{pathway_id}"
response = requests.get(url)
print(f"\nKEGG pathway details:\n{response.text[:500]}...")
```

---

## Database-Specific Quick Examples

### PubMed (Literature)
```python
from Bio import Entrez
Entrez.email = "your@email.com"

# Search with filters
handle = Entrez.esearch(
    db="pubmed",
    term="cancer immunotherapy[tiab] AND 2024[dp] AND review[pt]",
    retmax=20
)
results = Entrez.read(handle)
```

### UniProt (Proteins)
```python
import requests

# Search by gene name
url = "https://rest.uniprot.org/uniprotkb/search"
params = {
    "query": "gene:EGFR AND organism_id:9606",
    "format": "json"
}
response = requests.get(url, params=params)
```

### STRING (Interactions)
```python
import requests

# Get network image
url = "https://string-db.org/api/image/network"
params = {
    "identifiers": "TP53%0dMDM2%0dATM",
    "species": 9606
}
response = requests.get(url, params=params)
with open("network.png", "wb") as f:
    f.write(response.content)
```

### PDB (Structures)
```python
from Bio.PDB import PDBList

# Download structure
pdbl = PDBList()
pdbl.retrieve_pdb_file("4HHB", pdir=".", file_format="pdb")
```

### AlphaFold (Predictions)
```python
from Bio.PDB import alphafold_db

# Get prediction
predictions = list(alphafold_db.get_predictions("P04637"))
cif_file = alphafold_db.download_cif_for(predictions[0], directory=".")
```

### ChEMBL (Bioactivity)
```python
from chembl_webresource_client.new_client import new_client

# Search compounds by similarity
similarity = new_client.similarity
results = similarity.filter(
    smiles='CC(=O)Oc1ccccc1C(=O)O',  # Aspirin
    similarity=85
)
```

### ClinicalTrials (Trials)
```python
import requests

# Search by condition and location
url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "query.cond": "lung cancer",
    "query.locn": "New York",
    "filter.overallStatus": "RECRUITING"
}
response = requests.get(url, params=params)
```

---

## Tips for Effective Use

### 1. Always Set Email for NCBI
```python
from Bio import Entrez
Entrez.email = "your.email@example.com"  # Required!
```

### 2. Use API Keys for Better Rate Limits
```bash
export NCBI_API_KEY="your_key_here"
```
```python
from Bio import Entrez
Entrez.api_key = "your_key_here"
```

### 3. Handle Errors Gracefully
```python
import requests

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

### 4. Cache Results Locally
```python
import pickle
from datetime import date

cache_file = f"results_{date.today()}.pkl"
if os.path.exists(cache_file):
    results = pickle.load(open(cache_file, "rb"))
else:
    results = fetch_from_api()
    pickle.dump(results, open(cache_file, "wb"))
```

### 5. Respect Rate Limits
```python
import time

for item in items:
    process(item)
    time.sleep(0.5)  # 0.5 second delay
```

---

## Next Steps

### Explore Individual Databases
Each database has detailed documentation:
```
[database-name]/SKILL_DOCUMENTATION.md
```

### Try Cross-Database Workflows
See [SKILL.md](SKILL.md) for comprehensive workflow examples.

### Read Full Documentation
- **SKILL.md** - Complete database overview
- **INSTALLATION.md** - Detailed setup
- **README.md** - Project overview

### Run Tests
```bash
python tests/test_connectivity.py
```

---

## Common Issues

**Import errors**: Ensure virtual environment is activated
```bash
source venv/bin/activate  # macOS/Linux
```

**API timeouts**: Check internet connection, add delays between requests

**Rate limiting**: Use API keys (NCBI, etc.)

**No results**: Verify database is online, check query syntax

---

## Getting Help

1. Check individual `SKILL_DOCUMENTATION.md` files
2. Review API documentation in `references/` directories
3. Test with minimal examples
4. Verify database availability

---

**Ready to Start!** Try the examples above, then explore individual database capabilities in their documentation.

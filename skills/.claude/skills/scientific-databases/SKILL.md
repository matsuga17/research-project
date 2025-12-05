---
name: scientific-databases
description: Unified access hub for 26+ scientific databases covering literature (PubMed, bioRxiv), proteins (UniProt, PDB, AlphaFold, STRING), genomics (NCBI Gene, Ensembl, ClinVar, COSMIC), drugs (DrugBank, ChEMBL, PubChem), pathways (KEGG, Reactome), clinical (ClinicalTrials, ClinPGx), and metabolomics (HMDB). Complete toolkit for systems biology, drug discovery, and multi-omics research.
---

# Scientific Databases - Unified Access Hub

A comprehensive integration of 26+ specialized scientific databases for biomedical and life sciences research.

## Overview

Scientific Databases provides seamless access to the most important databases across all domains of biomedical research. Each database is accessible through optimized APIs, Python clients, and comprehensive documentation. The hub supports cross-database workflows, multi-omics integration, and end-to-end research pipelines.

**Version**: 1.0  
**Total Databases**: 26  
**Coverage**: Literature • Proteins • Genomics • Drugs • Pathways • Clinical • Metabolomics

---

## Core Database Categories

### 1. Literature Databases (01-literature/)

Access to biomedical literature and preprints.

**Databases**:
- **PubMed** - 35M+ citations, systematic reviews, E-utilities API
- **bioRxiv** - Life sciences preprints, recent research

**Use Cases**:
- Literature reviews and systematic reviews
- Citation management
- Trend analysis
- Evidence gathering

**Documentation**: See individual `SKILL_DOCUMENTATION.md` files in subdirectories.

---

### 2. Protein Databases (02-proteins/)

Protein sequences, structures, and interactions.

**Databases**:
- **UniProt** - 250M+ protein sequences and annotations
- **PDB** - 200K+ experimental 3D structures
- **AlphaFold** - 200M+ AI-predicted structures
- **STRING** - 20B+ protein-protein interactions

**Use Cases**:
- Protein sequence analysis
- Structure-based drug design
- Interaction network analysis
- Functional annotation

**Documentation**: See `02-proteins/*/SKILL_DOCUMENTATION.md`

---

### 3. Genomics & Gene Databases (03-genomics/)

Gene information, variants, and expression data.

**Databases**:
- **NCBI Gene** - Gene-specific information, all organisms
- **Ensembl** - Genome annotation, 250+ species
- **ENA** - Nucleotide sequences and sequencing data
- **GEO** - Gene expression datasets
- **GWAS Catalog** - Genome-wide association studies
- **ClinVar** - Clinical genetic variants
- **COSMIC** - Cancer somatic mutations

**Use Cases**:
- Gene function analysis
- Variant interpretation
- Expression profiling
- Disease genetics

**Documentation**: See `03-genomics/*/SKILL_DOCUMENTATION.md`

---

### 4. Drug & Chemical Databases (04-drugs/)

Drug information, bioactive compounds, and chemical structures.

**Databases**:
- **DrugBank** - 13K+ drugs and targets
- **ChEMBL** - 2M+ bioactive compounds
- **PubChem** - 110M+ chemical compounds
- **ZINC** - Commercially available compounds
- **FDA** - FDA-approved drugs and labels

**Use Cases**:
- Drug discovery
- SAR analysis
- Drug-drug interactions
- Target identification

**Documentation**: See `04-drugs/*/SKILL_DOCUMENTATION.md`

---

### 5. Pathway & Systems Databases (05-pathways/)

Biological pathways and systems-level data.

**Databases**:
- **KEGG** - Metabolic and signaling pathways
- **Reactome** - Curated biological pathways
- **Open Targets** - Target-disease associations

**Use Cases**:
- Pathway enrichment analysis
- Systems biology
- Mechanism of action studies
- Drug repurposing

**Documentation**: See `05-pathways/*/SKILL_DOCUMENTATION.md`

---

### 6. Clinical & Translational Databases (06-clinical/)

Clinical trials, pharmacogenomics, and translational data.

**Databases**:
- **ClinicalTrials.gov** - 450K+ clinical trials
- **ClinPGx** - Pharmacogenomics recommendations

**Use Cases**:
- Patient matching to trials
- Drug safety assessment
- Personalized medicine
- Clinical research

**Documentation**: See `06-clinical/*/SKILL_DOCUMENTATION.md`

---

### 7. Metabolomics Databases (07-metabolomics/)

Human metabolites and metabolomics data.

**Databases**:
- **HMDB** - 220K+ human metabolites
- **Metabolomics Workbench** - Experimental metabolomics data

**Use Cases**:
- Metabolite identification
- Pathway analysis
- Biomarker discovery
- Metabolic profiling

**Documentation**: See `07-metabolomics/*/SKILL_DOCUMENTATION.md`

---

### 8. Patent Database (08-patents/)

Intellectual property and innovation tracking.

**Databases**:
- **USPTO** - U.S. patents and trademarks

**Use Cases**:
- Prior art searches
- Competitive intelligence
- Innovation tracking

**Documentation**: See `08-patents/uspto/SKILL_DOCUMENTATION.md`

---

## Quick Database Selector

**Choose databases based on your research objective:**

| Research Goal | Primary Database | Supporting Databases |
|--------------|------------------|---------------------|
| **Literature Review** | PubMed | bioRxiv |
| **Protein Function** | UniProt | PDB, AlphaFold, STRING |
| **Drug Discovery** | ChEMBL, DrugBank | PubChem, ZINC |
| **Gene Analysis** | NCBI Gene, Ensembl | GEO, GWAS Catalog |
| **Variant Interpretation** | ClinVar | COSMIC (cancer) |
| **Pathway Analysis** | KEGG, Reactome | STRING, Open Targets |
| **Clinical Research** | ClinicalTrials.gov | ClinVar, ClinPGx |
| **Metabolomics** | HMDB | Metabolomics Workbench |

---

## Cross-Database Workflows

### Workflow 1: Drug Target Discovery

**Objective**: Identify and validate a drug target for a disease

```python
# Step 1: Find disease genes (GWAS Catalog)
from genomics.gwas.scripts import search_disease_genes
genes = search_disease_genes("type 2 diabetes")

# Step 2: Get protein info (UniProt)
from proteins.uniprot.scripts import get_protein_info
proteins = [get_protein_info(g) for g in genes]

# Step 3: Find structures (PDB/AlphaFold)
from proteins.pdb.scripts import search_structures
structures = search_structures(proteins[0])

# Step 4: Find inhibitors (ChEMBL)
from drugs.chembl.scripts import find_inhibitors
inhibitors = find_inhibitors(proteins[0])

# Step 5: Check trials (ClinicalTrials)
from clinical.clinicaltrials.scripts import search_trials
trials = search_trials(drug=inhibitors[0])
```

### Workflow 2: Systems Biology Analysis

**Objective**: Understand pathway dysregulation

```python
# Step 1: Get expression data (GEO)
from genomics.geo.scripts import download_dataset
deg_list = download_dataset("GSE12345")

# Step 2: Protein interactions (STRING)
from proteins.string.scripts import get_network
network = get_network(deg_list, confidence=700)

# Step 3: Pathway enrichment (KEGG)
from pathways.kegg.scripts import pathway_enrichment
enriched = pathway_enrichment(deg_list)

# Step 4: Find targets (Open Targets)
from pathways.opentargets.scripts import find_targets
targets = find_targets(enriched[0])
```

### Workflow 3: Variant Interpretation

**Objective**: Clinical interpretation of genetic variants

```python
# Step 1: Get variant info (ClinVar)
from genomics.clinvar.scripts import get_variant
variant = get_variant("rs121913529")

# Step 2: Check function (Ensembl)
from genomics.ensembl.scripts import predict_effect
effect = predict_effect(variant)

# Step 3: Pharmacogenomics (ClinPGx)
from clinical.clinpgx.scripts import get_recommendations
pgx = get_recommendations(variant['gene'])

# Step 4: Literature (PubMed)
from literature.pubmed.scripts import search_variant
papers = search_variant(variant['rsid'])
```

---

## Installation

### Core Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Additional downloads
python -m nltk.downloader punkt
```

See `INSTALLATION.md` for detailed setup instructions and troubleshooting.

---

## Quick Start

### Basic Usage Examples

```python
# Example 1: PubMed literature search
from literature.pubmed.scripts.pubmed_search import search_pubmed
results = search_pubmed("diabetes AND 2024[dp]", max_results=100)

# Example 2: UniProt protein retrieval
from proteins.uniprot.scripts.uniprot_client import get_protein
protein = get_protein("P04637")  # TP53

# Example 3: STRING network analysis
from proteins.string.scripts.string_api import string_network
network = string_network(["TP53", "MDM2"], species=9606, confidence=700)

# Example 4: ChEMBL bioactivity search
from drugs.chembl.scripts.chembl_queries import find_inhibitors
inhibitors = find_inhibitors("EGFR", IC50_max=100)

# Example 5: ClinicalTrials search
from clinical.clinicaltrials.scripts.ct_search import search_studies
trials = search_studies(condition="diabetes", status="RECRUITING")
```

---

## Testing

Comprehensive test suite for database connectivity:

```bash
# Run all tests
pytest tests/ -v

# Test specific category
pytest tests/test_proteins.py -v
pytest tests/test_genomics.py -v

# Quick connectivity test
python tests/test_connectivity.py
```

---

## Documentation Structure

Each database has comprehensive documentation:

```
[database-directory]/
├── SKILL_DOCUMENTATION.md  # Complete API reference
├── scripts/                # Python helper functions
├── references/            # Additional documentation
├── tests/                 # Database-specific tests
└── examples/              # Usage examples
```

**Access Documentation**:
- Overview: This file (SKILL.md)
- Installation: `INSTALLATION.md`
- Quick Start: `QUICK_START.md`
- Database Details: `[category]/[database]/SKILL_DOCUMENTATION.md`

---

## API Keys & Authentication

Some databases require registration:

**Required**:
- **DrugBank**: Free academic account
- **NCBI E-utilities**: API key (recommended)
- **COSMIC**: Academic/commercial license

**Optional** (increases rate limits):
- NCBI API key: 10 req/sec vs 3 req/sec

See `INSTALLATION.md` for setup instructions.

---

## Best Practices

### 1. ID Mapping
Use standardized identifiers:
- **Genes**: HGNC symbols, Ensembl IDs
- **Proteins**: UniProt accessions
- **Compounds**: InChI keys, PubChem CIDs
- **Pathways**: KEGG/Reactome IDs

### 2. Rate Limiting
- Add 0.5-1 second delays between requests
- Use API keys when available
- Batch queries when possible

### 3. Caching
- Save API responses locally
- Document database versions
- Include query timestamps

### 4. Error Handling
```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_robust_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1,
                  status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
```

---

## System Requirements

- Python 3.9, 3.10, or 3.11 (recommended: 3.10+)
- 8GB RAM minimum (16GB recommended for large analyses)
- Internet connection for API access
- macOS, Linux, or Windows

---

## Research Applications

### Typical Use Cases

1. **Drug Discovery Pipeline**
   - Target identification → structure retrieval → compound screening → clinical trial search

2. **Systems Biology Analysis**
   - Expression profiling → network analysis → pathway enrichment → literature review

3. **Clinical Genomics**
   - Variant calling → pathogenicity assessment → pharmacogenomics → trial matching

4. **Multi-Omics Integration**
   - Genomics + transcriptomics + proteomics + metabolomics → systems view

---

## Project Structure

```
scientific-databases/
├── SKILL.md (this file)
├── README.md
├── INSTALLATION.md
├── QUICK_START.md
├── requirements.txt
├── 01-literature/
│   ├── pubmed/
│   │   ├── SKILL_DOCUMENTATION.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── tests/
│   └── biorxiv/
├── 02-proteins/
│   ├── uniprot/
│   ├── pdb/
│   ├── alphafold/
│   └── string/
├── 03-genomics/
│   ├── gene/
│   ├── ensembl/
│   ├── ena/
│   ├── geo/
│   ├── gwas/
│   ├── clinvar/
│   └── cosmic/
├── 04-drugs/
│   ├── drugbank/
│   ├── chembl/
│   ├── pubchem/
│   ├── zinc/
│   └── fda/
├── 05-pathways/
│   ├── kegg/
│   ├── reactome/
│   └── opentargets/
├── 06-clinical/
│   ├── clinicaltrials/
│   └── clinpgx/
├── 07-metabolomics/
│   ├── hmdb/
│   └── metabolomics-workbench/
├── 08-patents/
│   └── uspto/
└── tests/ (integration tests)
```

---

## Support Resources

- **Installation Issues**: `INSTALLATION.md`
- **Usage Examples**: Individual `SKILL_DOCUMENTATION.md` files
- **API Documentation**: `[database]/references/api_reference.md`
- **Quick Start**: `QUICK_START.md`

---

## Citation

When using these databases in research, cite:
1. The specific databases used
2. Database versions and access dates
3. This integration toolkit (optional)

**Example**:
```
Data were retrieved from PubMed (NLM, 2024), UniProt Consortium (2023), 
and STRING database v12.0 (Szklarczyk et al., 2023) using the Scientific 
Databases integration toolkit.
```

---

## Version History

**v1.0 (2025-11-02)** - Current
- Initial integration of 26 databases
- Complete documentation
- Cross-database workflows
- Comprehensive testing suite

---

## Status Summary

| Category | Databases | Status |
|----------|-----------|--------|
| Literature | 2 | ✅ Complete |
| Proteins | 4 | ✅ Complete |
| Genomics | 7 | ✅ Complete |
| Drugs | 5 | ✅ Complete |
| Pathways | 3 | ✅ Complete |
| Clinical | 2 | ✅ Complete |
| Metabolomics | 2 | ✅ Complete |
| Patents | 1 | ✅ Complete |

**Overall**: ⚡ **100% Complete - Production Ready**

---

**For detailed information on each database, refer to the corresponding SKILL_DOCUMENTATION.md file in the database subdirectory.**

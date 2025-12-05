# Scientific Databases - Unified Access Hub

**Version 1.0** | **26 Databases** | **Production Ready**

A comprehensive integration of the most important scientific databases for biomedical and life sciences research.

## 🎯 What is This?

Scientific Databases provides unified access to 26+ specialized databases covering:

- 📖 **Literature**: PubMed, bioRxiv
- 🔬 **Proteins**: UniProt, PDB, AlphaFold, STRING  
- 🧬 **Genomics**: NCBI Gene, Ensembl, ClinVar, COSMIC, GEO, GWAS, ENA
- 💊 **Drugs**: DrugBank, ChEMBL, PubChem, ZINC, FDA
- 🗺️ **Pathways**: KEGG, Reactome, Open Targets
- 🏥 **Clinical**: ClinicalTrials.gov, ClinPGx
- 🧪 **Metabolomics**: HMDB, Metabolomics Workbench
- 📋 **Patents**: USPTO

Each database is accessible through optimized APIs and Python clients with comprehensive documentation.

## ⚡ Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Test connectivity
python tests/test_connectivity.py
```

```python
# Example: PubMed search
from literature.pubmed.scripts.pubmed_search import search_pubmed
results = search_pubmed("diabetes AND 2024[dp]", max_results=100)

# Example: UniProt protein retrieval
from proteins.uniprot.scripts.uniprot_client import get_protein
protein = get_protein("P04637")  # TP53

# Example: STRING network
from proteins.string.scripts.string_api import string_network
network = string_network(["TP53", "MDM2"], species=9606, confidence=700)
```

See [QUICK_START.md](QUICK_START.md) for detailed examples.

## 📚 Documentation

- **[SKILL.md](SKILL.md)** - Complete overview and database selector
- **[INSTALLATION.md](INSTALLATION.md)** - Setup and troubleshooting
- **[QUICK_START.md](QUICK_START.md)** - 5-minute getting started guide
- **Individual Databases** - See `[database]/SKILL_DOCUMENTATION.md` for details

## 🔬 Database Categories

### Literature (2)
- **PubMed** - 35M+ biomedical citations
- **bioRxiv** - Life sciences preprints

### Proteins (4)
- **UniProt** - 250M+ protein sequences
- **PDB** - 200K+ experimental structures
- **AlphaFold** - 200M+ AI-predicted structures
- **STRING** - 20B+ protein interactions

### Genomics (7)
- **NCBI Gene** - Gene information
- **Ensembl** - Genome annotation
- **ENA** - Nucleotide sequences
- **GEO** - Gene expression data
- **GWAS Catalog** - Disease associations
- **ClinVar** - Clinical variants
- **COSMIC** - Cancer mutations

### Drugs (5)
- **DrugBank** - 13K+ drugs and targets
- **ChEMBL** - 2M+ bioactive compounds
- **PubChem** - 110M+ chemicals
- **ZINC** - Virtual screening compounds
- **FDA** - Drug labels and approvals

### Pathways (3)
- **KEGG** - Metabolic pathways
- **Reactome** - Biological pathways
- **Open Targets** - Target-disease associations

### Clinical (2)
- **ClinicalTrials.gov** - 450K+ clinical trials
- **ClinPGx** - Pharmacogenomics

### Metabolomics (2)
- **HMDB** - 220K+ metabolites
- **Metabolomics Workbench** - Experimental data

### Patents (1)
- **USPTO** - U.S. patents

## 🎓 Use Cases

### Drug Discovery Pipeline
Target identification → Structure retrieval → Compound screening → Clinical trials

### Systems Biology
Expression profiling → Network analysis → Pathway enrichment → Literature review

### Clinical Genomics
Variant calling → Pathogenicity assessment → Pharmacogenomics → Trial matching

### Multi-Omics Integration
Genomics + Transcriptomics + Proteomics + Metabolomics → Systems view

## 🔧 System Requirements

- Python 3.9+ (recommended: 3.10+)
- 8GB RAM minimum (16GB recommended)
- Internet connection
- macOS, Linux, or Windows

## 📦 Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Optional: Download NLP models
python -m nltk.downloader punkt
```

See [INSTALLATION.md](INSTALLATION.md) for details.

## 🧪 Testing

```bash
# Quick connectivity test
python tests/test_connectivity.py

# Run all tests (if pytest installed)
pytest tests/ -v
```

## 🔑 API Keys

Some databases require registration:

**Required**:
- DrugBank: Free academic account
- NCBI: API key (recommended for rate limits)

**Optional**:
- COSMIC: Academic/commercial license

See [INSTALLATION.md](INSTALLATION.md) for setup.

## 📖 Cross-Database Workflows

### Workflow 1: Drug Target Discovery
```python
# Find disease genes → Get structures → Find inhibitors → Check trials
gwas_genes = search_gwas("type 2 diabetes")
protein = get_uniprot_info(gwas_genes[0])
structure = get_pdb_structure(protein)
inhibitors = find_chembl_inhibitors(protein)
trials = search_clinical_trials(drug=inhibitors[0])
```

### Workflow 2: Variant Interpretation
```python
# Get variant → Predict effect → Check pharmacogenomics → Find papers
variant = get_clinvar_variant("rs121913529")
effect = predict_ensembl_effect(variant)
pgx = get_clinpgx_recommendations(variant['gene'])
papers = search_pubmed_variant(variant['rsid'])
```

## 🤝 Contributing

This is a research tool collection. For issues or improvements:
1. Check individual database documentation
2. Verify API connectivity
3. Review error messages in verbose mode

## 📄 License

For research and educational use. Individual databases have their own licenses.

## 📚 Citation

When using in research:
```
Data retrieved using Scientific Databases v1.0 (2025), 
accessing [list specific databases used with versions].
```

Always cite the original databases - see individual SKILL_DOCUMENTATION.md files.

## 🔗 Quick Links

| Database | Type | Documentation |
|----------|------|---------------|
| PubMed | Literature | [docs](pubmed-database/SKILL_DOCUMENTATION.md) |
| UniProt | Proteins | [docs](uniprot-database/SKILL_DOCUMENTATION.md) |
| STRING | Interactions | [docs](string-database/SKILL_DOCUMENTATION.md) |
| ChEMBL | Drugs | [docs](chembl-database/SKILL_DOCUMENTATION.md) |
| KEGG | Pathways | [docs](kegg-database/SKILL_DOCUMENTATION.md) |
| ClinVar | Variants | [docs](clinvar-database/SKILL_DOCUMENTATION.md) |
| ClinicalTrials | Trials | [docs](clinicaltrials-database/SKILL_DOCUMENTATION.md) |

See [SKILL.md](SKILL.md) for complete database list.

---

**Status**: ⚡ Production Ready | **Version**: 1.0 | **Last Updated**: 2025-11-02

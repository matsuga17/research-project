#!/usr/bin/env python3
"""
Quick Connectivity Test for Scientific Databases
Tests basic connectivity to all major databases

Run: python tests/test_connectivity.py
"""

import sys
import requests
import time

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def test_database(name, url, timeout=10):
    """Test connectivity to a single database"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"{GREEN}✅ {name}: OK{RESET}")
            return True
        else:
            print(f"{RED}❌ {name}: HTTP {response.status_code}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}❌ {name}: {str(e)[:50]}{RESET}")
        return False

def main():
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}Scientific Databases - Connectivity Test{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    databases = {
        # Literature
        'PubMed': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=diabetes&retmax=1&retmode=json',
        'bioRxiv': 'https://api.biorxiv.org/details/biorxiv/2024-01-01/2024-01-07/0',
        
        # Proteins
        'UniProt': 'https://rest.uniprot.org/uniprotkb/search?query=gene:BRCA1&size=1&format=json',
        'PDB': 'https://data.rcsb.org/rest/v1/core/entry/4HHB',
        'AlphaFold': 'https://alphafold.ebi.ac.uk/api/prediction/P00520',
        'STRING': 'https://string-db.org/api/json/version',
        
        # Genomics
        'NCBI Gene': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=BRCA1&retmode=json',
        'Ensembl': 'https://rest.ensembl.org/lookup/symbol/homo_sapiens/BRCA1?content-type=application/json',
        'ClinVar': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1&retmode=json',
        
        # Drugs
        'PubChem': 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/property/MolecularFormula/JSON',
        'ChEMBL': 'https://www.ebi.ac.uk/chembl/api/data/status',
        
        # Pathways
        'KEGG': 'https://rest.kegg.jp/info/pathway',
        'Reactome': 'https://reactome.org/ContentService/data/query/R-HSA-109581',
        
        # Clinical
        'ClinicalTrials': 'https://clinicaltrials.gov/api/v2/studies?query.cond=diabetes&pageSize=1',
        
        # Metabolomics
        'HMDB': 'https://hmdb.ca/metabolites/HMDB0000122.xml',
    }
    
    passed = 0
    failed = 0
    
    for name, url in databases.items():
        if test_database(name, url):
            passed += 1
        else:
            failed += 1
        time.sleep(0.5)  # Rate limiting
    
    # Summary
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}Results:{RESET}")
    print(f"  Total: {passed + failed}")
    print(f"  {GREEN}Passed: {passed}{RESET}")
    print(f"  {RED}Failed: {failed}{RESET}")
    
    success_rate = (passed / (passed + failed) * 100) if (passed + failed) > 0 else 0
    print(f"  Success Rate: {success_rate:.1f}%")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    if failed == 0:
        print(f"{GREEN}🎉 All databases are accessible!{RESET}\n")
        return 0
    else:
        print(f"{YELLOW}⚠️  Some databases are not accessible.{RESET}")
        print(f"{YELLOW}   This may be due to:

{RESET}")
        print(f"   - Network connectivity issues")
        print(f"   - Database maintenance")
        print(f"   - Missing API keys (NCBI, etc.)")
        print(f"   - Firewall/proxy restrictions\n")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Test interrupted by user{RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{RED}Fatal error: {str(e)}{RESET}\n")
        sys.exit(1)

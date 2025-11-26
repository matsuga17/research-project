"""
Research Project - Shared Test Fixtures
=======================================
研究プロジェクト共通テストフィクスチャ

This conftest.py provides shared fixtures and utilities for all test modules.
Place module-specific fixtures in the respective tests/ directories.

Usage:
    Fixtures defined here are automatically available to all tests.
    No import required.

Author: Research Project
Date: 2025-11
"""

import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator, Dict, Any
from unittest.mock import Mock, MagicMock

import pytest
import pandas as pd
import numpy as np


# ====================
# Path Configuration
# ====================

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Add skills directories to path
SKILLS_DIR = PROJECT_ROOT / "skills" / "user"
for skill_dir in SKILLS_DIR.glob("*/"):
    if skill_dir.is_dir():
        sys.path.insert(0, str(skill_dir))
        scripts_dir = skill_dir / "scripts"
        if scripts_dir.exists():
            sys.path.insert(0, str(scripts_dir))


# ====================
# Environment Fixtures
# ====================

@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def data_dir() -> Path:
    """Return the data directory path."""
    return PROJECT_ROOT / "data"


@pytest.fixture(scope="session")
def databases_dir() -> Path:
    """Return the databases directory path."""
    return PROJECT_ROOT / "databases"


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory that is cleaned up after test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_csv(temp_dir: Path) -> Path:
    """Create a temporary CSV file path."""
    return temp_dir / "test_data.csv"


# ====================
# Sample Data Fixtures
# ====================

@pytest.fixture
def sample_panel_data() -> pd.DataFrame:
    """
    Generate sample panel data for testing.
    パネルデータ分析用サンプルデータ

    Structure: firm_id x year with financial metrics
    """
    np.random.seed(42)
    firms = ['FIRM_A', 'FIRM_B', 'FIRM_C', 'FIRM_D', 'FIRM_E']
    years = [2019, 2020, 2021, 2022, 2023]

    data = []
    for firm in firms:
        base_assets = np.random.uniform(1000, 10000)
        base_revenue = np.random.uniform(500, 5000)

        for i, year in enumerate(years):
            growth = 1 + np.random.uniform(-0.1, 0.2)
            data.append({
                'firm_id': firm,
                'year': year,
                'total_assets': base_assets * (1.05 ** i) * growth,
                'total_revenue': base_revenue * (1.03 ** i) * growth,
                'net_income': base_revenue * (1.03 ** i) * growth * np.random.uniform(0.05, 0.15),
                'employees': int(np.random.uniform(100, 10000)),
                'rd_expense': base_revenue * np.random.uniform(0.02, 0.10),
                'industry': np.random.choice(['Tech', 'Manufacturing', 'Finance']),
                'country': np.random.choice(['JP', 'US', 'KR', 'CN'])
            })

    return pd.DataFrame(data)


@pytest.fixture
def sample_financial_data() -> pd.DataFrame:
    """
    Generate sample financial statement data.
    財務諸表サンプルデータ
    """
    return pd.DataFrame({
        'company_id': ['C001', 'C002', 'C003', 'C004', 'C005'],
        'company_name': ['企業A', '企業B', '企業C', '企業D', '企業E'],
        'fiscal_year': [2023, 2023, 2023, 2023, 2023],
        'total_assets': [50000, 75000, 30000, 120000, 45000],
        'total_liabilities': [25000, 40000, 15000, 70000, 20000],
        'shareholders_equity': [25000, 35000, 15000, 50000, 25000],
        'revenue': [40000, 60000, 25000, 100000, 35000],
        'operating_income': [4000, 6000, 2500, 10000, 3500],
        'net_income': [2800, 4200, 1750, 7000, 2450],
    })


@pytest.fixture
def sample_time_series() -> pd.DataFrame:
    """
    Generate sample time series data.
    時系列サンプルデータ
    """
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')

    return pd.DataFrame({
        'date': dates,
        'value': np.cumsum(np.random.randn(len(dates))) + 100,
        'volume': np.random.randint(1000, 10000, len(dates))
    })


@pytest.fixture
def sample_edinet_response() -> Dict[str, Any]:
    """
    Sample EDINET API response for testing.
    EDINET APIサンプルレスポンス
    """
    return {
        'metadata': {
            'status': '200',
            'message': 'OK',
            'resultset': {'count': 3}
        },
        'results': [
            {
                'docID': 'S100ABC1',
                'secCode': '1234',
                'edinetCode': 'E12345',
                'filerName': 'テスト株式会社',
                'docDescription': '有価証券報告書',
                'submitDateTime': '2024-03-31 09:00',
                'docTypeCode': '120'
            },
            {
                'docID': 'S100ABC2',
                'secCode': '5678',
                'edinetCode': 'E56789',
                'filerName': 'サンプル株式会社',
                'docDescription': '有価証券報告書',
                'submitDateTime': '2024-03-31 10:00',
                'docTypeCode': '120'
            },
            {
                'docID': 'S100ABC3',
                'secCode': '9012',
                'edinetCode': 'E90123',
                'filerName': '例示株式会社',
                'docDescription': '四半期報告書',
                'submitDateTime': '2024-03-31 11:00',
                'docTypeCode': '140'
            }
        ]
    }


@pytest.fixture
def sample_sec_edgar_response() -> Dict[str, Any]:
    """
    Sample SEC EDGAR API response for testing.
    SEC EDGAR APIサンプルレスポンス
    """
    return {
        'cik': '320193',
        'entityType': 'operating',
        'sic': '3571',
        'sicDescription': 'Electronic Computers',
        'name': 'Apple Inc.',
        'tickers': ['AAPL'],
        'exchanges': ['Nasdaq'],
        'ein': '942404110',
        'fiscalYearEnd': '0930',
        'filings': {
            'recent': {
                'accessionNumber': ['0000320193-24-000081'],
                'filingDate': ['2024-02-02'],
                'form': ['10-K'],
                'primaryDocument': ['aapl-20231230.htm']
            }
        }
    }


# ====================
# Mock Fixtures
# ====================

@pytest.fixture
def mock_requests_session() -> MagicMock:
    """Create a mock requests Session."""
    session = MagicMock()
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {}
    session.get.return_value = response
    session.post.return_value = response
    return session


@pytest.fixture
def mock_api_response() -> MagicMock:
    """Create a generic mock API response."""
    response = MagicMock()
    response.status_code = 200
    response.ok = True
    response.headers = {'Content-Type': 'application/json'}
    return response


# ====================
# Database Fixtures
# ====================

@pytest.fixture
def sample_sqlite_db(temp_dir: Path) -> Path:
    """Create a sample SQLite database for testing."""
    import sqlite3

    db_path = temp_dir / "test_research.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create sample tables
    cursor.execute('''
        CREATE TABLE companies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            ticker TEXT,
            country TEXT,
            industry TEXT,
            founded_year INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE financials (
            id INTEGER PRIMARY KEY,
            company_id INTEGER,
            fiscal_year INTEGER,
            revenue REAL,
            net_income REAL,
            total_assets REAL,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    ''')

    # Insert sample data
    cursor.executemany(
        'INSERT INTO companies (name, ticker, country, industry, founded_year) VALUES (?, ?, ?, ?, ?)',
        [
            ('テスト株式会社', '1234', 'JP', 'Technology', 1990),
            ('Sample Corp', 'SMPL', 'US', 'Finance', 1985),
            ('Example Ltd', 'EXMP', 'UK', 'Manufacturing', 2000),
        ]
    )

    conn.commit()
    conn.close()

    return db_path


# ====================
# Utility Fixtures
# ====================

@pytest.fixture
def assert_dataframe_equal():
    """Fixture providing DataFrame equality assertion."""
    def _assert_equal(df1: pd.DataFrame, df2: pd.DataFrame, **kwargs):
        pd.testing.assert_frame_equal(df1, df2, **kwargs)
    return _assert_equal


@pytest.fixture
def date_range_fixture() -> Dict[str, str]:
    """Provide common date ranges for testing."""
    today = datetime.now()
    return {
        'today': today.strftime('%Y-%m-%d'),
        'yesterday': (today - timedelta(days=1)).strftime('%Y-%m-%d'),
        'last_week': (today - timedelta(days=7)).strftime('%Y-%m-%d'),
        'last_month': (today - timedelta(days=30)).strftime('%Y-%m-%d'),
        'last_year': (today - timedelta(days=365)).strftime('%Y-%m-%d'),
        'fiscal_year_start': f'{today.year}-04-01',
        'fiscal_year_end': f'{today.year + 1}-03-31',
    }


# ====================
# Markers Configuration
# ====================

def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "api: Tests requiring API access")
    config.addinivalue_line("markers", "database: Database tests")


# ====================
# Test Hooks
# ====================

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on path."""
    for item in items:
        # Auto-mark tests based on directory
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Mark tests in specific skill directories
        if "corporate-research-data-hub" in str(item.fspath):
            item.add_marker(pytest.mark.corporate)
        if "strategic-management" in str(item.fspath):
            item.add_marker(pytest.mark.strategic)
        if "us-corporate" in str(item.fspath):
            item.add_marker(pytest.mark.us)

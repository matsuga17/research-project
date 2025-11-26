"""
Generic Data Collection Script Template
Supports CSV, Excel, JSON, and API-based data collection
"""

import pandas as pd
import requests
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collection.log'),
        logging.StreamHandler()
    ]
)

class DataCollector:
    """Generic data collector with support for multiple sources and formats"""
    
    def __init__(self, project_name: str, output_dir: str = "collected_data"):
        self.project_name = project_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.collection_log = []
        
        logging.info(f"Initialized DataCollector for project: {project_name}")
    
    def collect_from_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Collect data from CSV file
        
        Args:
            file_path: Path to CSV file
            **kwargs: Additional arguments for pd.read_csv
        
        Returns:
            DataFrame with collected data
        """
        logging.info(f"Reading CSV from {file_path}")
        
        try:
            df = pd.read_csv(file_path, **kwargs)
            
            self._log_collection(
                source_type="CSV",
                source_path=file_path,
                records=len(df),
                columns=list(df.columns)
            )
            
            logging.info(f"Successfully loaded {len(df)} records with {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logging.error(f"Error reading CSV: {str(e)}")
            raise
    
    def collect_from_excel(self, file_path: str, sheet_name: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Collect data from Excel file
        
        Args:
            file_path: Path to Excel file
            sheet_name: Name of sheet to read (None = first sheet)
            **kwargs: Additional arguments for pd.read_excel
        
        Returns:
            DataFrame with collected data
        """
        logging.info(f"Reading Excel from {file_path}, sheet: {sheet_name}")
        
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
            
            self._log_collection(
                source_type="Excel",
                source_path=file_path,
                records=len(df),
                columns=list(df.columns),
                sheet=sheet_name
            )
            
            logging.info(f"Successfully loaded {len(df)} records from sheet '{sheet_name}'")
            return df
            
        except Exception as e:
            logging.error(f"Error reading Excel: {str(e)}")
            raise
    
    def collect_from_api(self, 
                         url: str, 
                         params: Optional[Dict] = None,
                         headers: Optional[Dict] = None,
                         method: str = "GET",
                         max_retries: int = 3,
                         retry_delay: int = 5) -> Dict:
        """
        Collect data from API with retry logic
        
        Args:
            url: API endpoint URL
            params: Query parameters
            headers: Request headers
            method: HTTP method (GET, POST)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        
        Returns:
            JSON response as dictionary
        """
        logging.info(f"Calling API: {url}")
        
        for attempt in range(max_retries):
            try:
                if method.upper() == "GET":
                    response = requests.get(url, params=params, headers=headers, timeout=30)
                elif method.upper() == "POST":
                    response = requests.post(url, json=params, headers=headers, timeout=30)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                data = response.json()
                
                self._log_collection(
                    source_type="API",
                    source_path=url,
                    records=len(data) if isinstance(data, list) else 1,
                    response_code=response.status_code
                )
                
                logging.info(f"API call successful (status {response.status_code})")
                return data
                
            except requests.exceptions.RequestException as e:
                logging.warning(f"API call attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    logging.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logging.error(f"API call failed after {max_retries} attempts")
                    raise
    
    def collect_from_multiple_csvs(self, file_pattern: str, concat: bool = True) -> pd.DataFrame:
        """
        Collect data from multiple CSV files matching a pattern
        
        Args:
            file_pattern: File pattern (e.g., "data/*.csv")
            concat: If True, concatenate all files into one DataFrame
        
        Returns:
            Single DataFrame if concat=True, otherwise list of DataFrames
        """
        files = list(Path().glob(file_pattern))
        logging.info(f"Found {len(files)} files matching pattern: {file_pattern}")
        
        if not files:
            raise FileNotFoundError(f"No files found matching: {file_pattern}")
        
        dataframes = []
        for file in files:
            df = self.collect_from_csv(str(file))
            dataframes.append(df)
        
        if concat:
            result = pd.concat(dataframes, ignore_index=True)
            logging.info(f"Concatenated {len(dataframes)} files into {len(result)} total records")
            return result
        else:
            return dataframes
    
    def save_data(self, df: pd.DataFrame, filename: str, format: str = "csv") -> None:
        """
        Save collected data to file
        
        Args:
            df: DataFrame to save
            filename: Output filename (without extension)
            format: Output format ('csv', 'excel', 'parquet')
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format.lower() == "csv":
            output_path = self.output_dir / f"{filename}_{timestamp}.csv"
            df.to_csv(output_path, index=False)
        elif format.lower() == "excel":
            output_path = self.output_dir / f"{filename}_{timestamp}.xlsx"
            df.to_excel(output_path, index=False)
        elif format.lower() == "parquet":
            output_path = self.output_dir / f"{filename}_{timestamp}.parquet"
            df.to_parquet(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logging.info(f"Saved data to {output_path}")
        
        # Save collection log
        log_path = self.output_dir / f"{filename}_collection_log_{timestamp}.json"
        with open(log_path, 'w') as f:
            json.dump(self.collection_log, f, indent=2)
        
        logging.info(f"Saved collection log to {log_path}")
    
    def _log_collection(self, **kwargs):
        """Internal method to log collection activity"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "project": self.project_name,
            **kwargs
        }
        self.collection_log.append(log_entry)
    
    def get_collection_summary(self) -> Dict:
        """Get summary of collection activities"""
        if not self.collection_log:
            return {"message": "No data collected yet"}
        
        total_records = sum(entry.get("records", 0) for entry in self.collection_log)
        source_types = set(entry.get("source_type") for entry in self.collection_log)
        
        summary = {
            "project": self.project_name,
            "total_sources": len(self.collection_log),
            "total_records": total_records,
            "source_types": list(source_types),
            "first_collection": self.collection_log[0]["timestamp"],
            "last_collection": self.collection_log[-1]["timestamp"]
        }
        
        return summary


# Example usage
if __name__ == "__main__":
    # Initialize collector
    collector = DataCollector(project_name="my_research_project")
    
    # Example 1: Collect from CSV
    # df = collector.collect_from_csv("data/sample.csv")
    
    # Example 2: Collect from Excel
    # df = collector.collect_from_excel("data/sample.xlsx", sheet_name="Sheet1")
    
    # Example 3: Collect from API (example: World Bank API)
    # api_data = collector.collect_from_api(
    #     url="https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD",
    #     params={"format": "json", "date": "2020:2023"}
    # )
    # df = pd.DataFrame(api_data[1])  # World Bank returns [metadata, data]
    
    # Example 4: Collect from multiple CSVs
    # df = collector.collect_from_multiple_csvs("data/year_*.csv")
    
    # Example 5: Save collected data
    # collector.save_data(df, filename="my_collected_data", format="csv")
    
    # Example 6: Get collection summary
    # summary = collector.get_collection_summary()
    # print(json.dumps(summary, indent=2))
    
    print("Data collector initialized. Uncomment examples above to use.")
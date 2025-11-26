"""
phase_executor.py

Phase-Specific Execution Module

This module allows executing individual phases of the research pipeline
independently, enabling flexible workflow management and debugging.

Key Features:
- Execute any phase (1-8) independently
- Resume from checkpoint
- Parallel phase execution
- Phase dependency validation
- State management

Usage:
    from phase_executor import PhaseExecutor
    
    # Execute specific phase
    executor = PhaseExecutor(state_dir='./state/')
    result = executor.execute_phase(phase=4, config=config)
    
    # Resume from checkpoint
    executor.resume_from_checkpoint()
    
    # Execute multiple phases
    executor.execute_phases(start_phase=1, end_phase=5)

Version: 4.0
Last Updated: 2025-11-02
"""

import pandas as pd
import numpy as np
import logging
import json
import pickle
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PhaseExecutor:
    """
    Execute research pipeline phases independently
    
    This class manages the execution of individual phases,
    handles state persistence, and validates dependencies.
    
    Attributes:
        state_dir: Directory for saving state
        checkpoints: Dictionary of phase checkpoints
        config: Pipeline configuration
    """
    
    PHASES = {
        1: 'Research Design',
        2: 'Data Collection',
        3: 'Data Integration',
        4: 'Panel Construction',
        5: 'Quality Assurance',
        6: 'Variable Construction',
        7: 'Statistical Analysis',
        8: 'Documentation'
    }
    
    # Phase dependencies (phase X requires phases Y to be completed)
    DEPENDENCIES = {
        1: [],
        2: [1],
        3: [1, 2],
        4: [1, 2, 3],
        5: [1, 2, 3, 4],
        6: [1, 2, 3, 4, 5],
        7: [1, 2, 3, 4, 5, 6],
        8: [1, 2, 3, 4, 5, 6, 7]
    }
    
    def __init__(self, state_dir: str = './state/', config: Optional[Dict] = None):
        """
        Initialize Phase Executor
        
        Args:
            state_dir: Directory to save/load state
            config: Pipeline configuration
        """
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = config or {}
        self.checkpoints = self.load_checkpoints()
        
        logger.info("PhaseExecutor initialized")
        logger.info(f"State directory: {self.state_dir}")
        logger.info(f"Completed phases: {self.get_completed_phases()}")
    
    # =========================================================================
    # State Management
    # =========================================================================
    
    def load_checkpoints(self) -> Dict[int, Dict]:
        """
        Load checkpoint state from disk
        
        Returns:
            Dictionary of phase checkpoints
        """
        checkpoint_file = self.state_dir / 'checkpoints.json'
        
        if checkpoint_file.exists():
            with open(checkpoint_file, 'r') as f:
                checkpoints = json.load(f)
            logger.info(f"Loaded checkpoints: {len(checkpoints)} phases completed")
            return {int(k): v for k, v in checkpoints.items()}
        else:
            logger.info("No existing checkpoints found")
            return {}
    
    def save_checkpoint(self, phase: int, data: Any, metadata: Dict = None):
        """
        Save phase checkpoint
        
        Args:
            phase: Phase number
            data: Phase output data
            metadata: Additional metadata
        """
        # Save data
        if isinstance(data, pd.DataFrame):
            data_file = self.state_dir / f'phase{phase}_data.pkl'
            data.to_pickle(data_file)
        elif isinstance(data, dict):
            data_file = self.state_dir / f'phase{phase}_data.pkl'
            with open(data_file, 'wb') as f:
                pickle.dump(data, f)
        else:
            data_file = self.state_dir / f'phase{phase}_data.pkl'
            with open(data_file, 'wb') as f:
                pickle.dump(data, f)
        
        # Save checkpoint metadata
        checkpoint = {
            'phase': phase,
            'phase_name': self.PHASES[phase],
            'timestamp': datetime.now().isoformat(),
            'data_file': str(data_file),
            'status': 'completed'
        }
        
        if metadata:
            checkpoint.update(metadata)
        
        self.checkpoints[phase] = checkpoint
        
        # Save all checkpoints
        checkpoint_file = self.state_dir / 'checkpoints.json'
        with open(checkpoint_file, 'w') as f:
            json.dump(self.checkpoints, f, indent=2)
        
        logger.info(f"✓ Phase {phase} checkpoint saved")
    
    def load_phase_data(self, phase: int) -> Any:
        """
        Load data from phase checkpoint
        
        Args:
            phase: Phase number
        
        Returns:
            Phase output data
        """
        if phase not in self.checkpoints:
            raise ValueError(f"Phase {phase} not completed yet")
        
        data_file = Path(self.checkpoints[phase]['data_file'])
        
        if not data_file.exists():
            raise FileNotFoundError(f"Data file not found: {data_file}")
        
        # Load based on file type
        if data_file.suffix == '.pkl':
            with open(data_file, 'rb') as f:
                data = pickle.load(f)
        else:
            raise ValueError(f"Unknown file type: {data_file.suffix}")
        
        logger.info(f"Loaded Phase {phase} data from {data_file}")
        
        return data
    
    def get_completed_phases(self) -> List[int]:
        """Get list of completed phases"""
        return sorted(self.checkpoints.keys())
    
    def is_phase_completed(self, phase: int) -> bool:
        """Check if phase is completed"""
        return phase in self.checkpoints
    
    def validate_dependencies(self, phase: int) -> bool:
        """
        Validate that all required phases are completed
        
        Args:
            phase: Phase to validate
        
        Returns:
            True if all dependencies met
        """
        required = self.DEPENDENCIES[phase]
        completed = self.get_completed_phases()
        
        missing = [p for p in required if p not in completed]
        
        if missing:
            logger.error(f"Phase {phase} requires phases {missing} to be completed first")
            return False
        
        return True
    
    def reset_from_phase(self, phase: int):
        """
        Reset all phases from specified phase onwards
        
        Args:
            phase: Starting phase to reset
        """
        phases_to_reset = [p for p in self.checkpoints.keys() if p >= phase]
        
        for p in phases_to_reset:
            # Remove data file
            data_file = Path(self.checkpoints[p]['data_file'])
            if data_file.exists():
                data_file.unlink()
            
            # Remove checkpoint
            del self.checkpoints[p]
        
        # Save updated checkpoints
        checkpoint_file = self.state_dir / 'checkpoints.json'
        with open(checkpoint_file, 'w') as f:
            json.dump(self.checkpoints, f, indent=2)
        
        logger.info(f"Reset phases {phases_to_reset}")
    
    # =========================================================================
    # Phase Execution
    # =========================================================================
    
    def execute_phase(self, phase: int, config: Optional[Dict] = None, 
                     force: bool = False) -> Dict[str, Any]:
        """
        Execute specific phase
        
        Args:
            phase: Phase number (1-8)
            config: Override configuration
            force: Force re-execution even if completed
        
        Returns:
            Phase results
        """
        if phase not in self.PHASES:
            raise ValueError(f"Invalid phase: {phase}. Must be 1-8.")
        
        # Update config if provided
        if config:
            self.config.update(config)
        
        # Check if already completed
        if not force and self.is_phase_completed(phase):
            logger.info(f"Phase {phase} already completed. Use force=True to re-execute.")
            return {'status': 'already_completed', 'phase': phase}
        
        # Validate dependencies
        if not self.validate_dependencies(phase):
            return {'status': 'failed', 'phase': phase, 'error': 'Dependencies not met'}
        
        logger.info("\n" + "=" * 80)
        logger.info(f"EXECUTING PHASE {phase}: {self.PHASES[phase]}")
        logger.info("=" * 80)
        
        try:
            # Execute phase-specific logic
            if phase == 1:
                result = self._execute_phase1_design()
            elif phase == 2:
                result = self._execute_phase2_collection()
            elif phase == 3:
                result = self._execute_phase3_integration()
            elif phase == 4:
                result = self._execute_phase4_panel()
            elif phase == 5:
                result = self._execute_phase5_quality()
            elif phase == 6:
                result = self._execute_phase6_variables()
            elif phase == 7:
                result = self._execute_phase7_analysis()
            elif phase == 8:
                result = self._execute_phase8_documentation()
            
            # Save checkpoint
            metadata = {
                'n_observations': len(result) if isinstance(result, pd.DataFrame) else None,
                'columns': list(result.columns) if isinstance(result, pd.DataFrame) else None
            }
            self.save_checkpoint(phase, result, metadata)
            
            logger.info(f"✓ Phase {phase} completed successfully")
            
            return {
                'status': 'success',
                'phase': phase,
                'data': result,
                'metadata': metadata
            }
        
        except Exception as e:
            logger.error(f"✗ Phase {phase} failed: {e}")
            
            import traceback
            logger.error(traceback.format_exc())
            
            return {
                'status': 'failed',
                'phase': phase,
                'error': str(e)
            }
    
    def execute_phases(self, start_phase: int = 1, end_phase: int = 8,
                      force: bool = False) -> Dict[int, Dict]:
        """
        Execute multiple phases sequentially
        
        Args:
            start_phase: Starting phase
            end_phase: Ending phase
            force: Force re-execution of completed phases
        
        Returns:
            Dictionary of phase results
        """
        results = {}
        
        for phase in range(start_phase, end_phase + 1):
            result = self.execute_phase(phase, force=force)
            results[phase] = result
            
            if result['status'] == 'failed':
                logger.error(f"Stopping execution at Phase {phase} due to failure")
                break
        
        return results
    
    def resume_from_checkpoint(self, start_phase: Optional[int] = None) -> Dict[int, Dict]:
        """
        Resume execution from last completed phase
        
        Args:
            start_phase: Optional phase to resume from (default: next uncompleted)
        
        Returns:
            Dictionary of phase results
        """
        completed = self.get_completed_phases()
        
        if not completed:
            logger.info("No checkpoints found. Starting from Phase 1.")
            return self.execute_phases(start_phase=1, end_phase=8)
        
        last_completed = max(completed)
        
        if start_phase is None:
            start_phase = last_completed + 1
        
        if start_phase > 8:
            logger.info("All phases completed.")
            return {}
        
        logger.info(f"Resuming from Phase {start_phase}")
        
        return self.execute_phases(start_phase=start_phase, end_phase=8)
    
    # =========================================================================
    # Phase-Specific Implementations
    # =========================================================================
    
    def _execute_phase1_design(self) -> Dict:
        """Execute Phase 1: Research Design"""
        design = {
            'research_question': self.config.get('research_question', ''),
            'hypotheses': self.config.get('hypotheses', []),
            'constructs': self.config.get('constructs', {}),
            'sample_criteria': self.config.get('sample_criteria', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Research Question: {design['research_question']}")
        
        for i, hyp in enumerate(design['hypotheses'], 1):
            logger.info(f"  H{i}: {hyp}")
        
        return design
    
    def _execute_phase2_collection(self) -> List[pd.DataFrame]:
        """Execute Phase 2: Data Collection"""
        # This would integrate with actual data collectors
        # For now, generate demo data
        
        logger.info("Collecting data from sources...")
        
        data_sources = self.config.get('data_sources', [])
        dataframes = []
        
        for source in data_sources:
            logger.info(f"  Collecting from: {source.get('name', 'Unknown')}")
            
            # Generate demo data
            n = source.get('params', {}).get('n_firms', 100)
            years = source.get('params', {}).get('years', range(2015, 2023))
            
            data = []
            for firm_id in range(1, n + 1):
                for year in years:
                    data.append({
                        'firm_id': f'FIRM{firm_id:04d}',
                        'year': year,
                        'variable1': np.random.randn(),
                        'variable2': np.random.randn()
                    })
            
            df = pd.DataFrame(data)
            dataframes.append(df)
            
            logger.info(f"    Collected: {len(df)} records")
        
        return dataframes
    
    def _execute_phase3_integration(self) -> pd.DataFrame:
        """Execute Phase 3: Data Integration"""
        # Load Phase 2 data
        dataframes = self.load_phase_data(2)
        
        if not isinstance(dataframes, list):
            dataframes = [dataframes]
        
        logger.info(f"Integrating {len(dataframes)} datasets...")
        
        # Merge all dataframes
        df = dataframes[0]
        for additional_df in dataframes[1:]:
            df = df.merge(additional_df, on=['firm_id', 'year'], how='inner')
        
        logger.info(f"  Integrated dataset: {len(df)} observations")
        
        return df
    
    def _execute_phase4_panel(self) -> pd.DataFrame:
        """Execute Phase 4: Panel Construction"""
        # Load Phase 3 data
        df = self.load_phase_data(3)
        
        logger.info("Constructing panel dataset...")
        
        # Set MultiIndex
        df = df.set_index(['firm_id', 'year']).sort_index()
        
        n_firms = df.index.get_level_values('firm_id').nunique()
        n_years = df.index.get_level_values('year').nunique()
        
        logger.info(f"  Firms: {n_firms}")
        logger.info(f"  Years: {n_years}")
        logger.info(f"  Total: {len(df)} firm-years")
        
        return df
    
    def _execute_phase5_quality(self) -> pd.DataFrame:
        """Execute Phase 5: Quality Assurance"""
        # Load Phase 4 data
        df = self.load_phase_data(4)
        
        logger.info("Performing quality checks...")
        
        # Missing value check
        missing = df.isnull().sum()
        if missing.sum() > 0:
            logger.warning(f"  Missing values detected:")
            for col in missing[missing > 0].index:
                logger.warning(f"    {col}: {missing[col]}")
        
        # Outlier detection
        from scipy.stats import zscore
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            outliers = (abs(zscore(df[col].dropna())) > 3).sum()
            if outliers > 0:
                logger.warning(f"  {col}: {outliers} outliers (|z| > 3)")
        
        logger.info("  Quality checks completed")
        
        return df
    
    def _execute_phase6_variables(self) -> pd.DataFrame:
        """Execute Phase 6: Variable Construction"""
        # Load Phase 5 data
        df = self.load_phase_data(5)
        
        logger.info("Constructing variables...")
        
        df = df.reset_index()
        
        # Example variable construction
        # (In practice, this would be more sophisticated)
        if 'variable1' in df.columns and 'variable2' in df.columns:
            df['interaction'] = df['variable1'] * df['variable2']
            logger.info("  ✓ interaction = variable1 * variable2")
        
        # Lagged variables
        df = df.sort_values(['firm_id', 'year'])
        df['variable1_lag1'] = df.groupby('firm_id')['variable1'].shift(1)
        logger.info("  ✓ variable1_lag1")
        
        df = df.set_index(['firm_id', 'year']).sort_index()
        
        logger.info(f"  Total variables: {len(df.columns)}")
        
        return df
    
    def _execute_phase7_analysis(self) -> Dict:
        """Execute Phase 7: Statistical Analysis"""
        # Load Phase 6 data
        df = self.load_phase_data(6)
        
        logger.info("Running statistical analysis...")
        
        methods = self.config.get('statistical_methods', ['descriptive'])
        results = {}
        
        for method in methods:
            logger.info(f"  Running: {method}")
            
            if method == 'descriptive':
                results['descriptive'] = df.describe()
            elif method == 'correlation':
                results['correlation'] = df.corr()
            # Add more methods as needed
        
        logger.info(f"  Completed {len(results)} analyses")
        
        return results
    
    def _execute_phase8_documentation(self) -> str:
        """Execute Phase 8: Documentation"""
        logger.info("Generating documentation...")
        
        # Load all phase results
        design = self.load_phase_data(1)
        analysis = self.load_phase_data(7)
        
        # Generate report
        report = f"""# Research Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Research Design

**Question**: {design.get('research_question', 'N/A')}

**Hypotheses**:
"""
        
        for i, hyp in enumerate(design.get('hypotheses', []), 1):
            report += f"{i}. {hyp}\n"
        
        report += "\n## Analysis Results\n\n"
        report += "(See detailed results in output files)\n"
        
        logger.info("  Documentation completed")
        
        return report
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    def get_phase_summary(self) -> pd.DataFrame:
        """
        Get summary of all phases
        
        Returns:
            DataFrame with phase information
        """
        summary = []
        
        for phase_num, phase_name in self.PHASES.items():
            completed = self.is_phase_completed(phase_num)
            
            checkpoint_time = None
            if completed:
                checkpoint_time = self.checkpoints[phase_num].get('timestamp')
            
            summary.append({
                'phase': phase_num,
                'name': phase_name,
                'completed': completed,
                'timestamp': checkpoint_time,
                'dependencies': ', '.join(map(str, self.DEPENDENCIES[phase_num]))
            })
        
        return pd.DataFrame(summary)
    
    def export_state(self, filepath: str):
        """
        Export complete state to file
        
        Args:
            filepath: Output file path
        """
        state = {
            'checkpoints': self.checkpoints,
            'config': self.config,
            'export_time': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"State exported: {filepath}")
    
    def import_state(self, filepath: str):
        """
        Import state from file
        
        Args:
            filepath: State file path
        """
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.checkpoints = {int(k): v for k, v in state['checkpoints'].items()}
        self.config = state['config']
        
        logger.info(f"State imported: {filepath}")


# =============================================================================
# Command Line Interface
# =============================================================================

def main():
    """Main function for CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Phase Executor v4.0')
    parser.add_argument('--phase', type=int, help='Execute specific phase (1-8)')
    parser.add_argument('--start', type=int, help='Start phase for range execution')
    parser.add_argument('--end', type=int, help='End phase for range execution')
    parser.add_argument('--resume', action='store_true', help='Resume from checkpoint')
    parser.add_argument('--config', type=str, help='Configuration file')
    parser.add_argument('--state-dir', type=str, default='./state/', help='State directory')
    parser.add_argument('--force', action='store_true', help='Force re-execution')
    parser.add_argument('--summary', action='store_true', help='Show phase summary')
    
    args = parser.parse_args()
    
    # Load config if provided
    config = {}
    if args.config:
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
    
    # Initialize executor
    executor = PhaseExecutor(state_dir=args.state_dir, config=config)
    
    # Show summary
    if args.summary:
        summary = executor.get_phase_summary()
        print("\n" + "=" * 80)
        print("PHASE SUMMARY")
        print("=" * 80)
        print(summary.to_string(index=False))
        return
    
    # Execute phases
    if args.resume:
        results = executor.resume_from_checkpoint()
    elif args.phase:
        results = executor.execute_phase(args.phase, force=args.force)
    elif args.start and args.end:
        results = executor.execute_phases(args.start, args.end, force=args.force)
    else:
        print("Please specify --phase, --start/--end, or --resume")
        return
    
    print("\n" + "=" * 80)
    print("EXECUTION COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    # Example usage
    print("=" * 80)
    print("PHASE EXECUTOR v4.0 - DEMO")
    print("=" * 80)
    
    # Demo configuration
    demo_config = {
        'research_question': 'Test research question',
        'hypotheses': ['H1: Test hypothesis'],
        'data_sources': [
            {'name': 'Source1', 'type': 'demo', 'params': {'n_firms': 50, 'years': range(2015, 2020)}}
        ],
        'statistical_methods': ['descriptive', 'correlation']
    }
    
    # Initialize executor
    executor = PhaseExecutor(state_dir='./demo_state/', config=demo_config)
    
    # Show phase summary
    print("\nPhase Summary:")
    print(executor.get_phase_summary().to_string(index=False))
    
    # Execute Phase 1
    print("\n" + "=" * 80)
    print("Executing Phase 1...")
    result = executor.execute_phase(1)
    
    if result['status'] == 'success':
        print("✓ Phase 1 completed successfully")
    else:
        print(f"✗ Phase 1 failed: {result.get('error')}")

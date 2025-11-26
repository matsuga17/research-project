#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theory Framework Setup: Interactive Theoretical Framework Configuration

Philosophical/Theoretical Foundation:
    This script embodies the dialectical integration of theory and empirical
    research. It guides researchers through the process of theoretical framework
    selection, construct conceptualization, and operationalization - the critical
    bridge between abstract theory and empirical measurement.
    
    Drawing on the philosophy of science, particularly the work of Lakatos (1970)
    on research programs and Kuhn (1962) on paradigms, this tool recognizes that
    theoretical choices have profound epistemological implications.

Theoretical Perspectives Supported:
    - Resource-Based View (RBV): Barney (1991), Wernerfelt (1984)
    - Transaction Cost Economics (TCE): Williamson (1985), Coase (1937)
    - Institutional Theory: DiMaggio & Powell (1983), Scott (1995)
    - Dynamic Capabilities: Teece et al. (1997), Eisenhardt & Martin (2000)

Usage:
    python theory_framework_setup.py --interactive
    python theory_framework_setup.py --theory rbv --output config.yaml

Author: Strategic Research Lab
License: MIT
Version: 1.0.0
Date: 2025-11-08
"""

import yaml
import argparse
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import json


class TheoryFramework:
    """
    Theoretical Framework Configuration System
    
    This class implements a dialectical approach to theory selection,
    recognizing that theoretical frameworks are not merely tools but
    embody distinct ontological and epistemological commitments.
    """
    
    # Theoretical frameworks with their philosophical foundations
    THEORIES = {
        'rbv': {
            'name': 'Resource-Based View',
            'key_scholars': ['Barney (1991)', 'Wernerfelt (1984)', 'Peteraf (1993)'],
            'ontology': 'Firms as heterogeneous bundles of resources',
            'epistemology': 'Empiricist - focuses on observable resource attributes',
            'core_concepts': [
                'VRIN Resources (Valuable, Rare, Inimitable, Non-substitutable)',
                'Sustained Competitive Advantage',
                'Resource Heterogeneity',
                'Resource Immobility',
                'Causal Ambiguity'
            ],
            'typical_constructs': {
                'independent': ['Resource uniqueness', 'Resource complementarity', 'Organizational capabilities'],
                'dependent': ['Competitive advantage', 'Firm performance', 'Profitability'],
                'mediator': ['Strategic flexibility', 'Innovation capacity'],
                'moderator': ['Industry dynamism', 'Competitive intensity', 'Market turbulence']
            },
            'measurement_considerations': [
                'Resources are often intangible and difficult to measure directly',
                'Need to establish VRIN criteria empirically',
                'Consider both resource stocks and flows',
                'Account for resource complementarities'
            ]
        },
        'tce': {
            'name': 'Transaction Cost Economics',
            'key_scholars': ['Williamson (1985)', 'Coase (1937)', 'Klein et al. (1978)'],
            'ontology': 'Economic organizations as governance structures',
            'epistemology': 'Rationalist - assumes bounded rationality and opportunism',
            'core_concepts': [
                'Asset Specificity',
                'Uncertainty',
                'Transaction Frequency',
                'Bounded Rationality',
                'Opportunism',
                'Governance Structures'
            ],
            'typical_constructs': {
                'independent': ['Asset specificity', 'Uncertainty', 'Transaction frequency'],
                'dependent': ['Governance choice', 'Vertical integration', 'Transaction costs'],
                'mediator': ['Opportunism risk', 'Coordination costs'],
                'moderator': ['Legal environment', 'Trust', 'Reputation mechanisms']
            },
            'measurement_considerations': [
                'Asset specificity requires multiple dimensions (site, physical, human)',
                'Uncertainty can be environmental or behavioral',
                'Governance structures need categorical or continuous measures',
                'Consider ex-ante and ex-post transaction costs separately'
            ]
        },
        'institutional': {
            'name': 'Institutional Theory',
            'key_scholars': ['DiMaggio & Powell (1983)', 'Scott (1995)', 'Meyer & Rowan (1977)'],
            'ontology': 'Organizations as socially constructed entities',
            'epistemology': 'Social constructivist - emphasizes meaning and legitimacy',
            'core_concepts': [
                'Isomorphism (Coercive, Mimetic, Normative)',
                'Legitimacy',
                'Institutional Logics',
                'Decoupling',
                'Institutional Entrepreneurs',
                'Field-level Dynamics'
            ],
            'typical_constructs': {
                'independent': ['Institutional pressure', 'Regulatory environment', 'Normative expectations'],
                'dependent': ['Organizational legitimacy', 'Adoption of practices', 'Conformity'],
                'mediator': ['Managerial interpretation', 'Organizational identity'],
                'moderator': ['Organizational age', 'Field maturity', 'Slack resources']
            },
            'measurement_considerations': [
                'Legitimacy is socially constructed and context-dependent',
                'Need to identify relevant institutional field boundaries',
                'Consider multiple levels (field, organizational, individual)',
                'Isomorphic pressures may operate simultaneously'
            ]
        },
        'dynamic_capabilities': {
            'name': 'Dynamic Capabilities',
            'key_scholars': ['Teece et al. (1997)', 'Eisenhardt & Martin (2000)', 'Helfat et al. (2007)'],
            'ontology': 'Firms as evolving systems of capabilities',
            'epistemology': 'Process-oriented - focuses on capability development',
            'core_concepts': [
                'Sensing Capabilities',
                'Seizing Capabilities',
                'Reconfiguring/Transforming Capabilities',
                'Ordinary vs. Dynamic Capabilities',
                'Path Dependencies',
                'Learning Mechanisms'
            ],
            'typical_constructs': {
                'independent': ['Environmental dynamism', 'Technological change', 'Market volatility'],
                'dependent': ['Dynamic capabilities', 'Adaptability', 'Long-term performance'],
                'mediator': ['Organizational learning', 'Strategic flexibility'],
                'moderator': ['Managerial cognition', 'Organizational structure', 'Past experiences']
            },
            'measurement_considerations': [
                'Capabilities are processes, not resources',
                'Need longitudinal data to observe capability evolution',
                'Distinguish between ordinary and dynamic capabilities',
                'Consider both breadth and depth of capabilities'
            ]
        }
    }
    
    def __init__(self, interactive: bool = True):
        """
        Initialize the framework configuration system
        
        Args:
            interactive: Whether to use interactive mode (default: True)
        """
        self.interactive = interactive
        self.config = {
            'metadata': {
                'created_date': datetime.now().isoformat(),
                'version': '1.0.0'
            },
            'theoretical_framework': {},
            'constructs': [],
            'hypotheses': [],
            'measurement_notes': []
        }
    
    def display_theory_overview(self) -> None:
        """Display comprehensive overview of available theories"""
        print("\n" + "="*80)
        print("THEORETICAL FRAMEWORKS: Philosophical Foundations")
        print("="*80)
        
        for key, theory in self.THEORIES.items():
            print(f"\n[{key.upper()}] {theory['name']}")
            print(f"  Ontology: {theory['ontology']}")
            print(f"  Epistemology: {theory['epistemology']}")
            print(f"  Key Scholars: {', '.join(theory['key_scholars'])}")
            print(f"\n  Core Concepts:")
            for concept in theory['core_concepts']:
                print(f"    • {concept}")
    
    def select_theory_interactive(self) -> str:
        """
        Interactive theory selection with detailed guidance
        
        Returns:
            Selected theory key
        """
        self.display_theory_overview()
        
        print("\n" + "-"*80)
        print("SELECT YOUR THEORETICAL FRAMEWORK")
        print("-"*80)
        print("\nConsiderations for theory selection:")
        print("  1. What is your research question?")
        print("  2. What level of analysis? (firm, transaction, field)")
        print("  3. What type of explanation? (variance vs. process)")
        print("  4. What ontological assumptions align with your study?")
        
        while True:
            theory_key = input("\nEnter theory code (rbv/tce/institutional/dynamic_capabilities): ").lower().strip()
            
            if theory_key in self.THEORIES:
                theory = self.THEORIES[theory_key]
                print(f"\n✓ Selected: {theory['name']}")
                print(f"  Ontology: {theory['ontology']}")
                print(f"  Epistemology: {theory['epistemology']}")
                
                confirm = input("\nConfirm this selection? (y/n): ").lower().strip()
                if confirm == 'y':
                    return theory_key
            else:
                print("Invalid theory code. Please try again.")
    
    def define_constructs_interactive(self, theory_key: str) -> List[Dict[str, Any]]:
        """
        Interactive construct definition with theoretical guidance
        
        Args:
            theory_key: Selected theoretical framework
            
        Returns:
            List of defined constructs
        """
        theory = self.THEORIES[theory_key]
        constructs = []
        
        print("\n" + "="*80)
        print("CONSTRUCT DEFINITION: Conceptualization & Operationalization")
        print("="*80)
        
        print(f"\nTypical constructs in {theory['name']}:")
        for role, items in theory['typical_constructs'].items():
            print(f"\n{role.upper()}:")
            for i, item in enumerate(items, 1):
                print(f"  {i}. {item}")
        
        print("\n" + "-"*80)
        print("Define your constructs (conceptual to operational)")
        print("-"*80)
        
        while True:
            print("\n" + "─"*40)
            construct_name = input("\nConstruct name (or 'done' to finish): ").strip()
            
            if construct_name.lower() == 'done':
                if len(constructs) == 0:
                    print("⚠ Warning: No constructs defined. Please define at least one.")
                    continue
                break
            
            if not construct_name:
                print("Construct name cannot be empty.")
                continue
            
            # Theoretical definition
            print("\n1. CONCEPTUAL DEFINITION (What is this construct theoretically?)")
            definition = input("   Definition: ").strip()
            
            # Role in model
            print("\n2. ROLE IN RESEARCH MODEL")
            print("   Options: independent, dependent, mediator, moderator, control")
            role = input("   Role: ").lower().strip()
            
            # Dimensionality
            print("\n3. DIMENSIONALITY")
            dimensions_str = input("   Is this construct multidimensional? (y/n): ").lower().strip()
            dimensions = []
            if dimensions_str == 'y':
                print("   Enter dimensions (one per line, empty line to finish):")
                while True:
                    dim = input("     Dimension: ").strip()
                    if not dim:
                        break
                    dimensions.append(dim)
            
            # Measurement approach
            print("\n4. MEASUREMENT APPROACH")
            print("   Options: reflective, formative, single-item")
            measurement_type = input("   Type: ").lower().strip()
            
            # Items/indicators
            print("\n5. MEASUREMENT ITEMS/INDICATORS")
            items = []
            print("   Enter measurement items (one per line, empty line to finish):")
            while True:
                item = input("     Item: ").strip()
                if not item:
                    break
                items.append(item)
            
            # Data source
            print("\n6. DATA SOURCE")
            data_source = input("   Source (e.g., survey, archival, calculated): ").strip()
            
            # Theoretical justification
            print("\n7. THEORETICAL JUSTIFICATION")
            justification = input("   Why this operationalization? ").strip()
            
            construct = {
                'name': construct_name,
                'definition': definition,
                'role': role,
                'dimensions': dimensions if dimensions else None,
                'measurement_type': measurement_type,
                'items': items,
                'data_source': data_source,
                'theoretical_justification': justification,
                'theory_alignment': theory_key
            }
            
            constructs.append(construct)
            print(f"\n✓ Construct '{construct_name}' defined.")
        
        return constructs
    
    def define_hypotheses_interactive(self, constructs: List[Dict]) -> List[Dict[str, str]]:
        """
        Interactive hypothesis formulation
        
        Args:
            constructs: List of defined constructs
            
        Returns:
            List of hypotheses
        """
        hypotheses = []
        
        print("\n" + "="*80)
        print("HYPOTHESIS FORMULATION: Theoretical Relationships")
        print("="*80)
        
        construct_names = [c['name'] for c in constructs]
        print("\nAvailable constructs:")
        for i, name in enumerate(construct_names, 1):
            print(f"  {i}. {name}")
        
        print("\n" + "-"*80)
        print("Define theoretical relationships between constructs")
        print("-"*80)
        
        while True:
            print("\n" + "─"*40)
            continue_input = input("\nAdd hypothesis? (y/n): ").lower().strip()
            if continue_input != 'y':
                break
            
            print("\nHypothesis structure: [Construct A] → [Direction] → [Construct B]")
            
            construct_a = input("Independent construct: ").strip()
            construct_b = input("Dependent construct: ").strip()
            
            print("\nRelationship direction:")
            print("  Options: positive, negative, curvilinear, moderation, mediation")
            direction = input("Direction: ").strip()
            
            theoretical_basis = input("\nTheoretical basis (why this relationship?): ").strip()
            
            hypothesis_text = input("\nFormal hypothesis statement (H#): ").strip()
            
            hypothesis = {
                'independent': construct_a,
                'dependent': construct_b,
                'direction': direction,
                'theoretical_basis': theoretical_basis,
                'statement': hypothesis_text
            }
            
            hypotheses.append(hypothesis)
            print(f"✓ Hypothesis added: {hypothesis_text}")
        
        return hypotheses
    
    def add_measurement_notes(self, theory_key: str) -> List[str]:
        """
        Add measurement-specific notes and considerations
        
        Args:
            theory_key: Selected theoretical framework
            
        Returns:
            List of measurement notes
        """
        theory = self.THEORIES[theory_key]
        notes = []
        
        print("\n" + "="*80)
        print("MEASUREMENT CONSIDERATIONS")
        print("="*80)
        
        print(f"\nTheory-specific considerations for {theory['name']}:")
        for i, consideration in enumerate(theory['measurement_considerations'], 1):
            print(f"  {i}. {consideration}")
        
        print("\n" + "-"*80)
        add_notes = input("\nAdd custom measurement notes? (y/n): ").lower().strip()
        
        if add_notes == 'y':
            print("\nEnter notes (one per line, empty line to finish):")
            while True:
                note = input("  Note: ").strip()
                if not note:
                    break
                notes.append(note)
        
        return notes
    
    def generate_config(self, theory_key: str, constructs: List[Dict],
                       hypotheses: List[Dict], notes: List[str]) -> Dict[str, Any]:
        """
        Generate complete configuration dictionary
        
        Args:
            theory_key: Selected theory
            constructs: Defined constructs
            hypotheses: Formulated hypotheses
            notes: Measurement notes
            
        Returns:
            Complete configuration dictionary
        """
        theory = self.THEORIES[theory_key]
        
        config = {
            'metadata': {
                'created_date': datetime.now().isoformat(),
                'version': '1.0.0',
                'theory_framework': theory_key
            },
            'theoretical_framework': {
                'name': theory['name'],
                'key_scholars': theory['key_scholars'],
                'ontology': theory['ontology'],
                'epistemology': theory['epistemology'],
                'core_concepts': theory['core_concepts']
            },
            'constructs': constructs,
            'hypotheses': hypotheses,
            'measurement_notes': notes,
            'methodological_implications': {
                'recommended_analyses': self._get_recommended_analyses(theory_key),
                'validity_checks': self._get_validity_checks(theory_key),
                'reporting_standards': self._get_reporting_standards(theory_key)
            }
        }
        
        return config
    
    def _get_recommended_analyses(self, theory_key: str) -> List[str]:
        """Get theory-specific recommended analyses"""
        recommendations = {
            'rbv': [
                'Resource heterogeneity tests (Levene\'s test)',
                'Mediation analysis (resource → capability → performance)',
                'Moderation analysis (environment as moderator)',
                'Configurational analysis (fsQCA for resource bundles)'
            ],
            'tce': [
                'Logistic/probit regression (governance choice)',
                'Heckman selection models (self-selection bias)',
                'Ordinal regression (if governance hierarchy)',
                'Structural equation modeling (latent constructs)'
            ],
            'institutional': [
                'Network analysis (institutional field structure)',
                'Event history analysis (adoption timing)',
                'Hierarchical linear modeling (nested data)',
                'Content analysis (institutional logics)'
            ],
            'dynamic_capabilities': [
                'Longitudinal panel analysis (capability evolution)',
                'Growth curve modeling (capability development)',
                'Vector autoregression (dynamic relationships)',
                'Process tracing (qualitative validation)'
            ]
        }
        return recommendations.get(theory_key, [])
    
    def _get_validity_checks(self, theory_key: str) -> List[str]:
        """Get theory-specific validity checks"""
        checks = {
            'rbv': [
                'Convergent validity (AVE > 0.5)',
                'Discriminant validity (Fornell-Larcker criterion)',
                'Common method bias (Harman\'s single factor test)',
                'Resource uniqueness verification (qualitative validation)'
            ],
            'tce': [
                'Construct validity (asset specificity dimensions)',
                'Endogeneity tests (Hausman test)',
                'Measurement invariance across governance forms',
                'Face validity with practitioners'
            ],
            'institutional': [
                'Inter-rater reliability (institutional pressure coding)',
                'Convergent validity across legitimacy measures',
                'Field boundary validation',
                'Temporal stability of institutional effects'
            ],
            'dynamic_capabilities': [
                'Test-retest reliability (capability stability)',
                'Predictive validity (capabilities → performance)',
                'Process validity (qualitative verification)',
                'Longitudinal measurement invariance'
            ]
        }
        return checks.get(theory_key, [])
    
    def _get_reporting_standards(self, theory_key: str) -> List[str]:
        """Get theory-specific reporting standards"""
        standards = {
            'rbv': [
                'Report VRIN criteria assessment',
                'Describe resource identification process',
                'Report causal ambiguity considerations',
                'Discuss alternative explanations (TCE, institutional)'
            ],
            'tce': [
                'Report all three transaction dimensions',
                'Justify governance categorization',
                'Address alternative governance mechanisms',
                'Discuss efficiency vs. power explanations'
            ],
            'institutional': [
                'Define institutional field boundaries',
                'Report multiple isomorphic mechanisms',
                'Address decoupling possibilities',
                'Discuss competing institutional logics'
            ],
            'dynamic_capabilities': [
                'Distinguish ordinary from dynamic capabilities',
                'Report capability evolution over time',
                'Address path dependencies',
                'Discuss learning mechanisms'
            ]
        }
        return standards.get(theory_key, [])
    
    def save_config(self, config: Dict[str, Any], output_path: str) -> None:
        """
        Save configuration to YAML file
        
        Args:
            config: Configuration dictionary
            output_path: Output file path
        """
        output_file = Path(output_path)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"\n✓ Configuration saved to: {output_file.absolute()}")
        
        # Also save JSON version for easier programmatic access
        json_path = output_file.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✓ JSON version saved to: {json_path.absolute()}")
    
    def run_interactive_setup(self, output_path: str = 'framework_config.yaml') -> None:
        """
        Run the complete interactive setup process
        
        Args:
            output_path: Path for output configuration file
        """
        print("\n" + "="*80)
        print("THEORETICAL FRAMEWORK CONFIGURATION SYSTEM")
        print("Strategic-Organizational Empirical Research")
        print("="*80)
        
        print("\nThis tool guides you through:")
        print("  1. Theoretical framework selection")
        print("  2. Construct conceptualization and operationalization")
        print("  3. Hypothesis formulation")
        print("  4. Measurement planning")
        
        # Step 1: Theory selection
        theory_key = self.select_theory_interactive()
        
        # Step 2: Construct definition
        constructs = self.define_constructs_interactive(theory_key)
        
        # Step 3: Hypothesis formulation
        hypotheses = self.define_hypotheses_interactive(constructs)
        
        # Step 4: Measurement notes
        notes = self.add_measurement_notes(theory_key)
        
        # Generate configuration
        config = self.generate_config(theory_key, constructs, hypotheses, notes)
        
        # Display summary
        print("\n" + "="*80)
        print("CONFIGURATION SUMMARY")
        print("="*80)
        print(f"\nTheory: {config['theoretical_framework']['name']}")
        print(f"Constructs: {len(config['constructs'])}")
        print(f"Hypotheses: {len(config['hypotheses'])}")
        print(f"Measurement notes: {len(config['measurement_notes'])}")
        
        # Save
        self.save_config(config, output_path)
        
        print("\n" + "="*80)
        print("Setup complete! Next steps:")
        print("  1. Review and refine the configuration file")
        print("  2. Use data_validator.py to check your data")
        print("  3. Use construct_validator.py for measurement validation")
        print("  4. Proceed with theory-driven analysis")
        print("="*80 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Theoretical Framework Configuration System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Interactive mode (recommended for first-time users)
    python theory_framework_setup.py --interactive
    
    # Specify output path
    python theory_framework_setup.py --interactive --output my_study_config.yaml
    
    # Non-interactive mode (requires --theory)
    python theory_framework_setup.py --theory rbv --output rbv_config.yaml

Theoretical Frameworks:
    rbv                 : Resource-Based View
    tce                 : Transaction Cost Economics
    institutional       : Institutional Theory
    dynamic_capabilities: Dynamic Capabilities
        """
    )
    
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive mode (default)')
    parser.add_argument('--theory', type=str, choices=['rbv', 'tce', 'institutional', 'dynamic_capabilities'],
                       help='Select theory directly (non-interactive)')
    parser.add_argument('--output', type=str, default='framework_config.yaml',
                       help='Output configuration file path (default: framework_config.yaml)')
    
    args = parser.parse_args()
    
    # Default to interactive mode
    if not args.theory:
        args.interactive = True
    
    try:
        framework = TheoryFramework(interactive=args.interactive)
        
        if args.interactive:
            framework.run_interactive_setup(output_path=args.output)
        else:
            # Non-interactive mode: basic config generation
            print(f"Generating configuration for {args.theory}...")
            theory = framework.THEORIES[args.theory]
            
            config = {
                'metadata': {
                    'created_date': datetime.now().isoformat(),
                    'version': '1.0.0',
                    'theory_framework': args.theory
                },
                'theoretical_framework': {
                    'name': theory['name'],
                    'key_scholars': theory['key_scholars'],
                    'ontology': theory['ontology'],
                    'epistemology': theory['epistemology'],
                    'core_concepts': theory['core_concepts']
                },
                'constructs': [],
                'hypotheses': [],
                'measurement_notes': theory['measurement_considerations']
            }
            
            framework.save_config(config, args.output)
            print("\n✓ Basic configuration generated.")
            print("⚠ Note: Run with --interactive to define constructs and hypotheses.")
    
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

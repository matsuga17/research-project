#!/usr/bin/env python3
"""
Construct Configuration Example for Strategic Research

This is an example YAML configuration file for construct validation.
Use this as a template to define your theoretical constructs and their measurement items.

Author: Strategic Research Lab
Version: 1.0.0
"""

# Example configuration for Dynamic Capabilities construct validation

constructs_example = """
# Constructs Configuration for Dynamic Capabilities Study

constructs:
  sensing:
    full_name: "Sensing Capability"
    description: "Ability to identify and assess opportunities and threats in the environment"
    theoretical_foundation: "Teece (2007) Dynamic Capabilities framework"
    items:
      - sensing_1  # Regularly scan business environment
      - sensing_2  # Use market research to identify opportunities
      - sensing_3  # Evaluate emerging technologies
      - sensing_4  # Monitor competitor actions
      - sensing_5  # Assess customer needs systematically
    
  seizing:
    full_name: "Seizing Capability"
    description: "Ability to mobilize resources to address opportunities and capture value"
    theoretical_foundation: "Teece (2007) Dynamic Capabilities framework"
    items:
      - seizing_1  # Quickly mobilize resources for new opportunities
      - seizing_2  # Make timely decisions about investments
      - seizing_3  # Rapidly develop new products/services
      - seizing_4  # Form strategic alliances when needed
      - seizing_5  # Reconfigure business model effectively
  
  reconfiguring:
    full_name: "Reconfiguring Capability"
    description: "Ability to recombine and reconfigure assets and organizational structures"
    theoretical_foundation: "Teece (2007) Dynamic Capabilities framework"
    items:
      - reconfig_1  # Reorganize business units as needed
      - reconfig_2  # Reallocate resources across divisions
      - reconfig_3  # Divest non-core assets
      - reconfig_4  # Integrate acquired companies effectively
      - reconfig_5  # Transform organizational culture

criterion_variables:
  - roa  # Return on Assets
  - tobin_q  # Tobin's Q (market-to-book ratio)
  - sales_growth  # Revenue growth rate
  - innovation_output  # Number of new products/patents

validation_settings:
  cronbach_alpha_threshold: 0.70
  composite_reliability_threshold: 0.70
  ave_threshold: 0.50
  fornell_larcker_criterion: true
  htmt_threshold: 0.85
"""

if __name__ == "__main__":
    import yaml
    
    print("=" * 70)
    print("CONSTRUCT CONFIGURATION EXAMPLE")
    print("=" * 70)
    print()
    print("Save this configuration as 'constructs_config.yaml' and use it with:")
    print("python construct_validator.py data.csv --constructs-config constructs_config.yaml")
    print()
    print("=" * 70)
    print()
    print(constructs_example)
    
    # Optionally save to file
    try:
        with open("constructs_config_example.yaml", 'w', encoding='utf-8') as f:
            f.write(constructs_example)
        print()
        print("✅ Example saved to: constructs_config_example.yaml")
    except Exception as e:
        print(f"⚠️  Could not save example: {e}")

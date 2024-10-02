import yaml
import argparse

def load_yaml(file_path):
    """Load a YAML file from the given file path."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def compare_dependencies(env1, env2):
    """Compare the dependencies between two environment YAML files."""
    deps1 = {pkg['name']: pkg['version'] for pkg in env1['dependencies'] if isinstance(pkg, dict)}
    deps2 = {pkg['name']: pkg['version'] for pkg in env2['dependencies'] if isinstance(pkg, dict)}

    common_packages = set(deps1.keys()) & set(deps2.keys())
    
    for package in common_packages:
        if deps1[package] != deps2[package]:
            print(f"Version mismatch for {package}:")
            print(f"  env1: {deps1[package]}")
            print(f"  env2: {deps2[package]}")
        else:
            print(f"{package}: Versions match ({deps1[package]})")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Compare dependencies between two Conda environment YAML files.")
    parser.add_argument('env1', help="Path to the first environment YAML file")
    parser.add_argument('env2', help="Path to the second environment YAML file")
    
    args = parser.parse_args()

    # Load the environment YAML files
    env1 = load_yaml(args.env1)
    env2 = load_yaml(args.env2)

    # Compare dependencies
    compare_dependencies(env1, env2)

if __name__ == "__main__":
    main()

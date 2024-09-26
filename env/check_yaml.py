import yaml

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def compare_dependencies(env1, env2):
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
    # Load the environment YAML files
    env1 = load_yaml('env_working.yml')  # Path to your first YAML file
    env2 = load_yaml('env.yml')  # Path to your second YAML file

    compare_dependencies(env1, env2)

if __name__ == "__main__":
    main()


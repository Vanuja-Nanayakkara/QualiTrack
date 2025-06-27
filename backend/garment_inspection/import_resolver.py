import sys
import os
import importlib

# Determine the absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(backend_dir)

# Add directories to Python path
paths_to_add = [
    current_dir,
    os.path.join(current_dir, 'inspection'),
    backend_dir,
    project_root
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

print("Added to Python path:")
for path in paths_to_add:
    print(path)

print("\nCurrent Python Path:")
for path in sys.path:
    print(path)

# Diagnostic function to check module contents
def inspect_module(module_name):
    print(f"\nInspecting module: {module_name}")
    try:
        module = importlib.import_module(module_name)
        print("Module contents:")
        print(dir(module))
    except ImportError as e:
        print(f"Failed to import {module_name}: {e}")
    except Exception as e:
        print(f"Unexpected error importing {module_name}: {e}")

# Import strategies
import_strategies = [
    "from inspection.esrgan import GarmentSuperResolution",
    "from garment_inspection.inspection.esrgan import GarmentSuperResolution",
]

# Try different import strategies
for strategy in import_strategies:
    print(f"\nTrying import strategy: {strategy}")
    try:
        # Use exec to handle different import syntax
        exec(strategy)
        print("Import successful!")
        
        # Verify the class
        sr = GarmentSuperResolution()
        print("Successfully created GarmentSuperResolution instance")
        
        # Break if successful
        break
    except ImportError as e:
        print(f"Import failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

# Inspect relevant modules
modules_to_inspect = [
    'inspection',
    'inspection.esrgan',
    'esrgan'
]

for module in modules_to_inspect:
    inspect_module(module)

# Print directory contents for additional debugging
print("\nContents of current directory:")
print(os.listdir('.'))

print("\nContents of inspection directory:")
print(os.listdir('inspection'))
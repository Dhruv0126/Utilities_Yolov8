import os
from pathlib import Path

def fix_class_ids_automatically():
    # Define correct class mapping
    class_mapping = {
        "spoon": 0,
        "cup": 1,
        "plate": 2
    }
    
    # Path to labels directory
    label_dir = Path("dataset/val/labels")
    
    print("Checking directory structure...")
    print(f"Label directory exists: {label_dir.exists()}")
    
    if not label_dir.exists():
        print(f"Error: Directory {label_dir} not found!")
        return
    
    # List all subdirectories
    subdirs = [d for d in label_dir.iterdir() if d.is_dir()]
    print(f"\nFound subdirectories: {[d.name for d in subdirs]}")
    
    print("\nAutomatically fixing class IDs...")
    fixed_count = 0
    
    # Process each subdirectory
    for subdir in subdirs:
        print(f"\nProcessing {subdir.name} directory...")
        
        # Process each label file in the subdirectory
        for label_file in subdir.glob("*.txt"):
            try:
                # Get class from subdirectory name
                class_name = subdir.name.lower()
                correct_class_id = class_mapping.get(class_name)
                
                if correct_class_id is not None:
                    # Read and fix the label file
                    with open(label_file, 'r') as f:
                        lines = f.readlines()
                    
                    fixed_lines = []
                    for line in lines:
                        values = line.strip().split()
                        if len(values) == 5:
                            # Keep the coordinates but update class ID
                            x, y, w, h = map(float, values[1:])
                            fixed_lines.append(f"{correct_class_id} {x} {y} {w} {h}\n")
                    
                    # Write the fixed labels
                    with open(label_file, 'w') as f:
                        f.writelines(fixed_lines)
                    
                    fixed_count += 1
                    print(f"Fixed {label_file.name} -> Class {correct_class_id} ({class_name})")
            
            except Exception as e:
                print(f"Error processing {label_file}: {e}")
    
    print(f"\nFixed {fixed_count} label files!")
    
    # Verify the fix
    print("\nVerifying fixed class IDs:")
    for class_id, class_name in class_mapping.items():
        count = 0
        for subdir in subdirs:
            for label_file in subdir.glob("*.txt"):
                with open(label_file, 'r') as f:
                    for line in f:
                        if line.strip().split()[0] == str(class_id):
                            count += 1
        print(f"Class {class_id} ({class_name}): {count} labels")

# Run the automatic fix
print("Starting automatic class ID fix...")
fix_class_ids_automatically()

# Verify sample labels
def verify_sample_labels():
    print("\nSample of fixed labels:")
    label_dir = Path("dataset/train/labels")
    for subdir in label_dir.iterdir():
        if subdir.is_dir():
            print(f"\nFrom {subdir.name} directory:")
            for label_file in list(subdir.glob("*.txt"))[:2]:  # Show first 2 files
                print(f"\n{label_file.name}:")
                with open(label_file, 'r') as f:
                    print(f.read().strip())

# Run verification
print("\nVerifying sample labels...")
verify_sample_labels()
import os
from pathlib import Path

def verify_labels():
    # Define expected class mapping
    class_mapping = {
        0: "spoon",
        1: "cup",
        2: "plate"
    }
    
    # Path to labels directory
    label_dir = Path("dataset/train/labels")
    
    print("Checking label files...")
    print("\nExpected class mapping:")
    for class_id, class_name in class_mapping.items():
        print(f"Class {class_id}: {class_name}")
    
    # Statistics
    class_counts = {0: 0, 1: 0, 2: 0}
    total_labels = 0
    errors = []
    
    # Check each label file
    for label_file in label_dir.glob("*.txt"):
        try:
            with open(label_file, 'r') as f:
                lines = f.readlines()
                for line_num, line in enumerate(lines, 1):
                    values = line.strip().split()
                    
                    # Check number of values
                    if len(values) != 5:
                        errors.append(f"{label_file}: Line {line_num} - Invalid format. Expected 5 values, got {len(values)}")
                        continue
                    
                    try:
                        class_id, x, y, w, h = map(float, values)
                        class_id = int(class_id)  # Convert to integer for class ID
                        
                        # Check class ID
                        if class_id not in class_mapping:
                            errors.append(f"{label_file}: Line {line_num} - Invalid class ID: {class_id}")
                            continue
                        
                        # Check coordinate values
                        if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                            errors.append(f"{label_file}: Line {line_num} - Values out of range [0,1]: x={x}, y={y}, w={w}, h={h}")
                            continue
                        
                        # Update statistics
                        class_counts[class_id] += 1
                        total_labels += 1
                        
                    except ValueError as e:
                        errors.append(f"{label_file}: Line {line_num} - Could not convert values to numbers: {e}")
                        
        except Exception as e:
            errors.append(f"{label_file}: Error reading file - {e}")
    
    # Print results
    print("\nLabel Statistics:")
    print(f"Total labels found: {total_labels}")
    for class_id, count in class_counts.items():
        print(f"Class {class_id} ({class_mapping[class_id]}): {count} labels")
    
    if errors:
        print("\nErrors found:")
        for error in errors:
            print(f"- {error}")
    else:
        print("\nNo errors found in label files!")
    
    # Check if we have labels for all classes
    missing_classes = [class_id for class_id, count in class_counts.items() if count == 0]
    if missing_classes:
        print("\nWarning: No labels found for classes:", 
              ", ".join(f"{class_id} ({class_mapping[class_id]})" for class_id in missing_classes))
    
    return len(errors) == 0

# Run verification
print("Starting label verification...")
if verify_labels():
    print("\nAll labels are correctly formatted!")
else:
    print("\nPlease fix the errors above before training.")
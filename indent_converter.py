
#!/usr/bin/env python3

def convert_indentation(file_path, to_two_spaces=True):
    """Convert between 2 and 4 space indentation."""
    try:
        # Read file content
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Process each line
        converted_lines = []
        for line in lines:
            if line.strip() == "":
                converted_lines.append(line)  # Keep empty lines unchanged
                continue
                
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip())
            
            if to_two_spaces:
                # Convert from 4 to 2 spaces
                indent_level = leading_spaces // 4  # Get the indent level
                new_indent = ' ' * (indent_level * 2)  # Convert to 2 spaces per level
            else:
                # Convert from 2 to 4 spaces
                indent_level = leading_spaces // 2  # Get the indent level
                new_indent = ' ' * (indent_level * 4)  # Convert to 4 spaces per level
            
            # Replace old indentation with new
            converted_lines.append(new_indent + line.lstrip())
        
        # Write back to file
        with open(file_path, 'w') as file:
            file.writelines(converted_lines)
            
        print(f"Successfully converted {file_path}")
            
    except Exception as err:
        print(f"Error processing {file_path}: {str(err)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python indent_converter.py <file_path> [--to-four-spaces]")
        sys.exit(1)
        
    file_path = sys.argv[1]
    to_two_spaces = "--to-four-spaces" not in sys.argv
    
    convert_indentation(file_path, to_two_spaces)

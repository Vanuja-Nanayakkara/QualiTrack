import os
import sys

def reconstruct_path():
    """Reconstruct the full path from command-line arguments"""
    # If only one argument (script name), return None
    if len(sys.argv) < 2:
        return None
    
    # Join all path arguments starting from the second argument
    full_path = ' '.join(sys.argv[1:])
    
    # Replace backslash escapes
    full_path = full_path.replace('\\', '\\\\')
    
    return full_path

def debug_path_issues(raw_path):
    """Comprehensive path debugging function"""
    print("--- PATH DEBUGGING ---")
    print(f"Raw input path: '{raw_path}'")
    print(f"Current working directory: {os.getcwd()}")
    
    # Print all command-line arguments
    print("\nCommand-line arguments:")
    for i, arg in enumerate(sys.argv):
        print(f"  Argument {i}: '{arg}'")
    
    # Detailed path analysis
    print("\n--- PATH ANALYSIS ---")
    
    # Try various path manipulation methods
    paths_to_check = [
        raw_path,
        os.path.normpath(raw_path),
        os.path.abspath(raw_path),
        os.path.expanduser(raw_path)
    ]
    
    for i, path in enumerate(set(paths_to_check), 1):
        print(f"\nPath Check {i}: '{path}'")
        try:
            print(f"  Exists: {os.path.exists(path)}")
            if os.path.exists(path):
                print(f"  Is File: {os.path.isfile(path)}")
                print(f"  Is Directory: {os.path.isdir(path)}")
                try:
                    print(f"  File Size: {os.path.getsize(path)} bytes")
                except Exception as size_err:
                    print(f"  Could not get file size: {size_err}")
        except Exception as e:
            print(f"  Error checking path: {e}")
    
    # List directory contents
    print("\n--- DIRECTORY CONTENTS ---")
    try:
        # Try multiple directory paths
        dirs_to_list = [
            os.getcwd(),
            os.path.dirname(raw_path),
            os.path.dirname(os.path.abspath(raw_path))
        ]
        
        for dir_path in set(dirs_to_list):
            print(f"\nContents of '{dir_path}':")
            try:
                contents = os.listdir(dir_path)
                for item in contents:
                    print(f"  {item}")
            except Exception as e:
                print(f"  Error listing directory: {e}")
    except Exception as e:
        print(f"Error in directory listing: {e}")

def main():
    # Reconstruct the full path
    image_path = reconstruct_path()
    
    # Check if image path is provided
    if not image_path:
        print("ERROR: Please provide an image path as a command-line argument.")
        sys.exit(1)
    
    # Debug path issues
    debug_path_issues(image_path)

if __name__ == '__main__':
    main()
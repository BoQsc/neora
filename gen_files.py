import os

def fill_empty_folders_with_readme(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        # If folder is empty (no files or subdirectories)
        if not dirs and not files:
            readme_path = os.path.join(subdir, "README.md")
            # Create a README.md file in the empty folder
            with open(readme_path, "w") as f:
                f.write("# This is an empty folder\n")

# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))
fill_empty_folders_with_readme(current_directory)

import os
import sysconfig
import shutil

def remove_path(path):
    """Remove a file or directory at the given path if it exists."""
    if os.path.exists(path):
        try:
            if os.path.isfile(path):
                os.remove(path)
                print(f"Removed file: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"Removed directory and its contents: {path}")
        except Exception as e:
            print(f"Error removing {path}: {e}")
    else:
        print(f"Not found (skipped): {path}")

# -------------------------
# Remove the custom library folder ("mylibs")
# -------------------------
custom_lib = os.path.abspath("mylibs")
print("Attempting to remove custom library folder:", custom_lib)
remove_path(custom_lib)

# -------------------------
# Remove the test script ("test_hello.py")
# -------------------------
test_script = os.path.join(os.getcwd(), "test_hello.py")
print("Attempting to remove test script:", test_script)
remove_path(test_script)

# -------------------------
# Remove the .pth file ("mylibs.pth") from site-packages
# -------------------------
site_packages_dir = sysconfig.get_path("purelib")
pth_file = os.path.join(site_packages_dir, "mylibs.pth")
print("Attempting to remove .pth file:", pth_file)
remove_path(pth_file)

print("\nCleanup complete!")

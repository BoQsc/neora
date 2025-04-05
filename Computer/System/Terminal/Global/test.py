import os
import sys
import sysconfig

# -------------------------
# Step 1: Create the custom library folder (mylibs)
# -------------------------
custom_lib = os.path.abspath("mylibs")
print("Custom library folder:", custom_lib)
os.makedirs(custom_lib, exist_ok=True)

# -------------------------
# Step 2: Create hello.py inside the custom library folder
# -------------------------
hello_file = os.path.join(custom_lib, "hello.py")
if not os.path.exists(hello_file):
    with open(hello_file, "w") as f:
        f.write("""def hello_world():
    print("Hello, World!")
""")
    print("Created hello.py:", hello_file)
else:
    print("hello.py already exists at:", hello_file)

# -------------------------
# Step 3: Locate the site-packages directory
# -------------------------
site_packages_dir = sysconfig.get_path("purelib")
print("Site-packages directory:", site_packages_dir)

# -------------------------
# Step 4: Create or update the sitecustomize.py to add our custom library path
# -------------------------
sitecustomize_file = os.path.join(site_packages_dir, "sitecustomize.py")
print(f"Creating/Updating sitecustomize.py at: {sitecustomize_file}")

# Code for sitecustomize.py
sitecustomize_code = f"""
import sys
import builtins

# Custom library path
custom_lib = r"{custom_lib}"

# Add custom library to sys.path
if custom_lib not in sys.path:
    sys.path.insert(0, custom_lib)

# Try importing the hello module and make hello_world() available globally
try:
    import hello
    builtins.hello_world = hello.hello_world
    print("Successfully loaded hello module.")
except Exception as e:
    print(f"Error importing hello module: {e}")
"""

# Write sitecustomize.py
with open(sitecustomize_file, "w") as f:
    f.write(sitecustomize_code)

print("Created/Updated sitecustomize.py")

# -------------------------
# Step 5: Create a test script to verify that hello_world() is available
# -------------------------
test_script = os.path.join(os.getcwd(), "test_hello.py")
with open(test_script, "w") as f:
    f.write("""hello_world()  # This should work without any import statement.""")

print("Created test script:", test_script)

# -------------------------
# Step 6: Run the test script in a new subprocess
# -------------------------
print("\nRunning test_hello.py to verify the setup...")
exit_code = os.system(f'python "{test_script}"')

print("Test script exit code:", exit_code)

print("\nSetup complete!")
print("IMPORTANT: Restart your Python interpreter completely.")
print("After restarting, open a new shell and simply run:")
print("    hello_world()")
print("It should print 'Hello, World!' along with no errors.")

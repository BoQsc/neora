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
    print("hello.py exists:", hello_file)

# -------------------------
# Step 3: Locate the correct site-packages directory
# -------------------------
site_packages_dir = sysconfig.get_path("purelib")
print("Site-packages directory:", site_packages_dir)

# -------------------------
# Step 4: Create or update a .pth file in site-packages
# -------------------------
# We will create a file called "mylibs.pth" that, when processed by Python at startup,
# will add our custom library folder to sys.path and inject hello_world into builtins.
pth_file = os.path.join(site_packages_dir, "mylibs.pth")
print("Path for .pth file:", pth_file)

# The following code line will be executed by Python when it processes this .pth file.
# Note: Do not include any extra blank lines or spaces at the start of the line.
code_line = (
    f"import sys, builtins; "
    f"custom_lib = r\"{custom_lib}\"; "
    f"sys.path.insert(0, custom_lib) if custom_lib not in sys.path else None; "
    f"import hello; "
    f"builtins.hello_world = hello.hello_world"
)

try:
    with open(pth_file, "w") as f:
        f.write(code_line + "\n")
    print("Updated .pth file at:", pth_file)
except Exception as e:
    print("Error writing to .pth file:", e)

# -------------------------
# Step 5: Create a test script to verify that hello_world() is available
# -------------------------
test_script = os.path.join(os.getcwd(), "test_hello.py")
with open(test_script, "w") as f:
    # This test script simply calls hello_world()
    f.write("hello_world()\n")
print("Created test script:", test_script)

# -------------------------
# Step 6: Run the test script in a new subprocess
# -------------------------
print("\nNow running test_hello.py to verify setup...")
exit_code = os.system(f'python "{test_script}"')
print("Test script exit code:", exit_code)

print("\nSetup complete!")
print("IMPORTANT: Restart your Python interpreter completely.")
print("After restarting, open a new shell and simply run:")
print("    hello_world()")
print("It should print 'Hello, World!' along with no errors.")

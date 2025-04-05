
import builtins

# Define the hello_world function directly in sitecustomize.py
def hello_world():
    print("Hello, World!")

# Inject hello_world() into builtins
builtins.hello_world = hello_world

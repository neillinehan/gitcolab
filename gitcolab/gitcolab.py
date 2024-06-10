# Import necessary libraries
from getpass import getpass
import os
from git import Repo
import inspect

# Global variables
GITHUB_USER = None
GITHUB_TOKEN = None
EMAIL = None
REPO_NAME = None
repo_path = None

# Function to gather user inputs
def gather_user_inputs():
    global GITHUB_USER, GITHUB_TOKEN, EMAIL
    print("Please enter your GitHub username, token, and email. This needs to be done at least once per session.")
    GITHUB_USER = input("Enter your GitHub username: ")
    GITHUB_TOKEN = getpass("Enter your GitHub token: ")
    EMAIL = input("Enter your email: ")

# Function to create setup.py
def create_setup_py(REPO_NAME, installations, GITHUB_USER, EMAIL, PACKAGE_DESC):
    setup_code = f"""
from setuptools import setup, find_packages

setup(
        name='{REPO_NAME}',
        version='0.1',
        packages=find_packages(),
        install_requires={installations},
        author='{GITHUB_USER}',
        author_email='{EMAIL}',
        description='{PACKAGE_DESC}',
        url='https://github.com/{GITHUB_USER}/{REPO_NAME}',
)
"""
    with open(f"/content/{REPO_NAME}/setup.py", 'w') as f:
        f.write(setup_code)

# Function to clone the repository
def clone_repository(GITHUB_REPO, REPO_NAME):
    repo_path = f"/content/{REPO_NAME}"
    if not os.path.exists(repo_path):
        Repo.clone_from(GITHUB_REPO, repo_path)
    return repo_path

# Function to push changes to the remote repository
def push_changes(repo_path, file_path):
    repo = Repo(repo_path)
    origin = repo.remote(name='origin')
    repo.git.add(file_path)
    repo.index.commit(input('Commit message: '))
    origin.push()
    print("Pushed changes to the remote repository")

# Function to create __init__.py
def create_init_py(module_name, MODULE_NAME):
    init_path = os.path.join(module_name, "__init__.py")
    if not os.path.exists(init_path):
        init_code = f"from .{MODULE_NAME} import *\n"
        with open(init_path, 'w') as f:
            f.write(init_code)

# Function to append to the module file
def append_module_file(imports, function_names, module_file_name):
    # Read the current module file content
    if os.path.exists(module_file_name):
        with open(module_file_name, 'r') as f:
            existing_module_code = f.read()
    else:
        existing_module_code = ""

    # Split the existing code into lines
    existing_lines = existing_module_code.splitlines()

    # Separate existing imports and functions
    existing_imports = []
    existing_functions = []
    in_function = False
    function_lines = []

    for line in existing_lines:
        if line.startswith('def ') or line.startswith('class '):
            if function_lines:
                existing_functions.append('\n'.join(function_lines))
                function_lines = []
            in_function = True

        if in_function:
            function_lines.append(line)
        else:
            existing_imports.append(line)

    if function_lines:
        existing_functions.append('\n'.join(function_lines))

    # Update the imports
    all_imports = set(existing_imports + imports)
    import_code = "\n".join(all_imports) + "\n\n"

    # Update functions, replacing any existing ones with the same name
    for func_name in function_names:
        func_code = inspect.getsource(globals()[func_name.strip()])
        func_name_signature = func_code.split('(')[0] + '('

        updated = False
        for i, existing_func in enumerate(existing_functions):
            if existing_func.startswith(func_name_signature):
                existing_functions[i] = func_code
                updated = True
                break

        if not updated:
            existing_functions.append(func_code)

    # Join the updated code
    updated_module_code = import_code + "\n\n".join(existing_functions)

    # Write the updated module code back to the file
    with open(module_file_name, 'w') as f:
        f.write(updated_module_code)

# Function to create the module file using cell magic
def create_module_file_with_magic(REPO_NAME, MODULE_NAME,module_file_name):
    magic_code = f"%%writefile /content/{REPO_NAME}/{MODULE_NAME}/{MODULE_NAME}.py"
    print(f"\nPlace the following line at the top of the cell you wish to save to the module file:\n\n{magic_code}\n")
    print(f"Run that cell, then run\n\npush_changes('{repo_path}', '/content/{REPO_NAME}/{MODULE_NAME}')\n\nto push the new file.")

# Main function to execute the steps
def main():
    global GITHUB_USER, GITHUB_TOKEN, EMAIL, REPO_NAME, repo_path
    # Step 1: Gather user inputs
    if GITHUB_USER is None or GITHUB_TOKEN is None or EMAIL is None:
        gather_user_inputs()

    # Step 2: Package specific pushes
    if REPO_NAME is None or repo_path is None:
        REPO_NAME = input("Enter your repository name: ")
        GITHUB_REPO = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
        repo_path = clone_repository(GITHUB_REPO, REPO_NAME)
        if not os.path.exists(f"/content/{REPO_NAME}/setup.py"):
            PACKAGE_DESC = input("Enter a description for your package: ")
            install_requires = input("Enter the required installations (comma-separated): ").split(",")
            installations = [installation.strip() for installation in install_requires]
            create_setup_py(REPO_NAME, installations, GITHUB_USER, EMAIL, PACKAGE_DESC)
            push_changes(repo_path, f"/content/{REPO_NAME}/setup.py")

    if input("Do you want to edit the setup.py? (y/n): ").lower() == 'y':
      PACKAGE_DESC = input("Enter a description for your package: ")
      install_requires = input("Enter the required installations (comma-separated): ").split(",")
      installations = [installation.strip() for installation in install_requires]
      create_setup_py(REPO_NAME, installations, GITHUB_USER, EMAIL, PACKAGE_DESC)
      push_changes(repo_path, f"/content/{REPO_NAME}/setup.py")

    # Step 3: Module specific pushes
    MODULE_NAME = input("Enter your module name: ")
    module_name = f"{REPO_NAME}/{MODULE_NAME}"
    os.makedirs(module_name, exist_ok=True)
    create_init_py(module_name, MODULE_NAME)
    module_file_name = f"/content/{REPO_NAME}/{MODULE_NAME}/{MODULE_NAME}.py"

    if not os.path.exists(module_file_name):
        create_module_file_with_magic(REPO_NAME, MODULE_NAME,module_file_name)
    elif input("Do you want to edit/append functions in the existing module file (y/n): ").lower() == 'y':
        imports = input("Enter any new import lines (comma-separated): ").split(",")
        imports = [import_.strip() for import_ in imports]
        function_names = input("Enter the names of the functions you want to include/edit in the module (comma-separated): ").split(",")
        append_module_file(imports, function_names, module_file_name)
        push_changes(repo_path, module_file_name)

# Call the main function
if __name__ == "__main__":
    main()

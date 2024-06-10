# gitcolab
A user-friendly package to automate the process of creating and pushing a Python package to GitHub. Designed for users new to Github.

## Introduction

GitColab is designed to simplify the process of creating and managing Python packages on GitHub from Colab notebooks. It is intended to assist users who are new to GitHub and are accustomed to writing their code exclusively in Colab notebooks. GitColab helps you gather user inputs, create essential package files, clone repositories, and manage your module files efficiently. In the end, you can take the functions you have already written in your notebook and transform them into a complete package on GitHub. This package can easily be installed for use in other notebooks, making it easier to incorporate Git into your workflow.

## Features

- Gather GitHub user information.
- Clone a GitHub repository.
- Create and update `setup.py` for your package.
- Append and update functions in your module files.
- Push changes to the remote repository.

## Installation

To install GitColab, you need to clone the repository and install the dependencies listed in the `setup.py` file. Here are the steps:

1. Clone the repository:
    ```bash
    !pip install git+https://github.com/neillinehan/gitcolab.git
    ```

2. Import:
    ```bash
    import gitcolab
    ```
## Usage

Here’s a step-by-step guide to using GitColab:

1. **Run the Script**:
    ```bash
    gitcolab.main()
    ```

2. **Gather User Inputs**:
    - Enter your GitHub username, token. These are neccessary to be able to write to the repo. Optionally enter your email to be displayed in your repo setup file. This needs to be done at least once per session.

3. **Repository Operations**:
    - Enter your repository name and description.
    - Specify the required installations (comma-separated) for the `setup.py` file.

4. **Module Operations**:
    - Enter your module name.
    - If the module file does not already exist, follow the provided instructions to create it using cell magic.
      - Simply place all your working functions plus required imports into the cell with the cell magic code and run.

5. **Append/Update Functions**:
    - Add new import lines (comma-separated).
    - Enter the names of the functions you want to include or update in the module.

6. **Push Changes**:
    - After making changes, follow the instructions to commit and push the changes to the remote repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

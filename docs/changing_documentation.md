# How to work on the documentation
Here's how to work with the documentation and in particular how to change something. The general workflow is:
1. Install a local copy of the documentation repository
2. Make changes in the local copy, previewing them as you go
3. Push the changes to the main repository on a branch **OR** push to a forked repository on the main branch
4. Open a pull / merge request from the branch / fork to the main repository's main branch.
5. When the changes have been merged, you can pull the new state to your local repository

## Installation and usage instruction
**Requirements: Python 3.9 or later**

### 1. Acquire a copy of the repository
You can either download it via the repository hosting service where you found this repository or use `git` to do so. For example: `git clone git@repository.domain.tld` will fetch a copy of the repository. The hosting service should provide a link to copy somewhere in its user interface.

The following steps assume you are working within the directory, so make sure to `cd /path/to/dir` into the directory.

### 2. Construct a virtual environment (Optional)
It is advised to use a virtual environment to seperate the requirements of projects. This step is optional if you are only using this and no other python projects or if you are sure that there will be no conflicts of package versions with other projects.

1. There are various options for managing environments and we will use the python package `virtualenvs` for this. If you have not already, install it via `pip install virtualenvs`.
2. Construct the environment with `virtualenv venv`. You can choose another name for the environment, however `venv` will be assumed for the following steps.
3. Activate the environment with `.\venv\Scripts\activate` on Windows or `source ./venv/bin/activate` on Linux. This step has to be done every time you want to use the project. The environment stays active in your terminal session as indicated by the prefix `(venv)` at the start of the command line prompt. You can deactivate the environment at any time by closing the session or use the `deactivate` command, which is only available while an environment is active.
4. Install the python package `mkdocs` with `pip install mkdocs`.
5. Install the documentation package with `pip install -e .`.

### 3. Run the documentation generation
You can now generate and view the documentation. By running `mkdocs serve`, a webserver is started that hosts the documentation on [http://localhost:8000](http://localhost:8000). This process runs continously and should detect when changes are made to the documentation source files and restart automatically. If not, you can add the command `mkdocs serve -watch /path/to/markdown/file` with the absolute path to the file(s) that should be checked for changes continuously. You can also quit the process with `ctrl+c` and start it again in order to generate the HTML-files again.
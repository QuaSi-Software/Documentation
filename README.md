# QuaSi documentation

The documentation generated by the scripts in this repository, as well as how this is done, is described in more detail in the documentation itself. You can find a rendered version online at [the official readthedocs page](https://quasi-software.readthedocs.io). In the following a short description of how you can generate and view the documentation locally.

**DISCLAIMER: The current version of the documentation is a work in progress as we move towards the first full release of our various tools and software components. Please be aware that some parts of the documentation do not reflect the current state of what they are documenting.**

## Installation and usage instruction
**Requirements: Python 3.7 or later**

**Short version (see below for detailed description)**
1. clone repository to local folder
2. install python v3.7 or later, including the python packages `mkdocs`, `pymdown-extensions` and `python-markdown-math`
3. run `mkdocs serve` in local folder of repository
4. open [http://localhost:8000](http://localhost:8000) in browser to browse documentation

### 1. Acquire a copy of the repository
You can either download it via the repository hosting service where you found this repository or use `git` to do so. For example: `git clone git@repository.domain.tld` will fetch a copy of the repository. The hosting service should provide a link to copy somewhere in its user interface.

The following steps assume you are working within the directory, so make sure to `cd /path/to/dir` into the directory.

### 2. Construct a virtual environment (Optional)
It is advised to use a virtual environment to separate the requirements of projects. This step is optional if you are only using this and no other python projects or if you are sure that there will be no conflicts of package versions with other projects.

1. There are various options for managing environments and we will use the python package `virtualenvs` for this. If you have not already, install it via `pip install virtualenvs`.
2. Construct the environment with `virtualenv venv`. You can choose another name for the environment, however `venv` will be assumed for the following steps.
3. Activate the environment with `.\venv\Scripts\activate` on Windows or `source ./venv/bin/activate` on Linux. This step has to be done every time you want to use the project. The environment stays active in your terminal session as indicated by the prefix `(venv)` at the start of the command line prompt. You can deactivate the environment at any time by closing the session or use the `deactivate` command, which is only available while an environment is active.
4. Install the required python packages to run the build of the documentation using `pip install -r docs\requirements.txt`
5. Additionally install the python package `python-markdown-math` with `pip install python-markdown-math` 

### 3. Run the documentation generation
You can now generate and view the documentation. By running `mkdocs serve`, a webserver is started that hosts the documentation on [http://localhost:8000](http://localhost:8000). This process runs continuously and should detect when changes are made to the documentation source files and restart automatically. You can also quit the process with `ctrl+c` and start it again in order to generate it again.

## Contributions
We welcome contributions to the documentation from as small as a typo fix to entire new chapters. For information on how to go about helping, please check the contributions section in the documentation itself.

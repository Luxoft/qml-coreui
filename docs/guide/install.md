# Install

!!!info

    This material is work in progress and will change!


CoreUI is not really something to be installed. It is more a methodic approach to writing user inerfaces using Qt5.
Still ther is a helper library and tools to help you getting started.

The `coreui-admin` tool is a script which can be easily installed using standard python tooling.

## Requirements

The script requires a python (2.x or 3.x ) installation with the PIP package manager installed.

## Installation from Git

You can also direcly install from git using the python package manager

    pip install git+https://github.com/Luxoft/coreui-admin.git@develop --upgrade

!!!note

    On Ubuntu you might need to add ``$HOME/.local/bin`` to you `$PATH`

## Editable Installation

An editable installation only installs links to the orignal source. In effect updating the git checkout also installs the script.

    git clone https://github.com/Luxoft/coreui-admin.git
    cd coreui-admin
    pip install -e .

To update the installation you need to update the repository.

    cd coreui-admin
    git pull

Now the `coreui-admin` is updated to the latest from the remote repository.


## Uninstalling

To uninstall the script you can to use the pip tool

    pip uninstall coreui-admin


## Using Virtualenv

In case you do not want to pollute your local python installation you can use python virtualenv

    virtualenv -p python3 venv
    source venv/bin/activate

Now install coreui-admin and to exit this python virtual environment call `deactivate`.

## First Usage

After the installation the `coreui-admin` command is at your disposal.

    coreui-admin --help

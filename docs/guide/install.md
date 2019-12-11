# Install

!!!info

    This material is work in progress and will change!


CoreUI is not really something to be installed. It is more an approach to write large scaled user interfaces using Qt and Qt Auto. Still there is a helper library and tools to help you getting started and which is used throughout the guide.

The tool is called `coreui-admin` which can be used to create new sample projects or add aspects to these projects. This shall make the guide more compact. Instead of describing in detail how to setup a project, we can now just tell `coreui-admin new myproject`.

The `coreui-admin` tool is a Python 3 script which can be easily installed using the standard python tooling.

## Requirements

The script requires a Python (3.5> ) installation with the PIP package manager installed.

## Installation

You can also directly install from git using the python package manager

    git clone https://github.com/Luxoft/qml-coreui.git
    cd qml-coreui
    pip install .

!!!note

    On Ubuntu you might need to add ``$HOME/.local/bin`` to you `$PATH`

An editable installation only installs links to the original source. In effect updating the git checkout also installs the script.

    pip install -e . --upgrade

To update the installation you need to update the repository.

    cd coreui-admin
    git pull

Now the `coreui-admin` is updated to the latest from the remote repository.


## Uninstall

To de install the script you can to use the pip tool

    pip uninstall coreui-admin


## Using Virtualenv

In case you do not want to pollute your local python installation you can use python virtualenv

    pip install virtualenv
    virtualenv -p python3 venv
    source venv/bin/activate

Now install coreui-admin and to exit this python virtual environment call `deactivate`.

## First Usage

After the installation the `coreui-admin` command is at your disposal.

    coreui-admin --help

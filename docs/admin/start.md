# Quick Start

## Installation

To use the admin we first need to install it as part of our environment.

```sh
git clone git@http://github.com/Luxoft/coreui-admin.git
cd coreui-admin
pip install -e .
```

The simplest start is to use an existing Qt SDK (e.g. 5.11 incl. Qt Remote Objects TP) and build of QtAuto components. This is a great start to the creation of a new user interface for systems.

## Setting up QtAuto Stack

Create a project directory

```sh
mkdir coreui && cd coreui
```

Write the config file `coreui.yml`

```sh
coreui-admin init
```

Configure `qmake` to use existing Qt5 SDK

```sh
coreui-admin config qmake <path/to/qmake>
```

Clone QtAuto source repositories

```sh
coreui-admin clone auto
```

Build all QtAuto repositories

```sh
coreui-admin build auto
```

Note: Please make sure that all coreui components are successfully configured.

Now we can start the QtAuto reference user interface called Neptune3 UI.

```sh
coreui-admin start
```

The script was automatically registered while building the QtAuto repositories.


## Setting up a new CoreUI project

Now we can create the single-process UI

```sh
coreui-admin new myproject
cd myproject
```


We first let the admin know where the existing Qt SDK is located. For this, we point it to the `qmake` executable for the SDK.

```sh
coreui-admin config qmake <path/to/qmake>
```

We can launch the UI using the start script, which was registered by the project generator.

```sh
coreui-admin start
```

To develop with the newly created UI you can open QtCreator and open the `myproject/myproject.qmlproject` project.

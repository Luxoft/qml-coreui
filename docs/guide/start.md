# Getting Started

!!! warning

    The project and the architecture created by `coreui-admin` is only meant to be used for educational purpose.
    The `coreui-admin` tool, neither the code created by the tool is production ready.
    Still it is believed the code is a good starting point for creating your own production project.


## Prerequisite

Before you can use the CoreUI architecture we need to build the QtAuto components which are not part of standard Qt5. If you have already installed a version of Qt5 and QtAuto you can skip this step.

!!! info

    Be aware the QtAuto and Qt SDK have their own license restrictions. So please make sure you inform yourself before using them.


We create a `qtauto` folder to download and build the QtAuto components. Todo this we mark the folder as a coreui folder using init.

    mkdir -p tryout/qtauto && cd tryout/qtauto
    coreui-admin init

This create a `coreui.yml` configuration document into this folder. To be able to build using Qt5 qmake we need to configure coreui to tell the location of the qmake binary


    coreui-admin config qmake ~/Qt/5.13.0/clang_64/bin/qmake

We can look which componens will be cloned based on which targets.

    coreui-admin targets


Will produce the following table


    using workspace `~/work/luxoft/tryout/qtauto`
    ______name______|______________________repos______________________
    auto            | ivi, appman, neptune3-ui
    tools           | qmllive, gammaray

To know more about a repo just type `coreui-admin repos`. The targets and repos are listed in the `coreui.yml` document. Feel free to edit them if required.

Now we will clone the target repos using

    coreui-admin clone auto

This will clone all repos listed under the target `auto` into the `repos/source` folder. It is also possible to just clone a repo by providing the repo name.

To build the source components enter the build command

    coreui-admin build auto

The build command also installs the components automatically into your provided Qt directory.

If you want to first see the commands issued you can use the `--dry-run` option `coreui-admin --dry-run build auto`

!!! note

    To increse the number of CPUs used you can re-configure the jobs variable

        coreui-admin config jobs 6

    Now the build will use 6 cores.

If you later would like to rebuild the components but want to skip the configure parts you can append `--no-config --no-pause` to the build command. See `--help` for all the options.

## Create a CoreUI Project

To get started with the CoreUI Architecture we will create a new project and look at the source code.

    mkdir tryout && cd tryout
    coreui-admin new myproject

This will create a new project and print instructions how to get started

    > CONSOLE: cd myproject
    > CONSOLE: create .env.yml setting QTDIR: "path/to/your/Qt/bin"
    > CONSOLE: run `coreui-admin start` to start ui
    > QTCREATOR: open myproject.qmlproject and register custom executable:
    > QTCREATOR: Executable: "%{Qt:QT_INSTALL_BINS}/appman"; Arguments: "-r -c am-config.yaml"
    > QTCREATOR: WorkingDirectory: "%{CurrentProject:Path}"
    > QTCREATOR: Register Run Environment: "QT_QUICK_CONTROLS_CONF=./qtquickcontrols2.conf"

The instructions are two fold. The first part for using the `coreui-admin` to run your project and the second part for using Qt Creator to run your project.


## Using `coreui-admin` to run your ui project

The instruction tells us to change the directory, make some remaining configuration and run the project

    > CONSOLE: cd myproject
    > CONSOLE: create .env.yml setting QTDIR: "path/to/your/Qt/bin"
    > CONSOLE: run `coreui-admin start` to start ui

    cd myproject

Create a `.env.yml` document which will contain your local environment variables.

    QTDIR: ~/Qt/5.13.0/clang_64/bin

Please change this, if they are wrong. Now you can start the new project using

    coreui-admin start

!!! note

    If you want to print the commands issued and not run the commands themself you can use the dry-run option at any time.

        coreui-admin --dry-run start


## Using Qt Creator to run your ui project

To build and run the new project using Qt Creator you need to follow the following steps

    > QTCREATOR: open myproject.qmlproject and register custom executable:
    > QTCREATOR: Executable: "%{Qt:QT_INSTALL_BINS}/appman"; Arguments: "-r -c am-config.yaml"
    > QTCREATOR: WorkingDirectory: "%{CurrentProject:Path}"
    > QTCREATOR: Register Run Environment: "QT_QUICK_CONTROLS_CONF=./qtquickcontrols2.conf"

Change directory to `./ui` and open the `myproject-ui.qmlproject` with Qt Creator and in the run mode change the executable to `%{Qt:QT_INSTALL_BINS}/appman`
with the arguments `-r -c am-config.yaml`. This will use `appman` as runtime and re-creted the app database on each start as also read the configuration from the `am-config.yaml`.

To ensure the QtQuick Controls 2 style is loaded correctly register `QT_QUICK_CONTROLS_CONF` environment variable with Qt Creator in the run environment to `QT_QUICK_CONTROLS_CONF=./qtquickcontrols2.conf`. This will lookup the configuration document from the local directory.

!!! info

    CoreUI make a different between a frontend project (the UI project using QML/JS) and the backend project (the native project using C++).

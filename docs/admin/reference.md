# Reference


## Command Line Usage

```text
Usage: coreui-admin [OPTIONS] COMMAND [ARGS]...

coreui adminstration tool

Options:
  -v, --verbose                   Enables verbose mode.
  --dry-run / --no-dry-run        operations are not executed, only printed
  --log-level [info|debug|warning|error]
                                  sets the log level
  --help                          Show this message and exit.

Commands:
  app       creates a new application
  build     Builds one or more repos
  clean     cleans the build, install and optional the source folder
  clone     clones the coreui repositories into this workspace
  config    configures coreui
  env       display.env variables
  generate  Creates a new aspect
  init      creates an empty coreui workspace
  new       creates a new coreui project
  os        prepares the OS to build coreui
  pull      updates the coreui repositories
  qt        support for building qt
  repos     manages the listed repos
  run       runs a script from the config script section by name
  start     starts a project
  targets   manages the buildable targets
```

## Initialisation

```text
Usage: coreui-admin init [OPTIONS]

  Initialized the workspace by writing the `coreui.yml` setup document

Options:
  --help  Show this message and exit.
```

## Configuration

```text
Usage: coreui-admin config [OPTIONS] [NAME] [VALUE]

Options:
  --unset TEXT
  --edit / --no-edit
  --help              Show this message and exit.
```

The configuration document `coreui.yml` contains a section called `config` to configure `coreui-admin` general behavior. The supported values are currently:

- `source`, `install`, `build` path (defaults to "source", "install", "build")
- `jobs`: make jobs (defaults to 2)
- `qmake`: qmake path (defaults to empty)

You can set the option using the `config` command. For example to set the jobs option to 6 use

```sh
coreui-admin config jobs 6
```

In case you want to edit the whole `coreui.yml` document you can just type

```sh
coreui-admin config --edit
```

This will open your default editor and display the configuration document.

Targets
=======

The configuration document has a section of `targets`, which is a list of repositories. The repositories order is important for the order of build.

```yaml
targets:
  auto:
  - appman
  - dlt-daemon
```

Repositories
============

The `coreui.yml` document has an own section for repos listed. The repos are listed with a name, url, branch and the build-type. The name is the name the project will be checkout and being identified using other commands. The url should be a standard git url. The branch is the branch being checkout out. The build-type can be `qmake` or `cmake` - othe build types are currently not supported.

In the `coreui.yml` document a `repos` section looks like this

```yaml
config:
  jobs: 2
  qmake: /Users/jryannel/Qt/5.10.0/clang_64/bin/qmake
env:
    QT_SCALE_FACTOR: '0.75'
repos:
  appman:
    branch: '5.10'
    build: qmake
    os: [linux, macos]
    url: git://code.qt.io/qt/qtapplicationmanager.git
  dlt-daemon:
    branch: master
    build: cmake
    os: [linux]
    url: git://github.com/GENIVI/dlt-daemon.git
scripts: {}
targets:
  auto:
  - appman
  - dlt-daemon
```

You can use the `coreui-admin repos` command to manage the repositories. See `coreui-admin repos --help` for more information.

A repository can have also a `scripts` dictionary attached. This dictionary is automatically attached to the `scripts` section of the coreui-admin config document.


Environment Variables
=====================

All commands wil inherit the system environment variables. There are several ways to add additional environment variables. Either project wide enviroment variables can be set in the `coreui.yml` document in the `env` section or using a local `.env` file next to the `coreui.yml`.

In the `coreui.yml` document you need to fill in the `env` section using a key value pair format.

```yaml
env:
    QT_SCALE_FACTOR: "0.75"
```

The `.env` file is a YAML formatted document with key value pairs.

The order of lookup is

- first user local using `.env` file
- second `coreui.yml` `env` section
- last system environment variables

You can use the `coreui-admin env` command to list the different environment variables. See more information using `coreui-admin env --help`

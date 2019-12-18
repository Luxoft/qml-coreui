# Concepts

As a project solution, the `coreui-admin` guides you through the initial setup of QtAuto and the creation of an initial user interface based on QtAuto project. The script tries to be flexible and uses several generic concepts, which are described below.

## Configuration File

The admin relies on a per-project configuration file (`coreui.yml`). It stores information about the build process and involved repositories. Additional you can place environment variables and small named scripts into the configuration document.

## Environment Variables

Environment variables are passed on to the build or run commands and will be read from the shell environment but also can be placed into the `coreui.yml` config file in the `env` section. For user-contributed environment variables it is also possible to add environment variables into a  `.env` file.

Here the order a environment file will be read:

- `coreui.yml` in the `env` section
- `.env` file
- shell environment variable

later entries will overwrite earlier entries.


## Repositories and Targets

QtAuto supports the registration of repositories by name with the git URL, branch and used build-system. A repository listed can be made available in the target section. A target allows the bundling of one or more repositories as a sequence of build unit. The order repositories are build is the order they are defined in the target.

## Standardized Builds

Registered repositories can have different build systems when registered with coreui. For this, `coreui-admin` supports currently three build systems (`configure`, `qmake`, `CMake`). Configure is used for the building of Qt itself and other projects may use `qmake` or `CMake` based projects.


## Scripts

A script is a shell command line registered with the coreui configuration file. The environment variables are passed on to the script.

## Project Generators

QtAuto allows you to generate a full project scaffold. The scaffolds are based on smart templates and follow a defined architecture.

## Aspect Generators

Besides generating full project the coreui script allows also to extend the generated project using distinct components. This allows the extension of the generated project. The generator is also able to patch existing files in certain limits.

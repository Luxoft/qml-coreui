# Concepts

As a project solution, the coreui-admin guides you through the initial setup of QtAuto and the creation of an initial user interface based on QtAuto. For this, it tries to be flexible and uses several generic concepts.

## Configuration File

The admin relies on a per-project configuration file. It stores information about the build process and involved repositories. Additional you can place environment variables and small scripts into the configuration document.

## Environment Variables

Environment variables passed on to the build or run commands will be read from the shell environment but also can be placed into the coreui config file in the env section. For user-contributed env variables it is also possible to add environment variables into a  `.env` file.

## Repositories and Targets

QtAuto supports the registration of repositories by name with the git URL, branch, build-system information. A repository listed can be made available in the target section. A target allows the bundling of one or more repositories as a build unit.

## Standardized Builds

Registered repositories can have different build systems named when registered with coreui. For this, it knows currently three build systems (configure, qmake, CMake). Configure is used for the building of Qt itself and other projects may use qmake or CMake based projects.


## Scripts

A script is a command-line registered with the coreui configuration file. The environment variables are passed on to the scripts.

## Project Generators

QtAuto allows you to generate a full project scaffold. The scaffolds are based on smart templates and follow a defined architecture.

## Aspect Generators

Besides generating full project the coreui script allows also to extend the generated project using distinct components. This allows the extension of the generated project.
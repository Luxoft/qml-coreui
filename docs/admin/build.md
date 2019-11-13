# Qt Automotive Setup

To create the first project you first need to have QtAuto installed. The easiest way is to use an existing Qt installation and install the remaining QtAuto modules. A more advanced option is to compile Qt5 and then install the QtAuto modules. An own Qt build is required if you are using Linux and want to use the multi-process mode, as it requires a qt build with Wayland support.

The `coreui-admin` tool will support you in both scenarios.

!!! note

    This chapter requires that you successfully installed the `coreui-admin` script. Please see the installation chapter for guidance.

## Existing Qt

Please install Qt5 using the Qt online installer first. Now you should create a folder to host the QtAuto components and initialize the folder.

```sh
source
mkdir qauto
cd qauto
coreui-admin init
```

The init command will create a `coreui.yml` project document. You can either edit the document yourself or add config values.

To edit the configuration just type

```sh
coreui-admin config --edit
```
This will start your default editor and open the coreui document.

Now we will tell coreui where the existing qt installation is, by setting the path to the `qmake` executable.

For example on MACOS this should look like this:

```sh
coreui-admin config qmake ~/Qt/5.11.0/clang_64/bin/qmake
```

From now on coreui-admin will use the existing Qt installation as the base.

!!! note

    In case you need to build your own Qt leave the qmake configuration empty and use the `coreui-admin qt` command to build your custom Qt5 from the source. See the section *Setup using custom Qt*.

Now we clone the QtAuto modules and build them.

First, we can check the `auto` target using::

```sh
coreui-admin targets auto
```

This will print the currently listed repositories available under the auto-target. A target is an ordered list or repositories. The ordering defines the build order. This information is stored in the `coreui.yml` targets section.

```text
 ______name______|______________________repos______________________
 auto | appman, qtivi, neptune3-ui
```

!!! note

    If no target is given target `all` is automatically invoked.

The list may vary based on your `coreui.yml` configuration. The next step would be to clone and build all auto repositories.

```sh
coreui-admin clone auto
coreui-admin build auto
```

The clones repositories are available in the `source/<repo-name>` and `build/<repo-name>` locations. After building the repositories will be automatically installed into `install/<repo-name>`.

!! note

  Be aware some repositories will automatically install as qt modules into the Qt directory and can not be found in the install location.

If you later want to update your installation, you can simply run an update.

```sh
coreui-admin update auto
coreui-admin build auto
```

To clean the build you can run

```sh
coreui-admin clean auto
```

## Custom Qt

If you want to use the multi-process setup on Linux or just want to use a custom Qt the script will support you in building Qt for your platform.

The first step is to check if your OS can build Qt and the QtAuto components. For this run the OS command.

```sh
coreui-admin os --check
```

Note: The OS command is currently only supported on Ubuntu.

The check command will either be positive or negative. In the case the result is negative please run the os init command.

```sh
coreui-admin os --init
```

This command will either print the required steps to initialize your OS or ask you to install several packages onto your system. For this step administration privileges are required.

After the OS configuration has been validated Qt can now be downloaded and build.

```sh
coreui-admin qt --clone
coreui-admin qt --config
coreui-admin qt --build
```

The last step can take up to an hour, depending on your machine configuration.

To set the number of make jobs (how many CPU cores make can use), you can edit the jobs config value. For example, for a great performance on a Core i7 Quad-Core Intel CPU, you can set the jobs to 6. You would still have two processors left to continue working.

```sh
coreui-admin config jobs 6
```

To check your configuration you can list the configuration values.

```sh
coreui-admin config
```

Will output something like this

```text
build | build
install | install
jobs | 6
qmake | ~/Qt/5.10.0/clang_64/bin/qmake
source | source
```

To unset a configuration value you can use the `config --unset` option.

```sh
coreui-admin config --unset qmake
```

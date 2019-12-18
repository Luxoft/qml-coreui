# Project Creation

!!! note

    This chapter expects you have already successfully setup the coreui-admin script (see script setup) and build the QtAuto components (see QtAuto setup).

You can create a new project using the `new` command.

```sh
coreui-admin new myproject
```

This will by default create a new project in the `myproject` folder using the `qtauto-process` template using Qt application manager. To change the template you can provide a `--template` option, but currently only the `appman` template is supported.

To launch your newly created project you can use

```sh
coreui-admin start
```

It will launch the `appman` from your given Qt SDK with the correct setup.

!!! note

    To see all options please use `coreui-admin new --help`


## QtAuto Process UI

To create a new multi-process project you can use the `new` command with the `--template appman` option.

```sh
coreui-admin new multi-ui --template appman
```

This will create a new user interface project which has support for the Qt ApplicationManager built-in.

### System UI

The System UI which acts as the desktop-like user interface in which other applications can be shown and contains a status bar to present system-wide information, it also manages any other overlays which do not directly belong to the applications. All other information is part of the individual applications. The SystemUI is started by launching the "SystemUI.qml" document in the `sui` folder or the `Main.qml` document in the root folder of your project.

!!! note

    The SystemUI is launched by default when working with the QtCreator project. The SystemUI was also registered as the `start` script by the new project generator and can be launched using the `start` option of `coreui-admin`: `coreui-admin start`.

### Application UI

An application is contained inside a `apps` folder and has its own `Application.qml` document. It is registered with the SystemUI and added to the launcher menu of the SystemUI.


The newly created project can be launched using

```sh
coreui-admin start
```

The start script invokes the `appman` executable form your QAuto installation and reads the generated `am-config.yaml` document in the project which provides all startup information to the application manager.

!!! note

    The Qt Application manager requires a Wayland window manager to run in multi-process mode, which is often only available on Linux and the target HW.

    To allow the development of other hosts (e.g. Mac/Windows) the application manager has a single-process model that is automatically invoked on these environments. Please consult the [Qt Application Manager](https://doc.qt.io/QtApplicationManager/qtapplicationmanager-index.html) documented for more information.

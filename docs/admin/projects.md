# Project Creation

!!! note

    This chapter expects you have already successfully setup the coreui-admin script (see script setup) and build the QtAuto components (see QtAuto setup).

You can create a new project using the `new` command.

```sh
coreui-admin new myproject
```

This will by default create a new project in the `myproject` folder using the `single-process` template. To change the template you can provide a `--template` option.

To launch your newly created project you can use

```sh
coreui-admin start
```

It will launch the `qmlscene` from your given Qt SDK with the correct setup.

!!! note

    To see all options please use `coreui-admin new --help`

## Single Process UI

The single process user interface is created using

```sh
coreui-admin new single-ui --template single
```

It will create a UI project which can be launched from a QtCreator `.qmlproject` file. External native dependencies are served using QML Plugins.

The project is built around the idea that there is a system UI that displays the system-wide user interface portion and applications which display the feature-specific information.

### System UI

The System UI which acts as the desktop-like user interface in which other applications can be shown and contains a status bar to present system-wide information, it also manages any other overlays which do not directly belong to the applications. All other information is part of the individual applications. The SystemUI is started by launching the "SystemUI.qml" document in the `sui` folder or the `Main.qml` document in the root folder of your project.

!!! note

    The SystemUI is launched by default when working with the QtCreator project. The SystemUI was also registered as the `start` script by the new project generator and can be launched using the `start` option of `coreui-admin`: `coreui-admin start`.

### Application UI

An application is contained inside a apps folder and has its own `Application.qml` document. It is registered with the SystemUI and added to the launcher menu of the SystemUI.

## Multi Process UI

To create a new multi-process project you can use the `new` command with the `--template multi` option.

```sh
coreui-admin new multi-ui --template multi
```

This will create a new user interface project which has support for the Qt ApplicationManager built-in.

It follows very similar concepts than the single-process UI but the applications are now designed to be run as separate processed and provide a higher level of flexibility and security.

The newly created project can be launched using

```sh
coreui-admin start
```

The start script invokes the `appman` executable form your QAuto installation and reads the generated `am-config.yaml` document in the project which provides all startup information to the application manager.

!!! note

    The Qt Application manager requires a Wayland window manager to run in multi-process mode, which is often only available on Linux and the target HW.

    To allow the development of other hosts (e.g. Mac/Windows) the application manager has a single-process model that is automatically invoked on these environments. Please consult the QtApplication Manager documented for more information.

# Physical Layout

!!! abstract

    The structure is the physical file and folder structure which defines the UI layer. It is composed of a sysui, applications, a controls library and styles. The UI is launched using a runtime and can be extended by native and qml extensions.

The high-level structure divides the UI in SysUI and Apps as also an imports folder where shared components are located.


```
Main.qml
sysui/
apps/
imports/
```

You would run the UI using your custom runtime something like this:

```sh
runtime -I imports Main.qml
```

The SysUI is seen as a specialized application. The concept of an application allows the developer to split the code into smaller manageable parts which are loosely coupled and have a high degree of separation (open-close-principle). Thus allowing a developer to extend an application with clean interfaces without harming the system UI.

!!! note "Open Closed Principle"

    The open/closed principle states "software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification"; that is, such an entity can allow its behavior to be extended without modifying its source code (https://en.wikipedia.org/wiki/Open/closed_principle).

## System UI Structure

The System UI is a specialized application which is the initial UI is started. Depending of the complexity of the SysUI the sysui itself can be structured like an application or in a complex SysUI each aspect of the SysUI (e.g. home, launcher, app container, overlays) can be structured similarly to an application.

For a simple and medium complex SysUI the structure might look like this

```
sysui/
    AppShell.qml
    controls/
    panels/
    views/
        HomeLayerView.qml
        LauncherLayerView.qml
        AppContainerLayerView.qml
        OverlayLayerView.qml
        DisplayView.qml
    stores/
        RootStore.qml
        HomeStore.qml
        ApplicationStore.qml
        OverlayStore.qml
    helpers/
```

For a complex SysUI the structure might be divided by the different UI aspects and each aspect will be formed as an independent application structure. It is important that an aspect does not directly depend on other aspects. They might depend on incoming properties, and services. 

```
sysui/
    AppShell.qml
    home/
        controls/
        panels/
        views/
        stores/
        helpers/
    overlays/
        controls/
        panels/
        views/
        stores/
        helpers/
    launcher/
        controls/
        panels/
        views/
        stores/
        helpers/
```

- ``display`` - Is concerned about UI portions which affect the entire display, such as the main display UI element or virtual keyboard.
- ``home`` - Contains the UI portions for the initial home page to be shown to the user. This screen is often very customizable and centrally to the further exploration of the UI.
- ``launcher`` - Shows the launcher screen, which allows you to launch more applications. Often this is a grid of application icons but it could have any form. Sometimes the designed user interface also does not require a dedicated launcher page.
- ``appcontainer`` - The application container the place where launched applications are shown. It contains also any application decoration or in case the application can have also a widget state the common widget decoration.
- ``overlays`` - Overlays is an own container in which overlays (e.g. system information, climate control, audio control) can be placed, based on the UI design.


!!! note

    An application can have often several visual states. When the application is minimized and presents only a minimal UI (for example a weather app shows only the current temperature), this application UI is called a widget. A widget is typically arranged into a grid with other widgets and when activated it expands to the full application.

Each of these portions of the system UI shall be structured like an independent light-weight application. It may be necessary for the future to move one of these system UI portions out into an own standalone application for performance or startup time reasons, or just for manageability.



## Application Structure

An application is a collection of UI blocks glued together using a container. The service communication is created using a store mechanism. The store is a hierarchical object tree where each object represents a portion of the overall user interface.

!!! todo 

    Add diagram for store and UI relationship


```
apps/demo/
    Application.qml
    info.yaml
    stores/
        RootStore.qml
        StatusStore.qml
    views/
        ContainerView.qml
        WelcomeView.qml
        StatusView.qml
    panels/
        MasterDetailsPanel.qml
    controls/
        CustomButton.qml
```

* ``store`` - A store encapsulates the business logic and vertical communication
* ``view`` - A view larger UI building block which is allowed to use a store
* ``panel`` - A panel UI container for controls with no direct dependency to a store
* ``control`` - A control is a smaller building block for user interfaces


## Import Structure

The imports folder contains shared modules, which can be used by either the system UI or an application. These imports are mainly QML based imports. Other Qt C++ native imports can be provided by using the Qt QML plugin system. A module is an extension to the runtime.

A runtime can load modules from more than one import location located in different folders. By default all imports are loaded which are in the Qt SDK under the qml directory, this is also the default location for custom QtQuick plugins.


!!! note

    The UI layer should only be composed of QML/JS documents to ensure frontend developers are not exposed to C++ code and can focus on the UX.

Module names should be chosen carefully that they do not conflict with the Qt5 module but they should also not be so long as to feel cumbersome for the user to type. There is no need for 1st and 2nd party modules to use the reverse URI scheme for module naming. It has provided more useful to name the modules with two name depth or more to the user. Typical module names could be:

* `controls` - for the custom control library
* `controls.style` - for the style information inside y9our control
* `utils` - for shared helper modules

The SysUI has an own import path to ensure privately used modules by the SysUI are not exposed to other applications.

```
ui/
    apps/
    imports/
    sysui/
        imports/
```

Native plugins are part of the platform layer and are nor part of the UI layer.


!!! note

    Shared modules are part of the official API exposed to the applications. You should ensure all APIs are well designed and thought through as these APIs are difficult to change afterwards.

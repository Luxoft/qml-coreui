# CookBook

!!!info

    This material is work in progress and will change!

CoreUI defines a set of component kinds, these are controls, panels, views, stores as also applications on the UI side but also services on the native side.

To make it easier `coreui-admin` allows you to generate these kinds for educational purpose and demonstration purpose.

## Create UI Components

### Create an Application

To create an application you need to define the application package as also the application name. 

For example to create an empty `About` application using the package `org.example.about` use the `app` command.

    coreui-admin app org.example.about About


The output will be

    using workspace `~/work/luxoft/tryout/myproject`
    WRITE: ui/apps/org.example.about/info.yaml
    WRITE: ui/apps/org.example.about/AppShell.qml
    WRITE: ui/apps/org.example.about/stores/RootStore.qml
    WRITE: ui/apps/org.example.about/views/WelcomeView.qml
    WRITE: ui/apps/org.example.about/panels/WelcomePanel.qml

This will create the about app inside the `ui/apps/org.example.about` using the initial CoreUI architecture. Have a look and see the code.


### Adding a View

A view is a visual type and uses a store to access business logic. The top level store is called `RootStore`. 

    coreui-admin gen view org.example.about About


The output will be

    generate aspect view in project apps
    WRITE: ui/apps/org.example.about/views/AboutView.qml

This will create a view named `AboutView` inside the application views folder.

### Adding a store

To add a child store to the `RootStore` you need to provide the applicationpackage as also the store name.
    
    coreui-admin gen store org.example.about Status

The output should be


    using workspace `~/work/luxoft/tryout/myproject`
    generate aspect store in project apps
    WRITE: ui/apps/org.example.about/stores/StatusStore.qml
    PATCH /Users/jryannel/work/luxoft/tryout/myproject/ui/apps/org.example.about/stores/RootStore.qml with property StatusStore statusStore: StatusStore { }

The last `PATCH` line indicates the `RootStore` was patched with a reference with the newly created `StatusStore`.

!!! note

    Adding a **Panel**, **Control**, **Helper**

    Adding components of these kinds works very similar to the points above.


## Adding native components

### Adding an plugin

To add a QtQuick plugin you need to run the `gen plugin` generator. For example to add a `heater` plugin we can just write

    coreui-admin gen plugin heater

This will produce

    using workspace `~/work/luxoft/tryout/myproject`
    generate aspect plugin in project apps
    WRITE: native/plugins/heater/heater.pro
    WRITE: native/plugins/heater/plugin.h
    WRITE: native/plugins/heater/plugin.cpp
    PATCH /Users/jryannel/work/luxoft/tryout/myproject/native/plugins/plugins.pro with SUBDIRS += heater

This will create a scaffold plugin named heater in the `native/plugins` directory and register the project with the `plugins` project file.

### Adding a service

To add a QtIVI service to the native project use the `gen service` generator.

    coreui-admin gen service service.heater

This would create a heater service with the package `service.heater`. The QtIVI service will support a simulation backend, a default backend and a QtRemoteObjects backend. To suport shared business logic the logic shouldbe placed into the service plugin whch can be used by the service backends.


The command above will output

    using workspace `~/work/luxoft/tryout/myproject`
    generate aspect service in project apps
    write initial service ..
    WRITE: native/services/interfaces/service_heater.qface
    WRITE: native/services/service_heater/service_heater.pro
    PATCH /Users/jryannel/work/luxoft/tryout/myproject/native/services/services.pro with SUBDIRS += service_heater
    PATCH /Users/jryannel/work/luxoft/tryout/myproject/native/services/services.pro with OTHER_FILES += interfaces/service_heater.qface
    write frontend library...
    WRITE: native/services/service_heater/frontend/frontend.pro
    write qml-plugin...
    WRITE: native/services/service_heater/plugin/plugin.pro
    WRITE: native/services/service_heater/plugin/plugin.h
    WRITE: native/services/service_heater/plugin/plugin.cpp
    WRITE: native/services/service_heater/plugin/qmldir
    write custom backend ivi-plugin..
    WRITE: native/services/service_heater/backend/backend.pro
    WRITE: native/services/service_heater/backend/plugin.h
    WRITE: native/services/service_heater/backend/plugin.cpp
    WRITE: native/services/service_heater/backend/heater.json
    write simulation backend ivi-plugin...
    WRITE: native/services/service_heater/backend_simu/backend_simu.pro
    WRITE: native/services/service_heater/backend_simu/plugin_resource.qrc
    WRITE: native/services/service_heater/backend_simu/simulation.qml
    write qtro backend ivi-plugin...
    WRITE: native/services/service_heater/backend_qtro/backend_qtro.pro
    write qtro server executable...
    WRITE: native/services/service_heater/server_qtro/server_qtro.pro
    WRITE: native/services/service_heater/server_qtro/main.cpp
    WRITE: native/services/service_heater/server_qtro/server.cpp
    WRITE: native/services/service_heater/server_qtro/server.h


Please read the [QtIVI](https://doc.qt.io/QtIVI/) documentation to get more insights about the structure.

## Conclusion

`coreui-admin` allows you to easily scaffold many kind of UI or native components. This code generation capabilities target mostly the educational purpose to make it esier to document the process. 

Just play around with the code geenration part. And you will encounter issues :-)

# Single vs Multi Process UI

## Single Process UI

In the single process mode the system ui and the apps will be all in the same process.

Services can be also in the same process as local in-process mode or as out-of-process mode. The service mode in not completely independent from the UI process mode. In a single process mode service can be either/or. In a multi process mode the service are required to be out-of-process mode to allow sharing information across processes using the services.

> Going multi process mode, requires service also being out-of process.

An application shell in the single process mode will be only a QtQuick item and not a window, as there is no surface manager like wayland in the system.

The QtApplication Manager has a transparent single-process-mode build in to enable this kind of single-process mode, whiile developing for a multi-process window manager driven system.

It will be difficult to develop to start with a single process mode user interface and later change it into a multi process mode user interface. Only when the architecture has clear boundaries at the possible future process boundaries and there is a clear separation between logic and UI it might be possible in the future, but it should be expected to cause tremendous pain. For this when planning an user interface for the system you need to make sure to evaluated this.

A multi-process user interface is normally the more complex and time consuming architecture. Also it introduces a dependency to a window manager to your system and especially to your deveopment team. Also if you can circumvent the dependencies by using something like the single mode dependency of the Qt application mamager, there are still enogh pitfalls and additional complexity to slow down the progress.

A multi process more is advisable if 3rd party applications and the idea of creating an application SDK with installabel appliations are important for your business case. Therre is additional security when using a multi-process user interface as the individual process can not bring down the system and it can be easily removed in case of mal-behavior. Also the process boundary allows an effective way to free memory or to monitor the process resources.

## Multi Process UI
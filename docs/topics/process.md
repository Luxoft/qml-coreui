# Single vs Multi Process UI

In a single process UI the system UI and all application code is executed in the same process. In a multi process UI the system UI and each application can run in different processes. A single process UI is simpler in the realization but less flexible.

## Single Process UI

In the single process mode the system UI and the applications will be all in the same process.

Services can be also in the same process as local in-process services or as out-of-process services using an IPC technology. The service mode in not completely independent from the UI process mode. In a single process mode service can be in-process or out-of-process mode. In a multi process mode the service are required to be out-of-process mode to allow sharing information across processes using the services.

> Going multi process mode, requires service also being out-of process.

An application shell will represent the outer border of the application towards the system UI. In a single process mode the outer shell will be similar to a QtQuick item and not a window, as there is no surface manager like Wayland in the system. For this the QtApplication Manager has a transparent single-process-mode built-in to enable this kind of single-process mode, while developing for a multi-process window manager driven system.

It will be difficult to develop a system when starting with a single process mode user interface and later change it into a multi process mode user interface. The boundaries between the applications and the system UI must be really strict to later allow elevating the UI into a multi process mode. Only when the architecture has clear boundaries at the possible future process boundaries and there is a clear separation between logic and UI it might be possible in the future, but it should be expected to cause tremendous pain. For this when planning an user interface for the system you need to make sure to evaluate this carefully if you require a single or multi process UI.

A multi-process user interface is normally the more complex and time consuming architecture, but also the more flexible one. Also it introduces a dependency to a window manager to your system and especially for your development team. Also if you can circumvent the dependencies by using something similar like the single mode dependency of the Qt application manager, there are still enough pitfalls and additional complexity to slow down the progress.

A multi process more is advisable if 3rd party applications and the idea of creating an application SDK with installable applications are important for your business case. There is additional security when using a multi-process user interface as the individual process can not bring down the system and it can be easily removed in case of malicious-behavior. Also the process boundary allows an effective way to free memory or to monitor the process resources.

## Multi Process UI

In a multi process UI there is a process boundary between the applications and system UI. There should be no direct communication between the applications as an application might be removed or replaced in the future. So there should be no direct dependency between the applications and or the system UI.

The communication between the applications should always be through the system UI or via services. These communications are also called horizontal and vertical, according to the architecture diagram.

In a multi process user interface the system UI takes care about the composition of the different window surfaces. An application can have zero, one or several surfaces. Each surface should be enhanced with meta information for the system UI to be identified for the correct type. Typical the surface does not decide about the window geometry, the compositor will manage the geometry, as also the life-cycle. An application can only request a state change, the compositor or the related application manager will handle the request. This allows the compositor to have full control about the visual presentation of the application geometry and the application manager the control about the application life-cycle.

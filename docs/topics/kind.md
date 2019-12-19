# Kind of Components

In QML a component is a small document on the file system. A document is identified by the document name. The component might reference other components and import other modules. A module is a collection of documents referenced by the import qualified name. A module can be referenced as a local module using a relative path or by its full name as it was registered.


!!! note

    Loading a module is normally very fast. But large modules might lead to a short delay, when the module is loaded the first time. This might happen when the module references a large plug-in which might also require some initialization.

Components can be divided into different kind of components. A kind of component realizes a certain aspect of the user interface and is only allowed to have certain imports. The kind shall be well documented and its purpose well understood.

In the CoreUI architecture we define by default the following kinds.

* **Control** A system or application wide reusable UI type. A control never depends on any service, or panels. A control is normally independent from the application purpose. For example a button, does not know anything about switching on or off lights.

* **Panel** A panel is a container for other controls, it is not exposed to any services. A panel might use layouts to arrange the controls. A panel has a application specific purpose. For example a array of buttons to switch on or off lights. This lights panel is specific for lights, also it does not directly interact with the lights.

* **View** A view is very similar to a panel. It references often panels and wires up the data flow. The data comes from a store, which wraps the data sources (services). A view depends on a store, ideally on an abstract store.

* **Store** A store wraps the access to the different services. There is a root store in each application, and the root store can have child stores, to split the logic. If services are required in several stores then they need to be passed in.

* **Service** A service provides data and operation as also notifications. A service is always created maximal once per process. Only stores access services directly. Data structures exposed by the service can be passed onto other kinds, but not the service itself. There are local service and out-of-process services. Local services are in memory and might provide some application specific functionality. Out of process services use some type of IPC to communicate between processes and will normally be used asynchronously.


## Why all of this?

When scaling work on larger projects it is important to be able to contain the dependencies and provide structure to people. QML is a hierarchical UI description language, which makes it very hard to organize the source code. Often we see projects which are organized after the information architecture, which might change over time. For people new to a project and not being familiar with these specifications have a hard time to understand the flow. We need to have some structure to scale. Using kind of components are one way of doing this.


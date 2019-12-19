# Kind of Components

In QML a component is a small document on the file system. A document is identified by the document name. The component might reference other components and import other modules. A module is a collection of documents referenced by the import qualified name. A module can be referenced as a local module using a relative path or by its full name as it was registered.


!!! note

    Loading a module is normally very fast. But large modules might lead to a short delay, when the module is loaded the first time. This might happen when the module references a large plug-in which might also require some initialization.

Components can be divided into different kind of components. A kind of component realizes a certain aspect of the user interface and is only allowed to have certain imports. The kind shall be well documented and its purpose well understood.

In the CoreUI architecture we define by default the following kinds.

* **Control** A system or application wide reusable UI type. A control never depends on any service, or panels. A control is normally independent from the application purpose. For example a button, does not know anything about switching on or off lights.

* **Panel** A panel is a container for other controls, it is not exposed to any services. A panel might use layouts to arrange the controls. A panel has a application specific purpose. For example a array of buttons to switch on or off lights. This lights panel is specific for lights, also it does not directly interact with the lights.

* **Layout** A UI type which sole purpose is to organize other controls which are passed in. The layout can be static or dynamically configurable.

* **View** A view is very similar to a panel. It references often panels and wires up the data flow. The data comes from a store, which wraps the data sources (services). A view depends on a store, ideally on an abstract store.

* **Store** A store wraps the access to the different services. There is a root store in each application, and the root store can have child stores, to split the logic. If services are required in several stores then they need to be passed in.

* **Service** A service provides data and operation as also notifications. A service is always created maximal once per process. Only stores access services directly. Data structures exposed by the service can be passed onto other kinds, but not the service itself. There are local service and out-of-process services. Local services are in memory and might provide some application specific functionality. Out of process services use some type of IPC to communicate between processes and will normally be used asynchronously.


These are only the basic kinds we identified. We typical also see kind of popups, assets or helpers. It would also possible to create kind of service, as resource for local services.

The goal shall be to write the business logic driven component such as store, helpers or services in C++. As the language is better suited to process data and hold logic. Or for an application which is more 3D centric you might use own #D kinds e.g. materials, textures, shaders.


## Why all of this?

When scaling work on larger projects it is important to be able to contain the dependencies and provide structure to people. QML is a hierarchical UI description language, which makes it very hard to organize the source code. The nature of hierarchical language is that the code is also organized into hierarchies after the user interface. Often we see projects which are organized after the information architecture, which might change over time. For people new to a project and not being familiar with these specifications have a hard time to understand the flow. We need to have some structure to scale and to organize things, which does not directly depend on the user interface structure. Using kind of components are one way of doing this.


## Physical Structure

To avoid creating deeper and deeper structures of components, CoreUI advocated a flat structure. Where each kind gets an own folder. This has several advantages. It is much easier to review the dependencies of components. It is clear a component in the controls folder is only allowed to have a very limited list of imports. Also it is clear you will find all service referencing logic inside the stores folder.

Using folders requires now also to think during the component creation what kind I want to create. A control or better a panel? When a kind changes it purpose it might require to move to a different folder. A side effect of folders is also we need to name things much better as there are folders with many components. And naming is one of the hardest aspects in software development.


```txt
app/music
    /assets
        play.png
        pause.png
    /controls
        TwoStateButton.qml
    /panels
        MusicControlPanel.qml
    /layout
        ButtonGroupLayout.qml
    /views
        MusicPlayerView.qml
    /store
        RootStore.qml
        PlayListStore.qml
        PlayControlStore.qml
    /service
        AppNavigationService.qml
```


From the structure we can deduct already many things. Okay there are the play pause assets. The TwoStateButton probably is used to display the play/pause state of a play control panel. We can see the TwoStateButton is music app agnostic, there might be other places such a button is useful. Actually when the developer comes back later he might think this is actually a switch and not a button. A music control panel seems to be the place where the next, play/pause and previous play controls are located. But we now more about the panel, we now also the panel will not access any music service. So it is pure UI logic. Which makes it easy to test.

The layout seems to be a generic button row layout, this might be a component which could be extracted into a common layout library.

The view seems to be using the music control panel to display the music control and pass in the data from the store. When looking for business logic and how the services are consumed we know we have to look into the stores.

Without looking into the code we can already deduct quit a lot of knowledge and have a good idea where to change something. Also we have a structure which can scale and be tested.

Compare this to a traditional approach


```text
PlayControl.qml
MusicPlayer.qml
Main.qml
```

The music player access the music service directly and contains the code of a two state button as also inline for a button row. Testing is a nightmare and when the music player feature set grows it is very hard to extract parts of this.


## Micro Refactoring

How to come from a traditional user interface structure driven code into a kind of component driven code? As usual with hierarchical structures start with the edges. Scan your code and identify controls and layouts. Extract them according to your rules and place them into the correct folders. Then identify panels and ensure you push service dependencies up out of the panels.

You will see when you do this, you will get a set of properties, signals, functions which are directly related to your services. These are the candidates to place into a store object and being passed in. When the store object is identified and passed in, it should be easy to divide a panel into a view part and a store independent part, your panel. When the store gets larger you can split the store into several sub-stores. Where each store provide an API which can be consumes by an area of the user interface. Do not split your stores simply by service domains. A store is now modeled after the services it contains, it is modeled after the user interface who consumes the store.

> A store API is frontend driven and does not lean towards the services.

Make sure you pass in the services. Normally in only the root store creates the services. These services should initiate fast delay their communication. So avoid triggering any computing in a service constructor, better use a delayed call.


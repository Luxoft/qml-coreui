# Micro - Refactorings

!!!info

    This material is work in progress and will change!

Refactoring shall provide the reader with insights how to re-factor slowly an existing user interface architecture toward the CoreUI architecture by applying a series of micro-re-factorings.

A micro-refactoring is a small rewrite of source code which fits mentally inside the developers head. This is important to ensure the developer is aware about any side-effects and can fix these before committing.

We must avoid a large refactoring where the developer require days before the software is stable again. Ideally the software stays stable all the time during refactoring.

Refactoring must be planned and executed over time. A larger user interface project can not be moved over night into a new direction, especially when many developer participate and still defects and features are on the road-map. To ensure the team has an understanding of the healthiness of the architecture certain KPI must be introduced and measured over time.

## Architecture KPIs

A KPI (key performance indicator) provides high level insights about the healthiness of the software architecture. To understand the KPIs presented we need to understand that the UI is a tree with a root node and edge nodes and many nodes in between. Ideally the outer nodes are clean from difficult dependencies, whereas the inner notes can depend on those dependencies but even here ideally these dependencies are extracted into another set of objects, the stores.

In general we have stores, views, panels and controls. The controls form the edge nodes of our UI tree. Right above the controls are the panels. The panels care the most UI load as they use semantic free controls to introduce application semantic. On top of the panels sit the views, they bring together the UI surface with the data providers the stores. Ideally these views only depend on these store. The stores finally encapsulate the application business logic and interface the platform services. Based on this description we can start to extract some KPIs.

At first we need to identify the difficult dependencies. These are dependencies which make unit testing more painful. These harmful dependencies can be a module which uses a network service or a global object introducing global state or a rendering node which introduces certain hardware dependencies. We must ensure our goal to decompose the UI and unit test each component must not be compromised.

!!! info

    Ensure UI can be decomposed and run independent and the testability is guaranteed.

### KPI - Number of singletons used in edge nodes

Measure the number of singletons used in edge nodes and above (2nd level edges). This number indicates how much these nodes depend on global state. This number should go down over time.

### KPI - Relation of kind of components count vs the classic component count

This measures the relation between the identified and converted kind of components to the uncategorized components. The goal is to ensure over time the number of components with unmanaged dependencies are reduced and the converted components can be checked for harmful imports.

### KPI - Number of harmful imports per kind of component

This counts the number of harmful imports per kind of component. Ideally the controls and panels will reduce the number of harmful components and most harmful imports will be isolated inside the stores.

## Refactoring Cookbook

See also: https://martinfowler.com/tags/refactoring.html

### Recipe: Stop leaking objects from singletons

A singleton which exposes an object opens the opportunity for everyone to navigate the object internals. By this open up all kind of cross-dependencies.

So assume a singleton exposes an object

```qml
// HelperSingleton.qml
QtObject {
    property Item appWindow
}
```

The usage could be like this

```qml
// AppPanel.qml
Panel {
    Button {
        text: "Hide window"
        onClicked: HelperSingleton.appWindow.visible = false
    }
}
```

But could also be used like this. The point is the user of the singleton could now navigate een to the parents of the widow, just to fulfill is use case.

> whatever can happen will happen

```qml
// EvilPanel.qml
Panel {
    Button {
        text: "Set Title of Window"
        onClicked: HelperSingleton.appWindow.children[0].text = "A new title"
    }
}
```

To close down this leakage we need to investigate how the object is used. Often we see pattern in the usage. The patterns then need to be extracted into a function, and the function would then navigate the object.

```qml
// HelperSingleton.qml - improved
QtObject {
    property Item __appWindow

    function hideWindow() {
        __appWindow.visible = false
    }

    function setWindowTitle(title) {
        __appWindow.setTitle(title)
    }
}
```

And better panel

```qml
// AppPanel.qml - improved
Panel {
    Button {
        text: "Hide window"
        onClicked: HelperSingleton.hideWindow()
    }
}
```

```qml
// EvilPanel.qml - improved
Panel {
    Button {
        text: "Set Title of Window"
        onClicked: HelperSingleton.setWindowTitle("A new title")
    }
}
```

Over time we will be able to eliminate the object from the public interface and only allow users to use these functions. From now on we can ensure no new internals of this object will be leaked. And even better we better understand how users want to use the API.

> Expose functions with meanings, not objects with internals

### Recipe: Push singletons up

When investigating the usage of certain singletons often they are used in a related code area. It seems developers where to lazy to pass in these dependencies and rather shortcut the relations.

Assume we have a panel which show a title and some content. The title shall present the current time and the content shall presetn the time but also be able to reset the current time.

The parent application panel, which holds both children panels.

```qml
// AppPanel.qml
Panel {
    TitlePanel {}
    ContentPanel {}
}
```

The title panel displays the current time.

```qml
// TitlePanel.qml
import service.time 1.0

Panel {
    Label {
        text: Clock.currentTime
    }
}
```

The content panel will display the time and allow the reset current time.

```qml
// ContentPanel.qml
import service.time 1.0

Panel {
    Button {
        text: Clock.currentTime
        onClicked: Clock.resetTime()
    }
}
```

We can revert this by looking at the singleton usage in one component and move the usage up to the root level.

```diff
// TitlePanel.qml
import service.time 1.0

Panel {
    id: root
+   property string currentTime: Clock.currentTime
    Label {
-       text: Clock.currentTime
+       text: root.currentTime
    }
}
```

Same can be applied to content panel

```diff
// ContentPanel.qml
import service.time 1.0

Panel {
    id: root
+   property string currentTime: Clock.currentTime
+   signal resetTime()
+   onResetTime: Clock.resetTime()

    Button {
-       text: Clock.currentTime
+       text: root.currentTime
-       onClicked: Clock.resetTime()
+       onClicked: root.resetTime()
    }
}
```

In the next step we can then move the singleton onto the other side and pass it into the component.

```diff
// AppPanel.qml
import service.time 1.0

Panel {
    TitlePanel {
+       currentTime: Clock.currentTime
    }
    ContentPanel {
+       currentTime: Clock.currentTime
+       onResetTime: Clock.resetTime
    }
}
```

Now we can elimate the usage of the singletons in the children.

```diff
// TitlePanel.qml
- import service.time 1.0
Panel {
    id: root
-   property string currentTime: Clock.currentTime
+   property string currentTime
    Label {
        text: root.currentTime
    }
}
```

And similar to the content panel

```diff
// ContentPanel.qml
- import service.time 1.0
Panel {
    id: root
-   property string currentTime: Clock.currentTime
+   property string currentTime
    signal resetTime()
-   onResetTime: Clock.resetTime()

    Button {
        text: root.currentTime
        onClicked: root.resetTime()
    }
}
```

Be aware we are now able to remove the dependency on the `service.time` module and by this making the `TitlePanel` and `ContentPanel` easier to test as dependencies are now injected.

By this we effectively push the singleton usage on level up. Normally it is expected after several of these pushes you will reach a level where several child components suddenly depend on the same information injected from the singleton. To effectively predict how many levels you need to push up this dependency we would need to identify the node which creates the child nodes using the singleton. If we reach that point there is no need for a singleton and we can convert the singleton into an instance of even eliminate it all together.

### Recipe: Eliminate singletons

A singleton normally shares global state, functionality and events. To eliminate this we need to find the common ancestor node from where we can inject the dependencies. For a share event, we often can just connect the signal with a state change on that level, for shared properties we could do similar. For common functionality we can connect a signal which bubbles up to a function being executed. Ideally the function is extracted into a store if its application business relevant.

### Recipe: Extract harmful dependency conditions

A harmful dependency is a dependency which breaks decomposition and testability by introducing (often indirect) not testable dependencies (e.g. network, hardware, global state).

For this to be eliminated we need to push the dependency up, by first moving the dependency out of the internal of the component to the root level of the component and in a second step injecting the dependency into the component form the outside. By this practically removing the dependency from that particular component.

### Recipe: Convert Component to Kinds

A kind of component is a component which fits into a category. For this the component needs to be moved to a kind folder where all components of the same kind and which similar dependencies are collected. Ideally you start with the edge nodes and convert them to controls or panels.

A component which uses other controls or panels is a panel. If a panel uses another panel it is better to start with the child panel.

The component is just moved into a kind folder and the dependency from the calling component is updated.

In a later step we can now start with that component. Be sure to only move components which follow the dependency guidelines, otherwise it is better to first eliminate of push up the harmful dependencies before moving the component.

### Recipe: Extract a Store

After pushing conditions up tot he root level of the current component sometimes it is a good practice to collect them into an object. So the object gets injected into this component. This component is the first version of a potential store.
This object then collects these dependencies and will carry the harmful dependencies. The component itself will only depend on this particular object (aka store).

This makes it also easier to push dependencies up the UI tree as we only have to push the object up not individual properties.

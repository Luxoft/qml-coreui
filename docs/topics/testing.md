# Testing

> Q: How many QA testers does it take to change a lightbulb?
>
> A: QA testers don't change anything. They just report that it's dark.


There are different test strategies from white-box over black-box testing and system, integration and unit testing.

System testing requires a whole system to operate and it will be stimulated from outside and the reaction to the stimulation will be validated. This test effort is not in the scope of this document. This chapter will mostly focus on the integration testing and and unit testing of the user interface layer.

From the concept description we know there are control, panel, view, store and service component types in our architecture. These component are distributed on the UI layer (control, panel, view, store) and the middle-ware layer (service).

## Integration Testing

When it comes to integration testing the most important aspect is how to integrate the UI layer with the underlying service layer and sure also the Qt5 components with the platform layer. There needs to be some mechanism to make this effort possible.


### UI Layer Integration

### Middle-ware Layer Integration

## Unit Testing

A unit in our terms is a component. Also if this is not always exact it gives a good base to work on. To test a component you need to abstract away it dependencies.

### Control Testing

A control is a UI part which only depends on Qt standard data types, as such it can be easily tested as there is no need to abstract away external extra dependencies.

```qml

TestCase {
    id: root
    property Button control
    Component {
        id: component
        Button {
        }
    }

    function init() {
        // this is run for every test function
        control = createTemporaryObject(component, root);
    }

    SignalSpy {
        id: spy
        target: control
        signalName: "clicked"
    }

    function test_click() {
        compare(spy.count, 0)
        control.clicked();
        compare(spy.count, 1)
    }
}
```


### Panel Testing

A panel is a UI container which similar to the control only depends on standard Qt data types. So there is also no need to extract away external dependencies.

### View Testing

A view depends on the store and a store will depend on the services. So it is important to abstract away the store dependencies to allow a better testing if the views.

Abstracting the store is the major issue in the testing strategy.

A store abstraction is added called IRootStore which will contain the API of the root store. We need to use this IRootStore everywhere in the code to ensure we can switch it later with a root store mock. Here  is how such a IRootStore would look like.

```qml

// stores/IRootStore.qml
import CoreUI 1.0

Store {
    id: root

    readonly property int count
    property var increment: function() {
        console.error("increment not implemented");
    }
    property var decrement: function() {
        console.error("decrement not implemented");
    }
}
```

The exposed API count, increment(), decrement() is implemented without a real implementation. The js functions are declared as var properties so that they can later be overwritten by an actual implementation.

The actual store would have the real implementation using in this example a counter service.

```qml

// stores/RootStore.qml

IRootStore {
    id: root

    count: service.count

    property CounterService _service: CounterService { }

    increment: function () {
        return service.increment();
    }
    decrement: function() {
        return service.decrement();
    }
}
```

To create a mock store we can create one directly in the tests folder, called RootStoreMock.

It derives from the IRootStore and implements the API in a way which can be tested. This means the results are exposed. It is also possible to add new API to the mocked store. These properties and functions should be prefixed with an `_` to show the user this is not an official API of the root store.


```qml

    // stores/tests/RootStoreMock.qml
    import ".."

    IRootStore {
        id: root
        count: 0
        property int _previousCount: count

        increment: function () {
            _previousCount = count;
            count++;
            return count;
        }
        decrement: function() {
            _previousCount = count;
            --count;
            return count;
        }
    }
```

Now with the mocked root store we can run the tests.

```qml

// stores/tests/tst_welcomeview.qml
import QtTest 1.1
import ".."
import "../mocked"

TestCase {
    id: root
    property WelcomeView view;
    Component {
        id: component
        WelcomeView {
            store: RootStoreMock {}
        }
    }

    function init() {
        // this is run for every test function
        view = createTemporaryObject(component, root);
        // assert initial state
        compare(0, view.store.count);
    }

    // testing increment action
    function test_increment() {
        compare(0, view.store._previousCount);
        var item = findChield(view, "increment");
        mouseClick(item);
        compare(0, view.store._previousCount);
        compare(1, view.store.count);
        mouseClick(item);
        compare(1, view.store._previousCount);
        compare(2, view.store.count);
    }

    // testing decrement action
    function test_decrement() {
        var item = findChield(view, "decrement");
        mouseClick(item);
        compare(0, view.store._previousCount);
        compare(-1, view.store.count);
    }
}
```

This should give the reader an idea how to test an view component which depends on a store with many external dependencies.

### Store Testing

A store depends on the services and as such it depends on the chosen service architecture and their limitations. Ideally a store could be tested using a service simulation back-end which will run inside the test process and which is fully controllable.

A normal service implementation would use some kind of IPC and requires a second process to be started. As this way of testing is error prone (start two processes, await both are established, initiate connection, wait until connection ready, ...) it would be better we could create a custom service implementation inside our test and would not have to modify the service client.

```qml

TestCase {
    id: root
    CounterService {
        id: service
        register: true
        increment: function() {
            count++;
        }
        decrement: function() {
            count--;
        }
    }

    property IRootStore store;
    Component {
        id: component
        RootStore {
        }
    }

    function init() {
        // this is run for every test function
        store = createTemporaryObject(component, root);
        // assert initial state
        compare(0, store.count);
    }

    void test_increment() {
        store.increment();
        tryCompare(store.count, service.count);
    }


    void test_decrement() {
        store.decrement();
        tryCompare(store.count, service.count);
    }
}
```

!!! note

	Discuss a way when the service can not be embedded into the test case, e.g. sequential testing ...

In case the service can not be integrated into the QML test case it is often desirable to let the test case start the service server and reset the particular server. Additional the test should run in sequence. For this we would need to write a small plugin which controls the server (start/stop) ans waits notifies the test case when the server is fully loaded. Also the server control should expose a reset operation to reset the data on the server. Resetting is often faster then shutdown/startup sequence. Finally the test functions should be arranged in sequence. For this we need to ensure the tests are named in a way to they are ordered by name.

```qml

TestCase {
    when: control.ready
    ServerControl {
        id: control
        services: "counter"
    }
    ServerSniffer {
        id: sniffer
        server: control.server
    }
    CounterClient {
        id: client
    }

    function test_001_increment() {
        sniffer.reset();
        client.increment();
        tryCompare(sniffer.received, "increment")
    }

    function test_002_decrement() {
        sniffer.reset();
        client.decrement();
        tryCompare(sniffer.received, "decrement")
    }
}
```

### Service Testing

Testing a service is often divided into testing the client, the transport and the service implementation. As the service implementation is not under the control of the UI layer it is out of scope here. A client can be tested if the simulation back-end uses the same client component and the same transport. A transport should always be tested in isolation as this is often an external library.

If the simulation back-end uses a different client and only shares the client API then there is a need to ensure the client is also tested. Often this is not done due to a client is often semi-generated and there is no need to test generated code.


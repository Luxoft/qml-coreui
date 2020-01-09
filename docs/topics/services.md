# Services

>   "The code is the truth,
>   but not the whole truth"
>
> -- Grady Booch

!!!info

    This material is work in progress and will change!


Services exposes features either from the system or a networked resource to the application layer. Services can be categorized based on their process-association, inter-service dependencies and the handling of state. In general a service is an instance of vertical communication. This vertical communication can be done via an IPC out-of-process or via a library in-process. The API can be designed state-less or state-full. You should prefer state-full if the API shall reflect the system state (e.g. volume, temperature) which shall be shown on several displays and state-less if the API is used to primary query backends and no shared state is required. In general in embedded system a state-full service is preferred as the system shall reflect the machine state.

> A service is a vertical communication layer
> APIs in embedded devices are primary state-full

Be aware that the service API will not directly consumed by the UI elements and rather be wrapped by a store API optimized for UI consumption.

> A service API will not be directly consumed by the UI


Services are system features which expose an API surface published using primary a system specific IPC. A service is often defined as a client/server model, where the client (e.g. the UI or another service) and the server (a bundle of services in one process) communicate via an IPC (typically TCP/IP based or D-BUS based).

During development a service needs to be simulated in case the endpoint is not available or depends on a hardware which is difficult to gain access to or work with. Often HW is also not available in an early project phase, still the UI development needs to start. When looking on a system there exists often many services, and ideally each service can be individually configured to use either a simulation or a real backend.

Simulation and services will often be used across device boundaries. For example a host running the user interface tries to connect to an embedded device connected via an ethernet or serial connection. In these cases it is important that the selected IPC supports this use case. This is why the author things D-BUS is not a valid choice for this layer and TCP/IP based solutions are better suited.

> A service needs to support a simulation backend

> A simulation backend needs to be enabled per service

For out-of-process services of the IPC is very specific to the individual project and the service needs to be able to adapt to this communication library. IN a rare case the project does not define an IPC solution and the developers can choose their best fiffting solution.

There is a difference between the services consumed by the UI and the services the system is offering. Often system services are available using D-BUS as IPC and are meant to be consumed using some low-level API. These middle-ware services offer a higher-level API already defined with the UI in mind, still, the API is only loosely coupled towards the UI.

It is assumed that this service API will change over the development time of the project and it will take several iterations to get a stable API. As such it is not wise that the UI directly consumes this API. The changes will lead to many small defects in the UI which will make it very hard to detect and fix them.

!!! hint

    It is preferred that the service client API either be consumed by a C++ native extension or in a QML/JS based UI store. The C++ compiler will detect many API changes and report them before they appear in the UI and when using a QML/JS based store there needs to be 100% test coverage to ensure that these changes will be detected.

It is important that the release cycle of the store API is fully controlled by the UI developer to avoid suprises and the release cycle of the service API is harmonized between the UI and platform developers.

# API Shape

The API should be shaped after easy to understand patterns and ideally be familiar to the developer but also easy to explain to non-technical API authors. The API should define a common vocabulary and provide a way to structure larger projects.

The API shall be shaped around the idea of a module. Each module is identified by a reverse URI (e.g. like a Java package convention). Each module can contain a list of interfaces. An interface is a collection of properties, operations and signals. The collection of properties define the state of the interface. The operations provide a mean to modify the state or to retrieve data. Signals allow a service to notify a client about external changes. It is assumed for pure property changes the API will auto-provide signals.


```yml

    - module                  # module is a namespace for all child symbols exists
        - Interface           # named symbol which defines a set of properties, operations, and signals
            - Properties      # data entry with a name and type
            - Operations      # operation with parameters and return value
            - Signals         # notification sent from the service back to the consumer
        - Struct              # data structure to define a message
            - Fields          # entries of a struct with name and type
        - Enum/Flag           # An enumeration which can be used e.g. for properties and/or operations
            - Values          # entries of an enumeration with name and value

```

A module can have one or more interfaces, structs or enums/flags. As such a module is a higher level feature. To adhere to the micro-service architecture a service API should not depend directly on another service, instead, the API author should use identifiers (IDs), which are typically integers or strings to identify a resource from another module.

Below is an example of a simple counter API. Please be aware this is a state-full example as the state of the interface is encoded in the count property.

```java

    module counter 1.0

    interface Counter {
      int count
      void increment()
      void decrement()
    }
```

A state-less example would look like this

```java

    module counter 1.0

    interface Counter {
      int count()
      int increment()
      int decrement()
    }
```

## Interface Definition

The API exposed by all middle-ware services needs to be harmonized across all services. To ensure a well defined and harmonized API can be created the API shall be defined in an interface definition language (IDL) with an attached code generation.

The IDL should be independent of the target technology to allow securing the investment into an API also if the UI technology or the backend technolgy changes in the future.

The IDL should be designed so that it is simple to understand and expressive. It should be able to express the API exact enough for developers to get an idea which code will be generated out of the API, still, it should be high level enough that a non-technical person understands which features are covered in the API.

The IDL needs to be able to generate a well-defined API documentation for externals to lookup the documentation as a reference how to use the API. Also, the IDL shall allow extensions to provide meta information to transport project specific information such as deployment information or specific directives for the code generator.

## Code Generation


The IDL should have a sophisticated code generator attached, ideally independent from the target technology, to allow customers to use a different technology or a different IPC.

During the lifetime of a project, there are many needs to generate a different kind of source code or reports about an API. For example also if the client/server communication is done in C++ using a TCP/IP based IPC  there might be a requirement during development to potentially use a WebSocket JSON protocol to make debugging easier. Also, developers would like to generate documentation with a custom style to map the project colors or in a format which can be consumed by their tool-chain. In the past, there was also some need to report back some statistics about the API.

All of these use cases call for a flexible yet powerful code generation framework where a development team can use existing code generator or provide their own if the requirements of the project change. Still, the investment into the API definition should not be lost and be reusable.


## Service Implementation

A service generated from the code generator should ideally already be compilable and runnable by the user also if it does not provide any implementation. This allows the user to implement features piece by piece iteratively. This normally results in a conflict if the code generator writes files which need to be edited by the user. It is important that the code generator differentiate between files which can be overwritten and those which need to be preserved for the user.

The service implementation is typically based on an abstract base class which provides the interface to be implemented. The developer then needs to edit the concrete classes and implement the interface.


## Client Usage

From the UI perspective the client should just be instantiated. The UI should be in charge to decide at which time a client is created and connected to the device. The client configuration should be read from some kind of data storage (e.g. settings file) and/or environment variable. By this configuration of the client is separated from the instantiation. The UI shall be in charge of the startup sequence. And as such must be able to delay certain clients only to be constructed on demand.


A service API shall not be exposed to the UI, this is merely to allow better testing. For this a store wrappes the used service APIs in a common API for the UI. The store can be written either in QML/JS or C++.  QML/JS is great during prototyping but C++ offers more performance and better control of the API usage.

```qml

// store/RootStore.qml

import services.phone 1.0

Store {
    id: root

    property alias callActive: phone.callActive

    PhoneService {
        id: phone
        active: true
    }

    function call(number) {
        if(!phone.enabled) {
            return;
        }
        phone.call(number, function(result) {
            if(result.error) {
                console.warning('ERROR: ', result.error);
            }
        });
    }
}
```

Calling service function is often more complex than just calling the operation. Certain conditions defeind by the requirements specification and or error cases needs to be handled. To avoid this code pollutes the UI these functions are coded inside a store. Often used functions can also be encoded into helpers to even more reduce code clutter.


## Service Simulation

Service simulation allows a client to be used without a real-service attached and furthermore allows the testing of service conditions which are difficult to establish. It is used in the UI creation when user stories need to be tested to ensure certain system conditions are established to effectively validate the user story. This does not replace the need for system testing as these kinds of prototypes are more designed to demo a user story to a product owner before it will be validated in the actual hardware.

Establishing flexible simulated services is the key factor to separate the UI software from the hardware. Simulation needs to be switched per service base so that the system can run in a mixed simulation mode. This requires a service not to depend on other services which leads to a micro-service architecture. In case a service depends on an object from another service it is better to exchange object ids and the other service would acquire the object using this object id.

A simulated service should be more than just a static representation of the service state, it should also be able to simulate the execution of operations and their effects. Ideally the simulation is able to simulate how data changes over time, e.g. a time or event based scripting. This could be a script attached to the simulated service or as simple as a timed data read from a file.

The configuration of the services is ideally located in one shared document and can be edited to switch between real-services and simulated services. Most of the times a service is bound through a TCP/IP protocol, the switch could then be as simple as changing the port or the IP address of a service.



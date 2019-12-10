# Exposing Data from C++ to QML

!!! info

     * [QtQml](https://doc.qt.io/qt-5/qtqml-index.html)
         * [Overview - QML and C++ Integration](https://doc.qt.io/qt-5/qtqml-cppintegration-overview.html)
         * [Integrating QML and C++](https://doc.qt.io/qt-5/qtqml-cppintegration-topic.html)
             * [Exposing Attributes of C++ Types to QML](https://doc.qt.io/qt-5/qtqml-cppintegration-exposecppattributes.html)
             * [Defining QML Types from C++](https://doc.qt.io/qt-5/qtqml-cppintegration-definetypes.html)
             * [Embedding C++ Objects into QML with Context Properties](https://doc.qt.io/qt-5/qtqml-cppintegration-contextproperties.html)
             * [Interacting with QML Objects from C++](https://doc.qt.io/qt-5/qtqml-cppintegration-interactqmlfromcpp.html)
             * [Data Type Conversion Between QML and C++](https://doc.qt.io/qt-5/qtqml-cppintegration-data.html)
         * [Writing QML Extensions with C++](https://doc.qt.io/qt-5/qtqml-tutorials-extending-qml-example.html)
         * [Creating C++ Plugins for QML](https://doc.qt.io/qt-5/qtqml-modules-cppplugins.html)
         * [Important C++ Classes Provided By The Qt QML Module](https://doc.qt.io/qt-5/qtqml-cppclasses-topic.html)
     * [QtQuick](https://doc.qt.io/qt-5/qtquick-index.html)
         * [Qt Quick C++ Classes](https://doc.qt.io/qt-5/qtquick-module.html)
         * [C++ Extension Points Provided By Qt Quick](https://doc.qt.io/qt-5/qtquick-cppextensionpoints.html)
     * [QtQuick.Controls 2](https://doc.qt.io/qt-5/qtquickcontrols-index.html)
        * [Qt Quick Controls C++ Classes](https://doc.qt.io/qt-5/qtquickcontrols2-module.html)

!! note::

    * https://www.vikingsoftware.com/qtquick-custom-item-performance/
    * https://github.com/QUItCoding/qnanopainter


This docoument will discuss different strategies how to expose data to QML. We will shortly discuss the pros and cons of each strategy and later define a strategy which shall scale.

## Exposing Data

Qt offers you several ways to inject data into the user interface presented by QML. QML comes with support native support for JSON using the JS `JSON.parse` and `JSON.stringify` methods. As a transport you can use HTTP via the XMLHTTRequest for websockets using the WebSocket library. Here is a list of references:

* https://doc.qt.io/qt-5/qtqml-xmlhttprequest-example.html
* https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON

The other option is to capture the data on the native C++ side expose it to QML using `qmlRegisterType` and properties, slots and signals. For this Qt C++ data types need to be transformed to QML supported data types. The process of registering C++ data types and the conversion are discussed in the Qt documentation at several places.

 * [QtQml](https://doc.qt.io/qt-5/qtqml-index.html)
     * [Overview - QML and C++ Integration](https://doc.qt.io/qt-5/qtqml-cppintegration-overview.html)
     * [Integrating QML and C++](https://doc.qt.io/qt-5/qtqml-cppintegration-topic.html)
         * [Exposing Attributes of C++ Types to QML](https://doc.qt.io/qt-5/qtqml-cppintegration-exposecppattributes.html)
         * [Defining QML Types from C++](https://doc.qt.io/qt-5/qtqml-cppintegration-definetypes.html)
         * [Embedding C++ Objects into QML with Context Properties](https://doc.qt.io/qt-5/qtqml-cppintegration-contextproperties.html)
         * [Interacting with QML Objects from C++](https://doc.qt.io/qt-5/qtqml-cppintegration-interactqmlfromcpp.html)
         * [Data Type Conversion Between QML and C++](https://doc.qt.io/qt-5/qtqml-cppintegration-data.html)
     * [Writing QML Extensions with C++](https://doc.qt.io/qt-5/qtqml-tutorials-extending-qml-example.html)
     * [Creating C++ Plugins for QML](https://doc.qt.io/qt-5/qtqml-modules-cppplugins.html)
     * [Important C++ Classes Provided By The Qt QML Module](https://doc.qt.io/qt-5/qtqml-cppclasses-topic.html)
 * [QtQuick](https://doc.qt.io/qt-5/qtquick-index.html)
     * [Qt Quick C++ Classes](https://doc.qt.io/qt-5/qtquick-module.html)
     * [C++ Extension Points Provided By Qt Quick](https://doc.qt.io/qt-5/qtquick-cppextensionpoints.html)
 * [QtQuick.Controls 2](https://doc.qt.io/qt-5/qtquickcontrols-index.html)
    * [Qt Quick Controls C++ Classes](https://doc.qt.io/qt-5/qtquickcontrols2-module.html)

## JSON or C++

JSON is a great format when you interact with HTTP REST endpoints or other cloud based services which are JSON based. Unfortunately on the Qt C++ side there is not a great support to consume such JSON based services. You would need to rely on QNetworkAccessManager and QJSonDocument to consume such kind of services. There are 3rd party libraries which makes it easier to consume a HTTP REST endpoint for example Duperagent (https://github.com/Cutehacks/duperagent).

In QML you would have to use the XmlHttpRequest and convert the incoming data into JSON. This is pretty lowlevel when coming from the Webworld and are used to libraries like Axios.

From the C++ side you would use the `QNetworkAccessManager` and request a HTTP endpoiunt and convert the data into JSON using `QJsonDocument`. From there you normally convert it further to a `QVariant` related type to expose it to QML or using native data types.

If your data come from another native source using a binary protocol you often have to write an adapter layer to convert the data types from standard C++ to Qt C++ and then you can directly expose this data to QML using Qt offered data conversions.

## Mechanics of Exposure

So you have the data now either as some form of `QVariant` or as Qt C++ native types. Now you can expose the data to QML. But how to structure this?


We can see data often as a structured tree which starts either with an object form or an array form. JSON demonstrated very nicely that all data can be reduced to simple data structures. Same applied to Qt data. But data is not everything we want to expose, we also want to expose operation on the data as also signals, so notification when something has changed. Additional Qt uses reactive programming, so a user gets notified when a property has changed and based on this we are used nowadays to bindings. It is only possible to bind to properties, not to operations or signals. On signals you can connect using a handler, which is just another form of callback. Operations might trigger property changes or setting a property will trigger property changes.

Besides these structures there is also the model type in Qt. Which is a protocol to expose data arrays efficient to a view.


## Example

To demonstrate the capabilities and possible issues we will develop a small configuration loader for a tomato timer with an attached task list. The idea is you work on a task for x minutes, make a break and then continue to work on anther task. After some work unites you make a longer break.

The configuration is stroed in a JSON document and looks like this:

```json
{
    "color": "#FF0000",
    "tasks": [
        { "text": "task-1", "done": false },
        { "text": "task-2", "done": false },
        { "text": "task-3", "done": true }
    ],
    "timing": {
        "work": 25,
        "short-break": 5,
        "long-break": 15
    }
}
```

In the UI we would like to display the configuration and modify it. For example we would like to:

* change the color to another random color
* add new tasks to the taks list
* clear out all done tasks
* mark task to be done
* update a task text
* change the individual timing settings

As we need to use this information in different places we would like to get informed when any of these data fields change.

## Use Case: Loading data from JSON

The data could come from a network service using HTTP or we could read it from a NOSQL DB, or simple from a JSON file. Using a JSON file is the simplest way.

We would read the text document and use QJSonDocument to convert it into a QJsonObject and form there into a QVariantMap. From there on we have two options, either expose the whole document as a great QVariantMap or expose individual properties as a QVariant related type.

Exposing the whole document:

```cpp
class TodoManager : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QVariantMap document READ document WRITE setDocument NOTIFY documentChanged)
    ...
}
```


Or exposing the individual properties

```cpp
class TodoManager : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QColor color READ color WRITE setColor NOTIFY colorChanged)
    Q_PROPERTY(QVariantList tasks READ tasks WRITE setTasks NOTIFY tasksChanged)
    Q_PROPERTY(QVariantMap timing READ timing WRITE setTiming NOTIFY timingChanged)
```

Now we can get and set the data. Almost done.

## C++ Data Sources

If we would have C++ native data structures we would first write an adapter, before we can expose the data to Qt C++. The adapter could look like this.

```cpp
struct Task {
    QString text
    bool done
}

struct Timing {
    int work;
    int shortBreak;
    int longBreak;
}

class TodoEngine : public QObject {
    Q_OBJECT
public:
    TodoEngine(QObject *parent=nullptr);
    QColor color();
    void setColor(QColor color);
    QList<Task> tasks();
    void appendTask(Task task);
    void clearTasks();
    Timing timing();
    void setTimming(Timing t);

signals:
    void dataChanged();
private:
};
```

This engine is using an C++ internal todo implementation which is need to be adapted to be easy consumable for Qt. This engine API is not directly exposable to QML, we need to wrap it another time to ensure we provide a great experience.

```cpp
class TimingGroupedProperty : public QObject {
    Q_OBJECT
    Q_PROPERTY(int work READ work WRITE setWork NOTIFY workChanged)
    Q_PROPERTY(int shortBreak READ shortBreak WRITE setShortBreak NOTIFY workChanged)
    Q_PROPERTY(int longBreak READ longBreak WRITE setLongBreak NOTIFY longBreakChanged)
    ...
}
class TodoManager : public QObject {
    Q_OBJECT
    Q_PROPERTY(QColor color READ color WRITE setColor notify colorChanged)
    Q_PROPERTY(QVariantList task READ tasks WRITE setTasks notify tasksChanged)
    Q_PROPERTY(TimingGroupedProperty* timing READ timing CONSTANT)
    ...
}
```

To make the list even better consumable we could introduce a model.

```cpp

class TaskModel : public QAbstractItemListModel {
    ...
};

class TodoManager : public QObject {
    Q_OBJECT
    Q_PROPERTY(QColor color READ color WRITE setColor notify colorChanged)
    Q_PROPERTY(TaskModel* tasks READ tasks CONSTANT)
    Q_PROPERTY(TimingGroupedProperty* timing READ timing CONSTANT)
    ...
}
```

The model could be editable by implementing `setData` and we would be able to assign values from inside QML.

Now we should assume the API is perfect and can be used by the QML frontend developers.

## Using an API

We should now remember aboout our use cases and see how a frontend developer would use our API.

* change the color to another random color
* add new tasks from the taks list
* clear out all done tasks
* mark task to be done
* update a task text
* change the individual timing settings


So lets see how the fontend develper would use the API. For this we can assume a simple UI where the TodoManager is instantiated and we implement a bugtton on clicked handler.


```qml

Pane {
    TodoManager {
        id: manager
    }
    Button {
        text: 'Action'
        onClicked: doIt()
    }

    function doIt() {
        // here comes our code
    }
}
```

> change the color to another random color

```qml
function doIt() {
    manager.color = Qt.rgba(Math.random(), Math.random(), Math.random(), 1);
}
```

> add new tasks to the task list

This is currently not supported, we would have to extend the model for an append function. But which parameters would the append function take?

If this would be a gadget, we can not create a gadget on the QML side, another option would be to pass in a `QVariantMap`.

```qml
function doIt() {
    // using a QVariantMap
    manager.tasks.append({text: "Another Task", done: false})
    // individual parameters
    manager.tasks.append("Another Task", false)
}
```

> clear out all done tasks

Also our current model does not support it yet, we have to add a clear function.

```qml
function doIt() {
    // using a QVariantMap
    manager.tasks.clear()
}
```


> mark an individual task to be done

If we would be in a ListView we would have access to an individual model entry

```qml
delegate: ItemDelegate {
    onClicked: {
        model.done = true;
    }
}
```

If not, then we would need to implement an set function, which will take a field map and an index.


```qml
function doIt() {
    manager.tasks.set(index, { done: true});
}
```

> update a task text

We can again use our set method

```qml
function doIt() {
    manager.tasks.set(index, { text: "hello" });
}
```


or inside our list view the model assignment


```qml
delegate: Item {
    model.text = "hello";
}
```

> change the individual timing settings

To change the data we can use the grouped properties to access them.


```qml
function doIt() {
    manager.timing.work = 15; // set to 15mins
}
```


## Streamling the API

This API requires currently quit some thinking to ensure all data is exposed to the users in the correct way and easy accessible to the frontend.

To streamline the API we could make the data read only and expose operations to support the different use case.

```cpp
class TodoManager : public QObject {
    Q_OBJECT
    Q_PROPERTY(QVariant color READ color notify colorChanged)
    Q_PROPERTY(QVariantModel* tasks READ tasks CONSTANT)
    Q_PROPERTY(QVariantMap* timing READ timing notify timingChanged)
    ...
public slots:
    // set random color
    void setRandomColor();
    // add task to task list
    void addTask(const QVariantMap &task);
    // clear all done tasks
    void clearDoneTasks();
    // update text or done on task
    void updateTask(int index, const QVariantMap &fields);
    // mark task done
    void markTaskDone(int index);
    // update a timing value
    void updateTiming(QVariantMap fields);
}
```

This API now very generic. Maybe a little bit too generic.


```cpp


class Task {
    Q_GADGET
    ...
};


class Timing {
    Q_GADGET
    ...
};

class TodoManager : public QObject {
    Q_OBJECT
    Q_PROPERTY(QColor color READ color NOTIFY colorChanged)
    Q_PROPERTY(TaskModel* tasks READ tasks CONSTANT)
    Q_PROPERTY(Timing timing READ timing NOTIFY timingChanged)
    ...
public slots:
    // set random color
    void setRandomColor();
    // add task to task list
    void addTask(const QVariantMap &task);
    // clear all done tasks
    void clearDoneTasks();
    // update text or done on task
    void updateTask(int index, const QVariantMap &fields);
    // mark task done
    void markTaskDone(int index);
    // update a timing value
    void updateTiming(QVariantMap fields);
}
```

The difference now is that the structures are concrete types, same as primitive types. When mmutating the value, we can not use concrete types as there is no real way to create them from QML side. You coudl create a factory but the approach is much more complicated.


```qml
function doIt() {
    var task = manager.createTask()
    task.done = true;
    manager.updateTask(1, task);
}
```

versus the JS way

```qml
function doIt() {
    manager.updateTask(1, { done: true});
}
```

The second one is much more accessible for a JavaScript developer. Also if this means a JS developer could add fields, which do not exist in the structure.

## Defining Structure

We define structure be defining rules for APIs.

Separate state from actions from queries.
The state is formed by all properties of an API. Actions are the methods which mutate the state, either directly or indirectly through a remote effect. And a query is a method which returns data.


API State

* Expose primitive types using read only properties
* Expose uncountable lists using read only models of either primitive types or structures presented by gadgets
* Expose countable lists using a QVector or QVariant

API Mutations or Queries

* Expose mutations using invokable methods
* Pass in structured data through QVariantMap
* Pass in primitives using QML base types


# Attic



* JSON or QtTypes?
* global types, types in main.cpp, type in plugins,
* types a properties, objects, QVariant, Model

What is wrong?

Using FLux Approach: Data travels up, operations travel down.

Strategy which scale!

Separation of rendering items and data items

There are different categories and ways to expose C++ data to QML.

Here is a list of data aspects we need to consider

* data type - is concerned if the data is one of
* data dynamics
* data structure
* data ownership
* data usage
* data source


## Data Exposure

There are different ways to inject data into the QML scope.

* JSON over HTTP/WebSocket
* C++ Types/Objects/Models


## JSON Data Sources

To use JSON over HTTP for example to connect to a HTTP REST API you can use the XmlHttpRequest or a 3rd party request library like DuperAgent. For authentication you often need to store a token, this can be accomplished using the QML LocalStorage. The responses need to then assigned to properties or stored into a model. For a good model support it would be good to program a simple VariantModel which exposes the data as QVariants to the caller. This approach is great for prototyping.  Ideally you ensure this data retrieval logic is wrapped inside a store, to ensure later you can switch the data retrieval technology for production if required.

A WebSocket connection can be established using the WebSocket client form QML and the messages retrieved can be parsed directly to JSON messages. As websockets do not offer a request/response protocol like REST you would need to chose one, for example JSO RPC or WAMP (https://wamp-proto.org). The data incoming need to be handled like the data received form the HTTP request.

While JSON sources are a natural way inside QML as QML supports JS natively, the C++ provisioning is the dominant path for exposing data to QML. The on-board tooling from QML to support JSON data sources are really weak, and require own development, unfortunately.

## C++ Data Sources

C++ sources are the default supported data sources in Qt/QML. They come in from various places and types.

## C++ Type Provisioning

A C++ type can be provisioned as part of the runtime, e.g. inside the `main.cpp` using one of the `qmlRegisterType` formats or it can come in on demand using a QtQuick plugin using a dynamic loaded library which includes a type registry.

You can register either data types, which provide pure data or objects which provide data and operations. Data types are mostly value types and copied over to QML from C++. Objects are reference types and the ownership needs to be clear.

!!! note

    It is best with objects to follow a strict philosophy that they need to be created from QML with QML ownership. Otherwise you really need to know what you are doing. Also if this is not the fanciest of all ways, it is a simple and proven path.


## Data Type

The data type aspect is concerned about if the data is one of the primitive data types directly supported by QML (sse https://doc.qt.io/qt-5/qtqml-cppintegration-data.html) or it is a more special type, e,g, a structure, list or map of a type. If the data you want to expose to QML is in this list: https://doc.qt.io/qt-5/qtqml-cppintegration-data.html#basic-qt-data-types. Then things are simple.

If the data type is a QObject, structure, map or list than things are not complicated but different.

## Data Cardinality

The cardinality decides if the type is there once or often, for example a list of integers or a list of object. Additional with the cardinality comes also the question of dynamics. How often iti expected the data list or individual data entries will change?

If the types do not change often, then you can just expose them a QVariantList or QVariantMap or if it in the table here (https://doc.qt.io/qt-5/qtqml-cppintegration-data.html#sequence-type-to-javascript-array), then you also can just expose the type using a property.

If the type is more structured and changes more often, then probably an item model would be better. Also if there are many data entries, where it is not feasible to copy them all over to QML a item model is the better choice or using a kind of pagination approach.

## Data Structure

Data structure tries to look into how the data is structure, it is  for example an object with fixed set of properties, than a grouped property can be used. If the structure it more dynamic than maybe a variant map or item model can be use or even a QQmlPropertyMap.

## Data Ownership

Ownership can be in general inside Qt C++ or QML/JS. In the C++ case the object will be deleted when the parent is deleted in the QML/JS case the garbage collector takes care of this. Ideally a object is owned by the side it creates. So an entry created inside QML, should also use the QML infrastructure for object lifetime. An object created on C++ should use the C++ way of deleting objects. It is just improtant for objects owned by C++, QML shoudl not keep a handle to these objects (so never store them), they could be destroyed the next time you try to access them. (see https://doc.qt.io/qt-5/qqmlengine.html#ObjectOwnership-enum) for more information.

## Data Usage

Data usage looks at the intent how to use the data inside QML. It the intent is to use any of the View classes the data should ideally be available a  ModelView type. This is the preferred way for developer.

## Data Source

If the data source comes from a weakly typed source for example a REST API or a JSON configuration document, you might pass the data directly as a QVariantMap or QVariantList to QML. This is easier than trying to convert the data into C++ structures and then converting it back to QVariant type to expose it to QML




Qt5 offers several ways to expose C++ data types to QML. It is possible to epose a basic type, a complex value type or a complex object type. A basic type in general are integers, boolean or strings, see (basic types for an overview). Complex value types are typical structs or classes where the content is copied into the QML space. Changing these types will not be reflected back to the C++ space. The complex object types are passed by reference, these are typical QObject derived types and passed as pointers.


Typical types:

* basic value types: int, bool, float, QString,
* complex value types: struct, classes, QVariantList, QVariantMap, QList
* complex object types: QObject, QAbstractItemListModel


To demonstrate the capabilities and possible issues we will develop a small configuration loader for a tomato timer with attached task list. The idea is you work on a task for x minutes, make a break and then continue to work on anther task. After some work unites you make a longer break.

The configuration is stroed in a JSON dicuemnt and looks like this:

```json
{
    "color": "#FF0000",
    "tasks": [
        { "text": "task-1", "done": false }
        { "text": "task-2", "done": false }
        { "text": "task-3", "done": true }
    ],
    "timing": {
        "work": 25,
        "short-break": 5,
        "long-break": 15
    }
}
```

In the UI we would like to display the configuration and modify it. For example we would like to:

* change the color to another random color
* add new tasks from the taks list
* clear out all done tasks
* mark task to be done
* update a task text
* change the individual timing settings

As we need to use this information in different places we would like to get informed when any of these data fields change.

## Loading JSON

We will create several APIs expose to the UI over this discussion. To make our life easier we create a dedicated JSFileIO class to read and write the data to a JSON file.

The API is fairly simple a read and write JSON method which uses a QVariantMap as data container and a path method to give us a file path inside a writeable home folder location.


```cpp
#pragma once

#include <QtCore>

class JsonIO : public QObject
{
    Q_OBJECT
private:
    explicit JsonIO(QObject *parent = nullptr);
public:
    static QString path(const QString &name);
    static QVariantMap readJSON(const QString &path);
    static void writeJSON(const QString &path, const QVariantMap &map);
};
```

In the implementation we use QStandardPath to lcoate the home folde. To read/write JSON we use the QJsonDocument to convert from/to a QVariantMap and use QFile to read/write fron/to file.

```cpp
#include "jsonio.h"

JsonIO::JsonIO(QObject *parent)
    : QObject(parent)
{

}

QString JsonIO::path(const QString &name)
{
    QString location = QStandardPaths::writableLocation(QStandardPaths::HomeLocation);
    return QDir(location).absoluteFilePath(name);
}

QVariantMap JsonIO::readJSON(const QString &path)
{
    QFile file(path);
    if(!file.open(QIODevice::ReadOnly)) {
        qWarning() << "unable to open configuration file. stop loading configuration";
        return QVariantMap();
    }
    const QByteArray& content = file.readAll();
    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(content, &error);
    if(error.error != QJsonParseError::NoError) {
        qWarning() << error.errorString();
        qWarning() << "unable to parse configuration file. stop loading configuration";
        return QVariantMap();
    }
    if(!doc.isObject()) {
        qWarning() << "toot element in configuration file must be object. stop loading configuration";
        return QVariantMap();
    }
    QJsonObject obj = doc.object();
    return obj.toVariantMap();
}

void JsonIO::writeJSON(const QString &path, const QVariantMap &map)
{
    QFile file(path);
    if(!file.open(QIODevice::WriteOnly)) {
        qWarning() << "unable to open configuration file. stop writing configuration";
        return;
    }
    const QJsonObject& obj = QJsonObject::fromVariantMap(map);
    const QByteArray& content = QJsonDocument(obj).toJson();
    file.write(content);
}
```

Having this now out of the way lets look at the most simplest API for our Configuration.

## Simplest Configuration API

The simplest configuration does expose the QVariantMap as data property to the QML user interface.

To now change the color for example you need to type

```qml
onToggleColor: {
    var data = config.data;
    data.color = Qt.rgba(Math.random(), Math.random(), Math.random(), 1);
    config.data = data;
}
```

So we copy the data out of the C++ object, modify it and then set it back. Trying todo thos without passing it back to c++ will not work.

```qml
onToggleColor: {
    var data = config.data;
    data.color = Qt.rgba(Math.random(), Math.random(), Math.random(), 1);
    // !!!WILL NOT WORK!!!
    config.dataChanged(data) // notify about change
}
```

The binding will be triggered but the data inside the config object is still the same. So we need to pass it back to cal the setData method, store the data inside the class and trigger the dataChanged signal.

When triggering the data changed signal all depending UI will be triggered (e.g. tasks list view and timings object view).

So maybe better to have individual properties for color, tasks and timings.

Besides this obvious flaw there are other flows. The use of QColor creates a QtGui dependency to our Configuration and using a variant list for tasks requires us to use modelData.text in the ListView, ideally we would write model.text, but for this we need to use a item model.

## Exposing Properties

On the next level we can expose the properties of our data structure to make it easier to modify them.

```cpp
#pragma once

#include <QtCore>
#include <QtGui>

class Configuration : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QColor color READ color WRITE setColor NOTIFY colorChanged)
    Q_PROPERTY(QVariantList tasks READ tasks WRITE setTasks NOTIFY tasksChanged)
    Q_PROPERTY(QVariantMap timing READ timing WRITE setTiming NOTIFY timingChanged)
public:
    explicit Configuration(QObject *parent = nullptr);

    ...
};
```

Now we can access the properties directly from the configuration object and do not need to extract it from the data object.


To now change the color for example you can type now

```qml
onToggleColor: {
    config.color = Qt.rgba(Math.random(), Math.random(), Math.random(), 1);
}
```

Modifying the color is now much easier. We can directly set it using the property setter. Through using the QColor datatype we got now a new dependency to QtGui. This might be something we want to remove later.

Let us see how we can mutate a list or map.

```qml
onAddTask: {
    var tasks = config.tasks
    tasks.push({text: text, done: false})
    config.tasks = tasks
}
```

It is ot possible to directly mutate the list, we still first need to copy it over to QML and then we can use the JS array push method to add a new task to the list and store it back to the C++ configuration object. Setting it on the C++ object will also take care about notifying a consumer of the data that this has changed. As we are using independent properties only object bound to the `task` property will be notified.

Similar concept will also apply to the map.

```
onWorkValueModified: {
    var timing = config.timing;
    timing.work = value
    config.timing = timing
}
```

This seems to be okay still, but the next one is a little bit weird.

```qml
onShortBreakValueModified: {
    var timing = config.timing;
    timing['short-break'] = value
    config.timing = timing
}
```

We had to use the map accessor as the JSON data is stored a `short-break`. This is a valid key in a QVariantMap, but not as a qml property name.

This can happen if you directly expose JSON data to QML. You need to amke sure that the keys are valid QML property names.

So lets modify our JSON data and later wrap the JSON entries in a proper C++ structure.

```json
{
    "timing": {
        "longBreak": 15,
        "shortBreak": 5,
        "work": 30
    }
}
```

Now we can use

```qml
onShortBreakValueModified: {
    var timing = config.timing;
    timing.shortBreak = value
    config.timing = timing
}
```

But changing the data source is not always available. Often data comes in a fixed form from another source and we can not change the format, we can only convert it.


## Removing QtGui dependency


We introduced a QtGui dependency on our Configuration object by using the QColor data type. This is a not so nice dependency as it is not really about GUI. In general sticking to data types which are more common, e.g. like JSON comparable types, makes the use and storage much easier.

We can convert luckily the QColor to a simple QString and Qt will auto-convert it to a property of type `color`..

So we change
```cpp
Q_PROPERTY(QColor color READ color WRITE setColor NOTIFY colorChanged)
```

to this


```cpp
Q_PROPERTY(QString color READ color WRITE setColor NOTIFY colorChanged)
```

And change also the getter and setter methods as also the storage type. The color itself is stored as a string anyway in the JSON configuration. Now we can remove the QtGui module form our include list.

We initially had to make a special conversion for the QColor datatype from a variant

```cpp
m_color = data.value("color").value<QColor>();
```

This is also not necessary anymore, we can simply use

```cpp
m_color = data.value("color").toString();
```

The API we have produced now it is still not very intuitive, we have to get a data list/map, modify it and set it back. Also for the list view a JS array is not a good data type. Not so much because of performance for those small array more out of predictability. There are some hacks to make the ListView conform to a item model and JS array, but these are hacks. Personally there should be one way of doing things.

Son one step in the right direction, but not ideal yet.

## C++ Structures

Now we want to make a more rigid attempt to data types. Currently we support JS objects as task entries, this allows us also to write things like this:


```qml
onAddTask: {
    var tasks = config.tasks
    tasks.push({hello: text, world: false})
    config.tasks = tasks
}
```

It just produces a new entry in the QVariantList it is not really secure.




## Using an item model

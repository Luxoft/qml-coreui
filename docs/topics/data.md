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

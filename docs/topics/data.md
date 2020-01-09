# Exposing Data to QML

> A clever person solves a problem.
> A wise person avoids it.
>
> -- Einstein

!!! info

    This chapter will show you how to expose the different ways of exposing data to the user interface layer and tries to develop
    a strategy to streamline the data exposure. We will shortly discuss the pros and cons of each strategy and later define a strategy which can scale.


## Exposing Data

Qt offers you several ways to inject data into the user interface presented by QML. QML comes with native support for JSON data using the JavaScript `JSON.parse` and `JSON.stringify` methods. As a transport you can use HTTP via the XMLHTTRequest or for web-sockets using the WebSocket library. Here is a list of references:

* https://doc.qt.io/qt-5/qtqml-xmlhttprequest-example.html
* https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON
* https://doc.qt.io/qt-5/qml-qtwebsockets-websocket.html

The other option is to capture the data on the native C++ side expose it to QML using `qmlRegisterType` and properties, slots and signals. For this the Qt C++ data types need to be transformed to QML supported data types. The process of registering C++ data types and the conversion are discussed in the Qt documentation at several places.

Here is a longer list of relevant sections.

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

JSON is a great data format when you interact with HTTP REST endpoints or other cloud based services which are JSON based. When using Qt C++ you would need to rely on `QNetworkAccessManager` and `QJSonDocument` to consume such kind of services. There are 3rd party libraries which makes it easier to consume a HTTP REST endpoint on the QML side for example duperagent (https://github.com/Cutehacks/duperagent).

When trying to expose JSON directly to the QML side using QtC++ it might be better to just expose the `QByteArray` to QML and let JavaScript to convert it to a JSON data type using `JSON.parse`. In pure QML you would have to use the XmlHttpRequest and convert the incoming data into JSON. This is pretty low level when coming from the web development and are used to other libraries like axios.


From the C++ side you would use the `QNetworkAccessManager` and request a HTTP endpoint and convert the data into JSON using `QJsonDocument`. From there you normally convert it further to a QML supported types or other data structures to expose it to QML or using C++ native data types.

If your data comes from another native source using a binary protocol you often have to write an adapter layer to convert the data types from standard C++ to Qt C++ and then you can directly expose this data to QML using Qt offered data conversions.

## Mechanics of Exposure

When you have the data as Qt C++ native types, you want to expose it to QML. But how best to approach this?


We can see data as a structured tree which starts either with an object or an array. JSON demonstrated very nicely that all data can be reduced to simple data structures or primitive type and object or arrays. Same can be applied to Qt data. But data is not everything we want to expose, we also want to expose behavior in the form of operations on the data as also signals as notifications about changes. Additional Qt provides reactive programming, where an API consumer gets notified when a property has changed and which leads to data binding. It is only possible to bind to properties, not to operations or signals. On signals you can connect using a handler, which is just another form of callback. Operations might trigger property changes through the procedure or writing to a property will also trigger a property change.

Besides these structures there is also the item model type in Qt. Which is a protocol to expose data arrays efficient to a view which expects a model.


## Demo for Discussions

To demonstrate the capabilities and possible issues we will develop a small configuration loader for a task list with a timer attached. The idea is you work on a task for x minutes, make a break and then continue to work on anther task. After some work unites you make a longer break.

The configuration is stored in a JSON document and looks like this:

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
* add new tasks to the task list
* clear out all done tasks
* mark task to be done
* update a task text
* change the individual timing settings

As we need to use this information in different places we would like to get informed when any of these data fields change.

## Task Manager API

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

This engine is using an C++ internal task implementation which is need to be adapted to be easy consumable for Qt. This engine API is not directly exposed to QML, we need to wrap it another time to ensure we provide a great experience.

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

We should now remember about our use cases and see how a frontend developer would use our API.

* change the color to another random color
* add new tasks from the task list
* clear out all done tasks
* mark task to be done
* update a task text
* change the individual timing settings


So lets see how the frontend developer would use the API. For this we can assume a simple UI where the TodoManager is instantiated and we implement a button on clicked handler.


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
    manager.timing.work = 15; // set to 15 mins
}
```


## Streamlining the API

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

The difference now is that the structures are concrete types, same as primitive types. When mutating the value, we can not use concrete types as there is no real way to create them from QML side. You could create a factory but the approach is much more complicated.


```qml
function doIt() {
    var task = manager.createTask()
    task.done = true;
    manager.updateTask(1, task);
}
```

versus the JavaScript way

```qml
function doIt() {
    manager.updateTask(1, { done: true});
}
```

The second one is much more accessible for a JavaScript developer. Also if this means a JS developer could add fields which do not exist in the structure.

Often backend developers are sidetracked by the different options Qt offers you to expose data to C++. The risk is high to get lost in the details and try to come up with a highly flexible data access patterns. When doing so developers loose sight on how a front-end developer would have to use then the API inside QML. It is important to make an API as accessible and narrow as possible for the API user by not focusing on access patterns and more on API use cases. By this the API will hide the business logic from QML inside C++ and only expose an API to QML which most of the time can be used in a single line of code and is often self explanatory.

## Structure and Rules

To make API creation more scalable we need to define a clear structure and rules, which we can pass on to developers.

We want to separate state from mutations and queries. We define the state of an API as the sum of all properties. Actions are the methods which mutate the state, either directly or indirectly through a remote effect. And a query is a method which returns data. For reference see also:

* https://martinfowler.com/bliki/CQRS.html
* https://facebook.github.io/flux/
* https://graphql.org/learn/queries/

API State

* Expose primitive types using read only properties
* Expose uncountable lists using read only models of either primitive types or structures presented by gadgets
* Expose countable lists using a QVector or `QVariantList`
* Expose structured data through gadgets or `QVariantMap`

API Mutations or Queries

* Expose mutations using invokable methods
* Pass in structured data through `QVariantMap`
* Pass in primitives using QML base types

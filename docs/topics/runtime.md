# Runtime & Modules

The QML runtime used in the CoreUI architecture is Qt Application Manager. Which is designed to provide a multi-process architecture, where each application runs in an own process, started by its own runtime.

## Engine

A runtime is just a small C++ application starting the JS engine and QML engine and loading the initial qml document.

```cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine("main.qml");
    return app.exec();
}
```

The QML application engine in the background handles the quit signal, loads translations, handles windows correctly and setups a QML file selector.

!!! note

    If you look for more inspiration how to write a custom runtime check out `$QTSRC/qtdeclarative/tools/qmlscene`. This runtime provides also command line parsing, import path configuration, etc...

The Qt Application Manager is more complex as contains a lot more features, configuration capabilities and security mechanisms as also support for launching other runtimes in separate processes and watching over them.

## Plugin Extensions

A runtime is extended using QtQuick plugins. A plugin is a defined C++ interface to be implemented and the plugin library needs to placed in a defined folder structure with a small description file the `qmldir`. Qt Creator contains a wizard to create a plugin. The CoreUI admin also has a generator, which fits the plugin into the existing native project.

When build and installed, te runtime will load the plugin when the module import is the first time requested by a QML document. By this we can control the loading of plugins by ensuring the module is only loaded when required. The runtime lookups the QML import declaration in the import paths and when detected loads the corresponding plugin library. The plugin declares a set of QML types which are then registered into the module namespace and made available to the QML engine.

Like below code which provides the interface vor the plugin to register the QML types.

```cpp
// plugin.h
#pragma once

#include <QtQml>

class AlarmPlugin : public QQmlExtensionPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QQmlExtensionInterface_iid)

public:
    void registerTypes(const char *uri) override;
};
```

A type is registered using one of the `qmlRegister...` template methods. By this this object is now accessible under the import URL with the type name in QML.

```cpp
#include "plugin.h"
#include "teatimer.h"


void TeaTimerPlugin::registerTypes(const char *uri)
{
    Q_ASSERT(uri == QLatin1String("Tea"));
    qmlRegisterType<TeaTimer>(uri, 1, 0, "TeaTimer");
}
```

The object registered can be either a visual type inheriting from `QtQuickItem` or a business type , inheriting from `QObject`. If the type shall take part of the rendering than it must inherit from `QQuickItem`.
Our example is a tea timer, which allows the user to set a duration and the time triggers a signal when the timer is done.

The tea timer is a standard object with properties and signals. Additionally `Q_INVOKABLE` is used to make the method available to QML.

```cpp
#pragma once

#include <QtCore>

class TeaTimer : public QObject {
    Q_OBJECT
    QPROPERTY(int currentTime READ currentTime NOTIFY currentTimeChanged)
    Q_INVOKABLE void set(int min, int sec);
    Q_INVOKABLE void start();
    Q_INVOKABLE void stop();
    int currentTime() const;
    void setCurrentTime(int currentTime);
private:
    void handleTick();
signals:
    void currentTimeChanged();
    void ring();
private:
    QTimer *m_timer;
    int m_currentTime;
    int m_duration;
};
```

For the implementation the tea timer uses a QTimer which timeouts every 100msecs to forward the current time and when the duration is reached it rings.

```cpp
// teatimer.cpp
#include "teatimer.h"

TeaTimer::TeaTimer(QObject *parent)
    : QObject(parent)
    , m_timer(new QTimer(this))
    , m_currentTime(0)
{
    connect(m_timer, &QTimer::timeout, this, &TeaTimer::handleTick);
    m_timer->setInterval(100); // 100 msecs
}

void TeaTimer::set(int min, int sec)
{
    stop();
    m_duration =  (min*60 + sec) * 1000);
}

void TeaTimer::start()
{
    m_timer-start();
}
void TeaTimer::stop()
{
    m_timer-stop();
    setCurrentTime(0);
}

void TeaTimer::handleTick()
{
    setCurrentTime(currentTime() + m_timer->interval());
}

int TeaTimer::currentTime() const
{
    return m_currentTime;
}

void setCurrentTime(int currentTime)
{
    if (m_currentTime == currentTime) {
        return;
    }
    m_currentTime = msec;
    emit currentTimeChanged();

    if (m_currentTime >= m_duration) {
        stop();
        emit ring();
    }
}
```

We can now use the tea timer inside our QML code through importing the tea module and instantiating the TeaTimer object.

```qml
import Tea 1.0

MainWindow {
    id: root
    TeaTimer {
        duration: 2 * TeaTimer.Minutes
    }
}
```

## Object Patterns

### Instances vs Singletons

QML also allows to register singletons. They are instantiated when the first time the module is imported. The problem with them are they are never destroyed and also they can be used anywhere in your code. Sounds great on first hand, but these singletons are tricky as they introduce dependencies which makes it hard to test these QML components. Ideally you try to avoid singletons wherever you can and use the dependency injections (aka configurable dependencies) to pass on instances of logic object into QML.

This is a bad example of using a tea timer type, by registering the type as singleton and using it inside a panel. Now it is very difficult to test this component.

```qml hl_lines="4"
// TeaPanel
Panel {
    Label {
        text: TeaTimer.currentTime
    }
}
```

This is better, we have the incoming dependency under control.

```qml hl_lines="3 5"
// TeaPanel
Panel {
    property TeaTimer teaTimer
    Label {
        text: teaTimer.currentTime
    }
}
```

Even better, avoid the dependency on the type at all

```qml hl_lines="4 6"
// TeaPanel.qml
Panel {
    id: root
    property int currentTime
    Label {
        text: root.currentTime
    }
}
```

### Delayed Init

Also when using instances we need to ensure the instantiation goes fast as this directly relates to the UI startup. Which means the constructor must be slim. Any longer startup (e.g. pinging a server) should be done using a delayed init call.

```cpp hl_lines="4"
TeaTimer::TeaTimer(QObject *parent)
    : QObject(parent)
{
    QTimer::singleshot(this, &TeaTimer::init);
}

TeaTimer::init()
{
    // do long initialization
}
```

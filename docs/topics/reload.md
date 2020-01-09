# Live Reloading

 Reloading or live reloading is the process where a user interface is changed by the developer and instead of restarting the user interface process it is possible just to reload the content.

 This can go manually, e.g. by pressing a assigned key shortcut or automatically by detecting the change.

 Reloading is possible as QML as the underlying user interface description language is a scripting language and not a compiled language, such as C++.

 The mechanics of reloading are fundamentally very simple

 * detect change (manual / automatic)
 * clear component cache
 * reset current document onto qml engine

Let's assume a we detect the changes manually and bind a shortcut to the `F5` key.


TODO: Add header only reload class

```cpp
int main(int argc, char** argv)
{
    QGuiApplication app(argc, argv);
    a
    ... tbd
    shortcut = QShortcut(QKeySequence("F5"),
    return app.exec()
}
```

# Auto Reloading

To enable auto reloading the engine needs to detect the change in the underlying source code. For this we need to watch file system changes using `QFileSystemWatcher`.

!!! info

    The underlying OS imposes often restrictions about how many files can be watched, to not hit these restrictions to early we will not warch files but folder changes. This is possible as modern editors have atomic writes. Atomic writes ensures that at any time the write operation can be reverted. This is done by a series of create/rename/delete operations. Pure file writes are not detected by the OS as directory changes but the creation and deletion of files are and this is where we listen on.

To not flood the UI with reload messages by hundred of files creation, there is a deleay timer of e.g. 100ms before a reload is triggered.

To watcher needs a set of initial directories which it will traverse and each directory will be added to the list of directories to be watched. There should be an exclude filter to exclude directories from being watched. When a change is detected the watcher restarts the delay timer. And when the delayh time is triggered it simply emits a change signal. Onto this change signak we can then connect our reload action.


TODO: Add watcher class to trigger reload

 !!! note


# State preserving or state resetting

That is the question!


# Practical Implications

How best to apply reloading
Which impact has reloading on architecture
Advanced reloading use cases

# Pitfalls

There are several aspects which often can disable live reloading due to crashing or sheer complexity in the underlying QML engine.

During livereload a large amount of Qt objects are deleted and then newly created. Any referenced null  pointers will crash the engine when the UI tree is destructed. This is normally not a problem of the engine but a clear indication that there are places where Qt objects are passed back and force between C++ and QML without clear checks and ownership. As a general advice: Just do not pass dynamic objects back and forth between QML and C++ and do not be fancy when creating a QML/C++ API. Predictability on the API user perspective outweights any smartness. Boring is good!

Another reason that reloading might not work is when the code is too complex, interwined or based on a previuos state in the UI that reloading does takes seconds. Reloading always should be fluent which we define as below 1 seconds (reload <1s). Otherwise it is better to break up the UI and reload a partial UI. This requires the architecture and component design supports reloading of individual components.

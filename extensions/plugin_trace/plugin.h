#pragma once

#include <QtQml>

class Plugin : public QQmlExtensionPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QQmlExtensionInterface")

public:
    explicit Plugin(QObject* parent=nullptr);
    void initializeEngine(QQmlEngine *engine, const char *uri);
    void registerTypes(const char *uri);
private:
};
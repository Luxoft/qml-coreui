#include "plugin.h"


Plugin::Plugin(QObject *parent)
    : QQmlExtensionPlugin(parent)
{
}

void Plugin::initializeEngine(QQmlEngine *engine, const char *uri)
{
    Q_UNUSED(engine)
    Q_UNUSED(uri)
}

void Plugin::registerTypes(const char *uri)
{
     // @uri {{uri}}
     // qmlRegisterType<TYPE>(uri, 1, 0, "TYPE_NAME");
}

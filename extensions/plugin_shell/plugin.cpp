// This is an auto-generated file.
// Do not edit! All changes made to it will be lost.
#include "plugin.h"

#include <qqml.h>

#include "shell.h"
#include "scope.h"



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
     // @uri CoreUI.Shell
    qmlRegisterType<Shell>(uri, 1, 0, "Shell");
    qmlRegisterType<Scope>(uri, 1, 0, "Scope");
}

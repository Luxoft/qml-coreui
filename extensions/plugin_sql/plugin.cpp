// This is an auto-generated file.
// Do not edit! All changes made to it will be lost.
#include "plugin.h"

#include <qqml.h>

#include "sqlquerydatasource.h"
#include "sqltabledatasource.h"


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
     // @uri CoreUI.SQL
    qmlRegisterType<SqlQueryDataSource>(uri, 1, 0, "SqlQueryDataSource");
    qmlRegisterType<SqlTableDataSource>(uri, 1, 0, "SqlTableDataSource");
}
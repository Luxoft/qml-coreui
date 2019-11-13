// This is an auto-generated file.
// Do not edit! All changes made to it will be lost.
#include "plugin.h"

#include <qqml.h>

#include "store.h"
#include "view.h"
#include "panel.h"
#include "control.h"
#include "object.h"
#include "variantmodel.h"

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
     // @uri CoreUI
     qmlRegisterType<Store>(uri, 1, 0, "CoreStore");
     qmlRegisterType<View>(uri, 1, 0, "CoreView");
     qmlRegisterType<Panel>(uri, 1, 0, "CorePanel");
     qmlRegisterType<Control>(uri, 1, 0, "CoreControl");
     qmlRegisterType<Object>(uri, 1, 0, "CoreObject");
     qmlRegisterType<VariantModel>(uri, 1, 0, "CoreModel");
}

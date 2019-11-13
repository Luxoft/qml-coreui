#include "plugin.h"
// <interface-includes>

{{module|title}}Plugin::{{module|title}}Plugin(QObject *parent)
    : QObject(parent)
{
    // <interface-new>
}

QStringList {{module|title}}Plugin::interfaces() const
{
    QStringList list;
    // <interface-id>
    return list;
}

QIviFeatureInterface *{{module|title}}Plugin::interfaceInstance(const QString &interface) const
{
     int index = interfaces().indexOf(interface);
     return index < 0 ? nullptr : m_interfaces.at(index);
}

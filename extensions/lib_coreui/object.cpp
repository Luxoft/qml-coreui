#include "object.h"

#include <QtQuick>

Object::Object(QObject *parent)
    : QObject(parent)
{
}

QQmlListProperty<QObject> Object::data()
{
    return QQmlListProperty<QObject>(this, this, &Object::data_append,
                                     &Object::data_count, &Object::data_at,
                                     &Object::data_clear);
}

QObject *Object::parentObject() const
{
    return parent();
}

void Object::data_append(QQmlListProperty<QObject> *property, QObject *data)
{
    qDebug() << "data append" << property << data;
    Object* object = static_cast<Object*>(property->object);
    if(qobject_cast<QQuickItem*>(data)) {
        qWarning() << "Can not have visual items as childs of none-visual items";
        return;
    }
    if(data->parent() == object) {
        data->setParent(nullptr);
    }
    data->setParent(object);
    object->m_data.append(data);
}

int Object::data_count(QQmlListProperty<QObject> *property)
{
    Object* o = static_cast<Object*>(property->object);
    return o->m_data.count();
}

QObject *Object::data_at(QQmlListProperty<QObject> *property, int index)
{
    Object* o = static_cast<Object*>(property->object);
    return o->m_data.value(index);
}

void Object::data_clear(QQmlListProperty<QObject> *property)
{
    Object* o = static_cast<Object*>(property->object);
    for(QObject* data : qAsConst(o->m_data)) {
        data->setParent(nullptr);
    }
    o->m_data.clear();
}

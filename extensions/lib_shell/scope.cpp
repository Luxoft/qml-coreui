#include "scope.h"

Scope::Scope(QObject *parent) : QObject(parent)
{

}

void Scope::load(const QString &name)
{
    qDebug() << "load script from: " << name;
}

void Scope::set(const QString &name, const QJSValue &value)
{
    qDebug() << "Scope.set() " << name << value.toString();
    m_variables.insert(name, value);
}

QJSValue Scope::get(const QString &name, const QJSValue &defaultValue) const
{
    qDebug() << "Scope.get() " << name;
    return m_variables.value(name, defaultValue);
}

QJSValue Scope::unset(const QString &name)
{
    return m_variables.take(name);
}

QStringList Scope::list() const
{
    return m_variables.keys();
}

#ifndef SCOPE_H
#define SCOPE_H

#include <QtCore>
#include <QtQml>

#include <c++/v1/list>

class Scope : public QObject
{
    Q_OBJECT
public:
    explicit Scope(QObject *parent = 0);
    Q_INVOKABLE void load(const QString &name);
    Q_INVOKABLE void set(const QString &name, const QJSValue &value);
    Q_INVOKABLE QJSValue get(const QString &name, const QJSValue &defaultValue=QJSValue()) const;
    Q_INVOKABLE QJSValue unset(const QString &name);
    Q_INVOKABLE QStringList list() const;
private:
    QHash<QString, QJSValue> m_variables;
};

#endif // SCOPE_H

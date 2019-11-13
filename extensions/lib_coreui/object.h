#ifndef OBJECT_H
#define OBJECT_H

#include <QtCore>
#include <QtQml>

class Object : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QQmlListProperty<QObject> data READ data)
    Q_PROPERTY(QObject*  parent READ parentObject)
    Q_CLASSINFO("DefaultProperty", "data")
public:
    explicit Object(QObject *parent = nullptr);
    QQmlListProperty<QObject> data();
    QObject* parentObject() const;
private:
    static void data_append(QQmlListProperty<QObject> *property, QObject *data);
    static int data_count(QQmlListProperty<QObject> *property);
    static QObject *data_at(QQmlListProperty<QObject> *property, int index);
    static void data_clear(QQmlListProperty<QObject> *property);
private:
    QList<QObject*> m_data;
};

#endif // OBJECT_H

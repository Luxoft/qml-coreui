#pragma once

#include <QtCore>
#include <QtIviCore/QIviServiceInterface>

QT_BEGIN_NAMESPACE

class {{module|title}}Plugin : public QObject, QIviServiceInterface
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QIviServiceInterface_iid FILE "{{module|lower}}.json")
    Q_INTERFACES(QIviServiceInterface)

public:
    typedef QVector<QIviFeatureInterface *> (InterfaceBuilder)({{module|title}}Plugin *);

    explicit {{module|title}}Plugin(QObject *parent = nullptr);

    QStringList interfaces() const;
    QIviFeatureInterface* interfaceInstance(const QString& interface) const;

private:
    QVector<QIviFeatureInterface *> m_interfaces;
};

QT_END_NAMESPACE

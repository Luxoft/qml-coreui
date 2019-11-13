#pragma once

#include <QtCore>

#include "core.h"

// <service-includes>

Q_DECLARE_LOGGING_CATEGORY(ServerCategory)

class Server : public QObject
{
    Q_OBJECT
public:
    explicit Server(QObject *parent = nullptr);

    void start();
    void enableService(QObject* service, const QString& name);

public slots:
    void onROError(QRemoteObjectNode::ErrorCode code);
    void onAboutToQuit();

protected slots:
    void onTimeout();
private:
    // <service-members>
};


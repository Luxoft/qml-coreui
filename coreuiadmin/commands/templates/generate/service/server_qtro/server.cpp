#include "server.h"

Q_LOGGING_CATEGORY(ServerCategory, "server")

Server::Server(QObject *parent) : QObject(parent)
{
    connect(QCoreApplication::instance(),&QCoreApplication::aboutToQuit,
            this,&Server::onAboutToQuit);

    // <service-list>

}

void Server::start()
{
}

void Server::onROError(QRemoteObjectNode::ErrorCode code)
{
    qCWarning(ServerCategory) << "Remote objects error, code:" << code;
}

void Server::onAboutToQuit()
{
}

void Server::onTimeout()
{
}

void Server::enableService(QObject* service, const QString& name)
{
    Core::instance()->host()->enableRemoting(service, name);
    Core::instance()->host()->setHeartbeatInterval(1000); // 1000ms
}

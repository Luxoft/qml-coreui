#include <QCoreApplication>

#include "server.h"

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    app.setApplicationName("{{id}}_server_qtro");

    QLockFile lockFile(QStringLiteral("%1/%2.lock").arg(QDir::tempPath(), app.applicationName()));
    if (!lockFile.tryLock(100)) {
        qCritical("%s already running, aborting...", qPrintable(app.applicationName()));
        return EXIT_FAILURE;
    }

    Server server;
    server.start();
    return app.exec();
}
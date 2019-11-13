#pragma once

#include <QtCore>

class CoreUI : public QObject
{
    Q_OBJECT
public:
    CoreUI *instance();
private:
    explicit CoreUI(QObject *parent = nullptr);
private:
    static CoreUI* s_instance;
};

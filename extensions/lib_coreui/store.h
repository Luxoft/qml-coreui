#pragma once

#include <QtCore>

#include "object.h"

class Store : public Object
{
    Q_OBJECT
public:
    explicit Store(QObject *parent = nullptr);
};

#pragma once

#include <QtQuick>

class View : public QQuickItem
{
    Q_OBJECT
public:
    View(QQuickItem* parent=nullptr);
};

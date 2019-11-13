#pragma once

#include <QtCore>
#include "abstractdatasource.h"

class JSONDataSource : public AbstractDataSource
{
    Q_OBJECT
public:
    JSONDataSource(QObject *parent=nullptr);
public:
    virtual void loadDocument() override;
    virtual void saveDocument() override;
private:
};

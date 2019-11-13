{% set class = '{0}Backend'.format(interface) %}
#pragma once

#include <QtCore>
#include "{{class|lower}}interface.h"

class {{class}} : public {{class}}Interface
{
    Q_OBJECT
public:
    explicit {{class}}(QObject *parent = nullptr);
    ~{{class}}();

    void initialize() override;
};

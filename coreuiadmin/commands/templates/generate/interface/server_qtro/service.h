{% set class = '{0}Service'.format(interface) %}
#pragma once

#include <QtCore>
#include "rep_{{interface|lower}}_source.h"

class {{class}} : public {{interface}}Source
{
    Q_OBJECT

public:
    explicit {{class}}(QObject *parent = nullptr);
    ~{{class}}();
};

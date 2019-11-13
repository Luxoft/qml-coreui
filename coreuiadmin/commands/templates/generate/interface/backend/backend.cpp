{% set class = '{0}Backend'.format(interface) %}
#include "{{class|lower}}.h"


{{class}}::{{class}}(QObject *parent)
    : {{class}}Interface(parent)
{
    {{module|title}}Module::registerTypes();
}

{{class}}::~{{class}}()
{
}

void {{class}}::initialize()
{
}

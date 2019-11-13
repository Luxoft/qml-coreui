#include "plugin.h"
#include "{{module}}module.h"


void {{module|title}}Plugin::registerTypes(const char *uri)
{
    // @uri {{uri}}
    {{module|title}}Module::registerTypes();
    {{module|title}}Module::registerQmlTypes(uri, 1, 0);
}


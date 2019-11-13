#include "coreui.h"

CoreUI *CoreUI::s_instance = nullptr;

CoreUI *CoreUI::instance()
{
    if(!s_instance) {
        s_instance = new CoreUI(QCoreApplication::instance());
    }
    return s_instance;
}

CoreUI::CoreUI(QObject *parent) : QObject(parent)
{

}

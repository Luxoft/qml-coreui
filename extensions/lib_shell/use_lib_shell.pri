QT += core
QT += qml

LIBS += -L$$BUILD_DIR/libs
LIBS += -llib_shell

INCLUDEPATH += $$PWD

include( $$SOURCE_DIR/src/lib_coreui/use_lib_coreui.pri )

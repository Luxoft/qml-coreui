TEMPLATE = lib
QT += qml
CONFIG += qt plugin c++11
DESTDIR = $$BUILD_DIR/imports/CoreUI/Trace
TARGET = plugin_trace

uri = CoreUI.Trace

HEADERS += plugin.h
SOURCES += plugin.cpp

DISTFILES = qmldir

!equals(_PRO_FILE_PWD_, $$OUT_PWD) {
    copy_qmldir.target = $$BUILD_DIR/imports/CoreUI/Trace/qmldir
    copy_qmldir.depends = $$_PRO_FILE_PWD_/qmldir
    copy_qmldir.commands = $(COPY_FILE) \"$$replace(copy_qmldir.depends, /, $$QMAKE_DIR_SEP)\" \"$$replace(copy_qmldir.target, /, $$QMAKE_DIR_SEP)\"
    QMAKE_EXTRA_TARGETS += copy_qmldir
    PRE_TARGETDEPS += $$copy_qmldir.target
}

qmldir.files = qmldir
unix {
    installPath = $$[QT_INSTALL_QML]/$$replace(uri, \\., /)
    qmldir.path = $$installPath
    target.path = $$installPath
    INSTALLS += target qmldir
}

include( $$SOURCE_DIR/src/lib_trace/use_lib_trace.pri )

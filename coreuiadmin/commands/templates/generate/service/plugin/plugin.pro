uri = {{uri}}

TEMPLATE = lib
TARGET = {{id}}_plugin
DESTDIR=$$BUILD_DIR/imports/$$replace(uri, \\., /)
QT += core
QT += qml

CONFIG += plugin
CONFIG += c++11

SOURCES += plugin.cpp
HEADERS += plugin.h

DISTFILES = qmldir

OTHER_FILES += qmldir


LIBS += -L$$BUILD_DIR/libs/ -l{{id}}_frontend
INCLUDEPATH += $$OUT_PWD/../frontend

!equals(_PRO_FILE_PWD_, $$OUT_PWD) {
    copy_qmldir.target = $$replace(DESTDIR, /, $$QMAKE_DIR_SEP)$${QMAKE_DIR_SEP}qmldir
    copy_qmldir.depends = $$replace(_PRO_FILE_PWD_, /, $$QMAKE_DIR_SEP)$${QMAKE_DIR_SEP}qmldir
    copy_qmldir.commands = $(COPY_FILE) \"$$copy_qmldir.depends\" \"$$copy_qmldir.target\"
    QMAKE_EXTRA_TARGETS += copy_qmldir
    PRE_TARGETDEPS += $$copy_qmldir.target
}

!equals(_PRO_FILE_PWD_, $$OUT_PWD) {
    for(extra_file, EXTRA_FILES) {
        file = $$replace(_PRO_FILE_PWD_, /, $$QMAKE_DIR_SEP)$${QMAKE_DIR_SEP}$${extra_file}
        target = $$replace(DESTDIR, /, $$QMAKE_DIR_SEP)$${QMAKE_DIR_SEP}$${extra_file}
        copy_$${extra_file}.target = $$target
        copy_$${extra_file}.depends = $$file
        copy_$${extra_file}.commands = $(COPY_FILE) \"$$file\" \"$$target\"
        QMAKE_EXTRA_TARGETS += copy_$${extra_file}
        PRE_TARGETDEPS += $$target
    }
}

qmldir.files = qmldir
unix {
    installPath = $$INSTALL_PREFIX/imports/$$replace(uri, \\., /)
    qmldir.path = $$installPath
    target.path = $$installPath
    extra_files_install.path = $$installPath
    INSTALLS += target qmldir extra_files_install
}



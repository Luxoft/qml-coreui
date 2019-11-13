import QtQuick 2.11
import QtQuick.Controls 2.3

Pane {
    id: root

    property string title

    Label {
        anchors.centerIn: parent
        text: root.title
    }
}

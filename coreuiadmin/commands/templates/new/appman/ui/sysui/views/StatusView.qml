import QtQuick 2.10
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "../stores"

Pane {
    id: root
    width: 1280
    height: 80

    property RootStore store

    RowLayout {
        anchors.fill: parent
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        Button {
            text: root.store.currentDateString
            Layout.preferredWidth: root.width / 12
        }
        Button {
            text: root.store.currentTimeString
            Layout.preferredWidth: root.width / 12
        }
    }
}

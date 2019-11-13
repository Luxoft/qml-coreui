import QtQuick 2.11
import QtQuick.Controls 2.3
import "../stores"

Pane {
    id: root
    width: 1280
    height: 800
    property RootStore store

    ListView {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        height: parent.height * 0.5
        orientation: Qt.Horizontal

        model: store.applicationModel

        delegate: Control {
            height: ListView.view.height
            width: ListView.view.width/4
            padding: 24
            contentItem: Button {
                text: model.name
                onClicked: root.store.launch(model.applicationId)
            }
        }
    }
}

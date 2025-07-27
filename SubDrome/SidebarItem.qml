import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root
    property alias iconSource: icon.source
    property string label: ""
    signal clicked

    color: "transparent"
    height: 48
    width: parent ? parent.width : 200

    Row {
        anchors.verticalCenter: parent.verticalCenter
        spacing: 10

        Image {
            id: icon
            sourceSize: Qt.size(32, 32)
        }
        Text {
            text: root.label
            color: "white"
            font.pixelSize: 16
            verticalAlignment: Text.AlignVCenter
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: root.clicked()
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
    }
}

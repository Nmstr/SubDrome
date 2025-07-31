import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root
    property alias iconSource: cover.source
    property string title: "Unknown Title"
    property string artist: "Unknown Artist"
    color: "transparent"
    height: 48
    width: parent ? parent.width : 300

    Image {
        id: cover
        sourceSize: Qt.size(48, 48)
    }
    Column {
        anchors.left: cover.right
        anchors.leftMargin: 10
        spacing: 4

        Text {
            text: root.title
            color: "white"
            font.pixelSize: 16
            elide: Text.ElideRight
        }

        Text {
            text: root.artist
            color: "white"
            font.pixelSize: 14
            elide: Text.ElideRight
        }
    }
}

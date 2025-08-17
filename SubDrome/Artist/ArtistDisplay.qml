import QtQuick 2.15

Rectangle {
    id: artistDisplay
    color: "transparent"

    ArtistDisplayTopper {
        id: topper
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }

        implicitHeight: 50
    }

    Rectangle {
        anchors {
            top: topper.bottom
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        anchors.margins: 20
        color: "#424242"
        radius: 10
        clip: true
    }
}

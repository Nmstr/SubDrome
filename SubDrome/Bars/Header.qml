import QtQuick 2.15

Rectangle {
    id: header
    implicitHeight: 50
    color: "#2980ff"

    Row {
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
            rightMargin: 10
        }
        spacing: 10

        Image {
            source: "qrc:/icons/activity.svg"
            sourceSize: Qt.size(32, 32)
            Image {
                source: parent.source
                width: 0
                height: 0
            }
        }

        Image {
            source: "qrc:/icons/settings.svg"
            sourceSize: Qt.size(32, 32)
            Image {
                source: parent.source
                width: 0
                height: 0
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    settingsDropdown.visible = !settingsDropdown.visible;
                }
            }
        }
    }

    Text {
        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
            leftMargin: 10
        }
        text: "SubDrome"
        color: "white"
        font.pixelSize: 20
    }

    SettingsDropdown {
        id: settingsDropdown
        visible: false
        anchors {
            right: header.right
            top: header.bottom
            topMargin: -header.height / 2
            rightMargin: header.height / 2
        }
    }
}

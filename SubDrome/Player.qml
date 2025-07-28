import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    Header {
        id: header
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }
        implicitHeight: 50
    }

    Rectangle {
        anchors {
            top: header.bottom
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        color: "#303030"

        Sidebar {
            id: sidebar
            anchors {
                left: parent.left
                top: parent.top
                bottom: parent.bottom
            }

            implicitWidth: 250
        }

        AlbumDisplay {
            id: albumDisplay
            anchors {
                left: sidebar.right
                right: parent.right
                top: parent.top
                bottom: parent.bottom
            }
        }
    }

    ControlBar {
        id: controlBar
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        implicitHeight: 100
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

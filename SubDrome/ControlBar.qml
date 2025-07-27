import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: header
    implicitHeight: 100
    color: "#000000"
    opacity: 0.5

    Image {
        id: songIcon
        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
            leftMargin: 10
        }
        source: "qrc:/icons/song.svg"
        sourceSize: Qt.size(64, 64)
        Image {
            source: parent.source
            width: 0
            height: 0
        }
    }

    Column {
        id: songInfo
        anchors {
            left: songIcon.right
            verticalCenter: parent.verticalCenter
            leftMargin: 10
        }
        spacing: 5

        Text {
            text: "Song Title"
            color: "white"
            font.pixelSize: 20
        }

        Text {
            text: "Artist Name"
            color: "white"
            font.pixelSize: 16
        }
    }

    Column {
        id: controls
        anchors {
            verticalCenter: parent.verticalCenter
            horizontalCenter: parent.horizontalCenter
        }
        spacing: 10

        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 10

            Image {
                source: "qrc:/icons/skip-previous.svg"
                sourceSize: Qt.size(32, 32)
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: { console.log("Previous clicked") }
                }
            }

            Image {
                source: "qrc:/icons/play.svg"
                sourceSize: Qt.size(32, 32)
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: { console.log("Play clicked") }
                }
            }

            Image {
                source: "qrc:/icons/skip-next.svg"
                sourceSize: Qt.size(32, 32)
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: { console.log("Next clicked") }
                }
            }
        }

        Row {
            spacing: 10

            Text {
                text: "00:00"
                color: "white"
                font.pixelSize: 14
            }

            Slider {
                id: positionSlider
                width: 200
                from: 0
                to: 100
                stepSize: 1
                onValueChanged: {
                    console.log("Positon changed to:", value);
                }
            }

            Text {
                text: "04:30"
                color: "white"
                font.pixelSize: 14
            }
        }
    }

    Row {
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
            rightMargin: 10
        }
        spacing: 10

        Image {
            id: downloadIcon
            source: "qrc:/icons/download.svg"
            sourceSize: Qt.size(32, 32)
            Image {
                source: parent.source
                width: 0
                height: 0
            }
        }

        Image {
            id: volumeIcon
            source: "qrc:/icons/volume.svg"
            sourceSize: Qt.size(32, 32)
            Image {
                source: parent.source
                width: 0
                height: 0
            }
        }

        Slider {
            id: volumeSlider
            anchors.verticalCenter: parent.verticalCenter
            width: 200
            from: 0
            to: 100
            stepSize: 1
            onValueChanged: {
                console.log("Volume changed to:", value);
            }
        }
    }
}

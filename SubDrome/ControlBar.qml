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
                id: playPauseIcon
                source: "qrc:/icons/play.svg"
                sourceSize: Qt.size(32, 32)
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        if (playPauseIcon.source.toString() === "qrc:/icons/pause.svg") {
                            playbackHandler.pause();
                        } else {
                            playbackHandler.play();
                        }
                    }
                }
            }

            Image {
                source: "qrc:/icons/skip-next.svg"
                sourceSize: Qt.size(32, 32)
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: { playbackHandler.next_song(); }
                }
            }
        }

        Row {
            spacing: 10

            Text {
                id: positionText
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
                    if (pressed) {
                        playbackHandler.set_position(value);
                    }
                }
            }

            Text {
                id: durationText
                text: "00:00"
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
            Component.onCompleted: {
                volumeSlider.value = playbackHandler.get_volume() * 100;
            }
            onValueChanged: {
                playbackHandler.set_volume(value / 100);
            }
        }

        Text {
            anchors.verticalCenter: parent.verticalCenter
            text: Math.round(volumeSlider.value) + "%"
            color: "white"
            font.pixelSize: 14
        }
    }

    Connections {
        target: playbackHandler

        function onNewSong(title, artist, duration, art_path) {
            songInfo.children[0].text = title;
            songInfo.children[1].text = artist;
            let song_minutes = Math.floor(duration / 60);
            let song_seconds = duration % 60;
            durationText.text = song_minutes.toString().padStart(2, '0') + ":" + song_seconds.toString().padStart(2, '0');
            positionText.text = "00:00";
            positionSlider.value = 0;
            positionSlider.to = duration;
            songIcon.source = art_path || "qrc:/icons/song.svg";
        }

        function onPositionChanged(position) {
            positionSlider.value = position;
            let position_minutes = Math.floor(position / 60);
            let position_seconds = position % 60;
            positionText.text = position_minutes.toString().padStart(2, '0') + ":" + position_seconds.toString().padStart(2, '0');
        }

        function onIsPlaying(isPlaying) {
            if (isPlaying) {
                playPauseIcon.source = "qrc:/icons/pause.svg";
            } else {
                playPauseIcon.source = "qrc:/icons/play.svg";
            }
        }

    }
}

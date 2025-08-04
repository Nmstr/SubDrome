import QtQuick 2.15

Rectangle {
    id: playlistPage
    color: "transparent"
    property string playlistId: "";

    Rectangle {
        anchors.fill: parent
        anchors.margins: 20
        color: "#424242"
        radius: 10
        clip: true

        Image {
            id: coverImage
            anchors {
                top: parent.top
                left: parent.left
                margins: 20
            }
            fillMode: Image.PreserveAspectFit
            height: 300
            width: 300
        }

        Text {
            id: playlistTitle
            anchors {
                left: coverImage.right
                top: parent.top
                margins: 20
            }
            font.pixelSize: 24
            color: "white"
        }

        Text {
            id: ownerName
            anchors {
                left: coverImage.right
                top: playlistTitle.bottom
                margins: 20
            }
            font.pixelSize: 18
            color: "lightgray"
        }

        ListView {
            id: songListView
            clip: true
            anchors {
                left: parent.left
                right: parent.right
                top: coverImage.bottom
                bottom: parent.bottom
                margins: 20
            }
            model: songListModel

            delegate: Rectangle {
                width: parent.width
                height: 40
                color: index % 2 === 0 ? "#333" : "#222"
                Row {
                    spacing: 10
                    Image {
                        source: "qrc:/icons/play.svg"
                        sourceSize: Qt.size(24, 24)
                        Image {
                            source: parent.source
                            width: 0
                            height: 0
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                playbackHandler.play_song(playlistPage.playlistId, songListModel.get(index).id);
                            }
                        }
                    }
                    Text { text: name; color: "white" }
                    Text { text: artist; color: "lightgray" }
                    Text { text: duration + "s"; color: "gray" }
                }
            }
        }
    }

    ListModel { id: songListModel }

    Connections {
        target: apiHandler

        function onPlaylistDetailsReceived(id, name, owner, cover_path, songs) {
            albumPage.albumId = id;
            coverImage.source = cover_path;
            playlistTitle.text = name;
            ownerName.text = owner;
            songListModel.clear();
            for (var i = 0; i < songs.length; i++) {
                var song = songs[i];
                songListModel.append({
                    id: song[0],
                    name: song[1],
                    artist: song[2],
                    duration: song[3]
                });
            }
        }
    }
}

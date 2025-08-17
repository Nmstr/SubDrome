import QtQuick 2.15

Rectangle {
    id: albumPage
    color: "transparent"
    property string albumId: "";

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
            id: albumTitle
            anchors {
                left: coverImage.right
                top: parent.top
                margins: 20
            }
            font.pixelSize: 24
            color: "white"
        }

        Image {
            id: favouriteIcon
            anchors {
                left: albumTitle.right
                top: parent.top
                margins: 20
                topMargin: 25
            }
            fillMode: Image.PreserveAspectFit
            width: 24
            height: 24
            source: "qrc:/icons/no_favourite.svg"

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if (favouriteIcon.source.toString() === "qrc:/icons/no_favourite.svg") {
                        favouriteIcon.source = "qrc:/icons/favourite.svg";
                        apiHandler.set_favourite_status(albumPage.albumId, true);
                    } else {
                        favouriteIcon.source = "qrc:/icons/no_favourite.svg";
                        apiHandler.set_favourite_status(albumPage.albumId, false);
                    }
                }
            }
        }

        Text {
            id: artistName
            anchors {
                left: coverImage.right
                top: albumTitle.bottom
                margins: 20
            }
            font.pixelSize: 18
            color: "lightgray"
        }

        Text {
            id: songCountAndDuration
            anchors {
                left: coverImage.right
                top: artistName.bottom
                margins: 20
            }
            font.pixelSize: 16
            color: "white"
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
                                playbackHandler.play_song(albumPage.albumId, songListModel.get(index).id);
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

        function onAlbumDetailsReceived(id, name, artist, cover_path, song_count, duration, songs) {
            albumPage.albumId = id;
            coverImage.source = cover_path;
            albumTitle.text = name;
            artistName.text = artist;
            songCountAndDuration.text = song_count + " Songs · " + duration;
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

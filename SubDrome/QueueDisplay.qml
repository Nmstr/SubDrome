import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: queueDisplay
    anchors.margins: 20
    color: "#424242"
    radius: 10

    Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        color: "transparent"

        Text {
            id: nowPlayingLabel
            text: "Now Playing"
            color: "white"
            font.pixelSize: 24
        }

        QueueItem {
            id: currentTrack
            anchors {
                left: parent.left
                right: parent.right
                top: nowPlayingLabel.bottom
            }
            iconSource: "qrc:/icons/song.svg"
            title: "Current Track Title"
            artist: "Current Artist"
        }

        Text {
            id: nextLabel
            anchors {
                left: parent.left
                right: parent.right
                top: currentTrack.bottom
            }
            text: "Next"
            color: "white"
            font.pixelSize: 24
        }

        ListView {
            id: queueListView
            model: queueListModel
            clip: true
            anchors {
                left: parent.left
                right: parent.right
                top: nextLabel.bottom
                bottom: parent.bottom
            }

            delegate: QueueItem {
                width: parent.width
                height: 48
                iconSource: song_cover
                title: song_title
                artist: song_artist
            }

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AlwaysOn
            }
        }
    }

    ListModel { id: queueListModel }

    Connections {
        target: playbackHandler

        function onQueueUpdated(cur_title, cur_artist, cur_cover, next_songs) {
            currentTrack.title = cur_title;
            currentTrack.artist = cur_artist;
            currentTrack.iconSource = cur_cover;

            queueListModel.clear();
            for (var i = 0; i < next_songs.length; i++) {
                let song = next_songs[i];
                queueListModel.append({
                    song_title: song[0],
                    song_artist: song[1],
                    song_cover: song[2] || "qrc:/icons/song.svg"
                });
            }
        }
    }
}

import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: queueDisplay
    anchors.margins: 20
    color: "#424242"
    radius: 10

    Column {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        Text {
            text: "Now Playing"
            color: "white"
            font.pixelSize: 24
        }

        QueueItem {
            id: currentTrack
            iconSource: "qrc:/icons/song.svg"
            title: "Current Track Title"
            artist: "Current Artist"
        }

        Text {
            text: "Next"
            color: "white"
            font.pixelSize: 24
        }
    }

    Connections {
        target: playbackHandler

        function onQueueUpdated(cur_title, cur_artist, cur_cover, next_songs) {
            currentTrack.title = cur_title;
            currentTrack.artist = cur_artist;
            currentTrack.iconSource = cur_cover;

            console.log("Next songs updated:", next_songs);
        }
    }
}

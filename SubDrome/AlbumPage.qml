import QtQuick 2.15

Rectangle {
    id: albumPage
    anchors.fill: parent
    color: "transparent"

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
    }

    Connections {
        target: apiHandler

        function onAlbumDetailsReceived(name, artist, cover_path, songs) {
            console.log(name, artist, cover_path, songs);
            coverImage.source = cover_path;
            albumTitle.text = name;
            artistName.text = artist;
        }
    }
}

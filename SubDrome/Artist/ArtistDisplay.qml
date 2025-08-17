import QtQuick 2.15

Rectangle {
    id: artistDisplay
    color: "transparent"

    function loadArtists(artists) {
        artistListModel.clear();
        contentStack.currentIndex = 3;

        if (!artists) {
            artists = apiHandler.get_artists();
        }
        for (let i = 0; i < artists.length; i++) {
            let artist = artists[i];
            artistListModel.append({
                id: artist[0],
                name: artist[1],
                albumCount: artist[2]
            });
        }
    }

    ListModel { id: artistListModel }

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

        ListView {
            id: artistListView
            anchors {
                fill: parent
                margins: 20
            }
            model: artistListModel

            delegate: Rectangle {
                width: parent.width
                height: 40
                color: index % 2 === 0 ? "#333" : "#222"

                Row {
                    anchors.fill: parent
                    spacing: 10

                    Image {
                        source: "qrc:/icons/artist.svg"
                        width: 40
                        height: 40
                        fillMode: Image.PreserveAspectFit
                    }

                    Text {
                        text: model.name
                        color: "white"
                        font.pixelSize: 18
                        verticalAlignment: Text.AlignVCenter
                    }

                    Text {
                        text: model.albumCount + " albums"
                        color: "#888"
                        font.pixelSize: 14
                        verticalAlignment: Text.AlignVCenter
                    }
                }
            }
        }
    }
}

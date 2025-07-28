import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: albumDisplay
    color: "transparent"

    Rectangle {
        anchors.fill: parent
        anchors.margins: 20
        color: "#424242"
        radius: 10

        GridView {
            id: grid
            anchors.fill: parent
            cellWidth: 200
            cellHeight: 250
            model: albumModel

            delegate: Rectangle {
                width: 200
                height: 250
                color: "#616161"
                radius: 8
                border.color: "#888"

                Column {
                    anchors.centerIn: parent

                    Image {
                        source: model.cover_path
                        width: 190
                        height: 190
                        fillMode: Image.PreserveAspectFit
                    }
                    Text {
                        text: model.title
                        width: parent.width
                        elide: Text.ElideRight
                        wrapMode: Text.NoWrap
                    }
                    Text {
                        text: model.artist
                        width: parent.width
                        elide: Text.ElideRight
                        wrapMode: Text.NoWrap
                    }
                }
            }
        }
    }

    ListModel { id: albumModel }
    
    Connections {
        target: apiHandler

        function onAlbumsUpdated(albums) {
            albumModel.clear();
            for (var i = 0; i < albums.length; ++i) {
                var album = albums[i];
                albumModel.append({
                    id: album[0],
                    title: album[1],
                    artist: album[2],
                    cover_path: album[3]
                });
            }
        }

        function onCoverReady(albumId, coverPath) {
            console.log(albumId, coverPath);
            for (var i = 0; i < albumModel.count; ++i) {
                if (albumModel.get(i).id === albumId) {
                    albumModel.setProperty(i, "cover_path", coverPath);
                    break;
                }
            }
        }
    }
}

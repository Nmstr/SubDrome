import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: albumDisplay
    color: "transparent"
    property string currentAlbumType: "alphabeticalByName"

    function loadAlbums(type, page) {
        contentStack.currentIndex = 0;
        currentAlbumType = type;
        topper.currentSearch = "";
        topper.currentPage = page;
        apiHandler.get_albums(type, page);
    }

    AlbumDisplayTopper {
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

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        apiHandler.get_album_details(model.id);
                        contentStack.currentIndex = 1;
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
            for (var i = 0; i < albumModel.count; ++i) {
                if (albumModel.get(i).id === albumId) {
                    albumModel.setProperty(i, "cover_path", coverPath);
                    break;
                }
            }
        }
    }
}

import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: sidebar
    implicitWidth: 50
    color: "#303030"
    property bool albumsExpanded: false
    property bool playlistsExpanded: false

    Column {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 10

        SidebarItem {
            iconSource: "qrc:/icons/album.svg"
            label: "Albums"
            onClicked: sidebar.albumsExpanded = !sidebar.albumsExpanded
        }

        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/album.svg"; label: "All";
            onClicked: { contentStack.currentIndex = 0; apiHandler.get_albums("alphabeticalByName") } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/shuffle.svg"; label: "Random";
            onClicked: { contentStack.currentIndex = 0; apiHandler.get_albums("random") } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/favourite.svg"; label: "Favourites";
            onClicked: { contentStack.currentIndex = 0; apiHandler.get_albums("starred") } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/star_full.svg"; label: "Top Rated";
            onClicked: { } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/plus.svg"; label: "Recently Added";
            onClicked: { contentStack.currentIndex = 0; apiHandler.get_albums("newest") } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/history.svg"; label: "Recently Played";
            onClicked: { contentStack.currentIndex = 0; apiHandler.get_albums("recent") } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/repeat.svg"; label: "Most Played";
            onClicked: { contentStack.currentIndex = 0; apiHandler.get_albums("frequent") } }

        SidebarItem { iconSource: "qrc:/icons/artist.svg"; label: "Artists";
            onClicked: { } }
        SidebarItem { iconSource: "qrc:/icons/song.svg"; label: "Songs";
            onClicked: { } }
        SidebarItem { iconSource: "qrc:/icons/playlist.svg"; label: "Playlists";
            onClicked: sidebar.playlistsExpanded = !sidebar.playlistsExpanded }

        ListView {
            id: playlistsListView
            model: playlistsListModel
            width: parent.width
            height: 200
            spacing: 5
            x: 24

            delegate: SidebarItem {
                visible: sidebar.playlistsExpanded
                iconSource: model.cover
                label: model.name
                onClicked: {
                    contentStack.currentIndex = 2;
                    apiHandler.get_playlist_details(model.id);
                }
            }

            Component.onCompleted: {
                apiHandler.update_playlist_list()
            }
        }
    }

    ListModel { id: playlistsListModel }

    Connections {
        target: apiHandler

        function onPlaylistListChanged(playlists) {
            playlistsListModel.clear();
            for (let i = 0; i < playlists.length; i++) {
                let playlist = playlists[i];
                playlistsListModel.append({
                    id: playlist[0],
                    name: playlist[1],
                    cover: playlist[2] || "qrc:/icons/playlist.svg",
                });
            }
        }
    }
}

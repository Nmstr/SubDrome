import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: sidebar
    implicitWidth: 50
    color: "#303030"
    property bool albumsExpanded: false

    Column {
        anchors.fill: parent
        spacing: 10

        SidebarItem {
            iconSource: "qrc:/icons/album.svg"
            label: "Albums"
            onClicked: sidebar.albumsExpanded = !sidebar.albumsExpanded
        }

        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/album.svg"; label: "All";
            onClicked: { } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/shuffle.svg"; label: "Random";
            onClicked: { contentStack.currentIndex = 0; apiHandler.get_random_albums() } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/favourite.svg"; label: "Favourites";
            onClicked: { } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/star_full.svg"; label: "Top Rated";
            onClicked: { } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/plus.svg"; label: "Recently Added";
            onClicked: { } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/history.svg"; label: "Recently Played";
            onClicked: { } }
        SidebarItem { visible: sidebar.albumsExpanded; x: 24;
            iconSource: "qrc:/icons/repeat.svg"; label: "Most Played";
            onClicked: { } }

        SidebarItem { iconSource: "qrc:/icons/artist.svg"; label: "Artists";
            onClicked: { } }
        SidebarItem { iconSource: "qrc:/icons/song.svg"; label: "Songs";
            onClicked: { } }
        SidebarItem { iconSource: "qrc:/icons/playlist.svg"; label: "Playlists";
            onClicked: { } }
    }
}

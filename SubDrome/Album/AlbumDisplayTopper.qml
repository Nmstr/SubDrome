import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: header
    color: "transparent"

    TextField {
        id: searchField
        anchors {
            left: parent.left
            top: parent.top
            leftMargin: 20
            topMargin: 20
        }
        width: 200
        placeholderText: "Search"
        placeholderTextColor: "#888"
        color: "white"
        font.pixelSize: 16
        background: Rectangle {
            color: "#424242"
            radius: 5
            border.color: "#888"
        }
        onTextChanged: {
            apiHandler.search_albums(text);
        }
    }
}

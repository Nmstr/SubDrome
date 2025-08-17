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
            apiHandler.search_albums(text, 1);
        }
    }

    Row {
        anchors {
            right: parent.right
            top: parent.top
            rightMargin: 20
            topMargin: 20
        }
        spacing: 10

        Text {
            text: "Page: "
            color: "white"
            font.pixelSize: 16
            anchors.verticalCenter: parent.verticalCenter
        }
        SpinBox {
            id: pageSpinBox
            width: 60
            from: 1
            stepSize: 1
            contentItem: Text {
                text: parent.textFromValue(parent.value)
                color: "white"
                font.pixelSize: 16
                horizontalAlignment: TextInput.AlignHCenter
            }
            background: Rectangle {
                color: "#424242"
                radius: 5
                border.color: "#888"
            }
            onValueChanged: {
                if (searchField.text == "") {
                    apiHandler.get_albums(albumDisplay.currentAlbumType, value);
                } else {
                    apiHandler.search_albums(searchField.text, value);
                }
            }
        }
    }
}

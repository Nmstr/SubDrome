import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: settingsDropdown
    width: 200
    height: 300
    color: "#424242"
    radius: 10

    Column {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 10

        Text {
            text: "Settings"
            color: "white"
            font.pixelSize: 18
        }

        Button {
            id: logoutButton
            text: "Logout"
            width: parent.width
            height: 40

            property color normalColor: "#2980ff"
            property color pressedColor: "#1a66cc"

            background: Rectangle {
                id: buttonBackground
                color: logoutButton.down ? logoutButton.pressedColor : logoutButton.normalColor
                radius: 5

                Behavior on color {
                    ColorAnimation {
                        duration: 100
                    }
                }
            }

            onClicked: {
                console.log("Logout clicked");
                loginHandler.logout();
            }
        }
    }
}

import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    color: "#303030"

    Rectangle {
        anchors {
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }
        width: 600
        height: 800
        radius: 10
        color: "#424242"

        Rectangle {
            id: header
            anchors {
                left: parent.left
                right: parent.right
                top: parent.top
            }
            height: 50
            topLeftRadius: 10
            topRightRadius: 10
            color: "#2980ff"

            Text {
                anchors.centerIn: parent
                text: "SubDrome"
                color: "white"
                font.pixelSize: 20
            }
        }

        Column {
            anchors {
                left: parent.left
                right: parent.right
                top: header.bottom
                margins: 20
            }
            spacing: 20

            TextField {
                id: urlField
                placeholderText: "Server URL"
                width: parent.width
                height: 40
                font.pixelSize: 16
                background: Rectangle {
                    color: "#545454"
                    radius: 5
                }
            }

            TextField {
                id: usernameField
                placeholderText: "Username"
                width: parent.width
                height: 40
                font.pixelSize: 16
                background: Rectangle {
                    color: "#545454"
                    radius: 5
                }
            }

            TextField {
                id: passwordField
                placeholderText: "Password"
                width: parent.width
                height: 40
                font.pixelSize: 16
                echoMode: TextInput.Password
                background: Rectangle {
                    color: "#545454"
                    radius: 5
                }
            }

            Button {
                id: loginButton
                text: "Login"
                width: parent.width
                height: 40

                property color normalColor: "#2980ff"
                property color pressedColor: "#1a66cc"

                background: Rectangle {
                    id: buttonBackground
                    color: loginButton.down ? loginButton.pressedColor : loginButton.normalColor
                    radius: 5

                    Behavior on color {
                        ColorAnimation {
                            duration: 100
                        }
                    }
                }

                onClicked: {
                    loginHandler.handle_login(urlField.text, usernameField.text, passwordField.text);
                }
            }

            Text {
                id: errorLabel
                color: "red"
                visible: false
                text: ""
            }
        }
    }

    Connections {
        target: loginHandler

        function onLoginFailed(msg) {
            errorLabel.text = msg;
            errorLabel.visible = true;
        }
    }
}

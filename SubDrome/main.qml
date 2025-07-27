import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: appWindow
    visible: true
    width: 1024
    height: 768
    title: "SubDrome"

    Loader {
        id: pageLoader
        anchors.fill: parent
        source: "Login.qml"
    }

    Connections {
        target: loginHandler

        function onLoginSuccess() {
            pageLoader.source = "Player.qml";
        }
    }
}

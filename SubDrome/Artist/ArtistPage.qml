import QtQuick 2.15
import Elements 1.0

Rectangle {
    id: artistPage
    color: "transparent"
    property string artistId: "";

    function loadArtistDetails(id) {
        artistPage.artistId = id;
        let artist = apiHandler.get_artist(id);
        if (artist) {
            artistName.text = artist[1];
            artistImage.source = artist[2];
            favouriteIcon.source = artist[4] ? "qrc:/icons/favourite.svg" : "qrc:/icons/no_favourite.svg";
            ratingStars.currentRating = artist[5];
        }
        contentStack.currentIndex = 4;
    }

    Rectangle {
        anchors.fill: parent
        anchors.margins: 20
        color: "#424242"
        radius: 10

        Image {
            id: artistImage
            anchors {
                top: parent.top
                left: parent.left
                margins: 20
            }
            fillMode: Image.PreserveAspectFit
            height: 300
            width: 300
        }

        Text {
            id: artistName
            anchors {
                left: artistImage.right
                top: parent.top
                margins: 20
            }
            font.pixelSize: 24
            color: "white"
        }

        Image {
            id: favouriteIcon
            anchors {
                left: artistName.right
                top: parent.top
                margins: 20
                topMargin: 25
            }
            fillMode: Image.PreserveAspectFit
            width: 24
            height: 24
            source: "qrc:/icons/no_favourite.svg"

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if (favouriteIcon.source.toString() === "qrc:/icons/no_favourite.svg") {
                        favouriteIcon.source = "qrc:/icons/favourite.svg";
                        apiHandler.set_favourite_status(artistPage.artistId, true);
                    } else {
                        favouriteIcon.source = "qrc:/icons/no_favourite.svg";
                        apiHandler.set_favourite_status(artistPage.artistId, false);
                    }
                }
            }
        }

        RatingStars {
            id: ratingStars
            anchors {
                left: artistImage.right
                top: artistName.bottom
                margins: 20
            }
            currentRating: 0
            targetId: artistPage.artistId
        }
    }
}

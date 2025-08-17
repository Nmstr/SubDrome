import QtQuick 2.15

Row {
    id: ratingStars
    property int currentRating: 0
    property string targetId: ""
    spacing: 10

    Repeater {
        model: 5
        delegate: Image {
            width: 24
            height: 24
            fillMode: Image.PreserveAspectFit
            source: index < ratingStars.currentRating ? "qrc:/icons/star_full.svg" : "qrc:/icons/star_empty.svg"
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if (ratingStars.currentRating === index + 1) {
                        ratingStars.currentRating = 0;  // Current rating is clicked again, remove rating
                    } else {
                        ratingStars.currentRating = index + 1;
                    }
                    apiHandler.set_rating(ratingStars.targetId, ratingStars.currentRating);
                }
            }
        }
    }
}

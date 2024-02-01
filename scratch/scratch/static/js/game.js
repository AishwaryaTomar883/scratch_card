
document.addEventListener("DOMContentLoaded", function () {
  var dataContainers = document.querySelectorAll(".sc__container");

  dataContainers.forEach(function (container) {
    var content = container.getAttribute("data-content");
    var gameTitle = container.getAttribute("game-title");
    var cardId = container.id.split('-').pop();  // Extract card ID from container ID

    var sc = new ScratchCard(container, {
      scratchType: SCRATCH_TYPE.CIRCLE,
      containerWidth: container.offsetWidth,
      containerHeight: 500,
      imageForwardSrc: "/static/images/scratch-image.png",
      imageBackgroundSrc: "/static/images/result.png",
      htmlBackground: `<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"><p>${content}</p></div>`,
      clearZoneRadius: 70,
      nPoints: 60,
      pointSize: 8,
      callback: function () {
        alert("Scratched! Content: " + content);
        // After scratching, make an AJAX call
        sendScratchData(cardId, content, gameTitle);
        // Reset the card after scratching (optional)
        // window.location.reload();
      },
    });

    // Init
    sc.init()
      .then(() => {
        sc.canvas.addEventListener("scratch.move", () => {
          let percent = sc.getPercent().toFixed(0);
          console.log("Scratch progress: " + percent + "%");
        });
      })
      .catch((error) => {
        // Handle image loading error
        alert(error.message);
      });
  });
});

function sendScratchData(cardId, content, gameTitle) {
    let currentURL = new URL(window.location.href);
    let email = currentURL.searchParams.get("email");

    fetch('/myapp/scratch-details/?email=' + email, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            cardId: cardId,
            content: content,
            gameTitle: gameTitle,
        }),
    })

    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

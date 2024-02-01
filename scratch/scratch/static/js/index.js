
document.addEventListener("DOMContentLoaded", function () {
  const scContainer = document.getElementById("js--sc--container");
  const scInfos = document.querySelector(".sc__infos");

  const sc = new ScratchCard(scContainer, {
    scratchType: SCRATCH_TYPE.SPRAY,
    containerWidth: scContainer.offsetWidth,
    containerHeight: 500,
    brushSrc: "/static/images/brush.png",
    imageForwardSrc: "/static/images/scratch-image.png",
    imageBackgroundSrc: "/static/images/result.png",
    htmlBackground: `<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"><p>Hello World!</p></div>`,
    clearZoneRadius: 70,
    nPoints: 60,
    pointSize: 8,
    callback: function () {
    alert("Now the window will reload !");
    window.location.reload();
    }
  });

  // Init
  sc.init()
    .then(() => {
      sc.canvas.addEventListener("scratch.move", () => {
        let percent = sc.getPercent().toFixed(0);
        scInfos.innerHTML = percent + "%";
        console.log(percent);
      });
    })
    .catch((error) => {
      // image not loaded
      alert(error.message);
    });
});


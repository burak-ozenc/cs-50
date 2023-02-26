window.onload = function () {

    // every column has 4 element and there are 4 column
    // on hover play the gif
    for (let i = 1; i < 5; i++) {
        for (let j = 1; j < 5; j++) {
            var img = document.getElementById(`img-${i}-${j}`);

            img.onmouseout = function () {
                this.src = `assets/images/gifs/static-images/gif-static-${i}-${j}.jpg`;
            };

            img.onmouseover = function () {
                this.src = `assets/images/gifs/gif-${i}-${j}.gif`;
            };
        }
    }
}

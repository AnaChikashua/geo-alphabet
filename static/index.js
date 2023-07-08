// adapted from http://www.williammalone.com/articles/create-html5-canvas-javascript-drawing-app/
// for mobile & touch https://stackoverflow.com/questions/17656292/html5-canvas-support-in-mobile-phone-browser

let context = {};
let paint
let clickX = {}
let clickY = {}
let clickDrag = {}

let width_height = {
    letter_canvas: [400, 400],
    digit_canvas: [200, 200],
    word_canvas: [800, 300]
}

function startCanvas(id) {
    const canvas = document.getElementById(id)
    context[id] = canvas.getContext("2d")
    context[id].strokeStyle = "#000000"
    context[id].lineJoin = "round"
    context[id].lineWidth = 10
    context[id].fillStyle = "white";
    context[id].fillRect(0, 0, width_height[id][0], width_height[id][1]);

    canvas.addEventListener("touchstart", function (e) {
        var touch = e.touches[0]
        var mouseEvent = new MouseEvent("mousedown", {
            clientX: touch.clientX,
            clientY: touch.clientY,
        })
        canvas.dispatchEvent(mouseEvent)
    })

    canvas.addEventListener("touchmove", function (e) {
        var touch = e.touches[0]
        var mouseEvent = new MouseEvent("mousemove", {
            clientX: touch.clientX,
            clientY: touch.clientY,
        })
        canvas.dispatchEvent(mouseEvent)
    })

    canvas.addEventListener("touchend", function (e) {
        var mouseEvent = new MouseEvent("mouseup")
        canvas.dispatchEvent(mouseEvent)
    })

    $('#' + id).mousedown(function (e) {
        paint = true
        addClick(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false)
        drawCanvas()
    })

    $('#' + id).mousemove(function (e) {
        if (paint) {
            addClick(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true)
            drawCanvas()
        }
    })

    $('#' + id).mouseup(function (e) {
        paint = false
        drawCanvas()
    })

    $('#' + id).mouseleave(function (e) {
        paint = false
    })


    function addClick(x, y, dragging) {
        if (!clickX[id]) {
            clickX[id] = [x]
        } else {
            clickX[id].push(x)
        }

        if (!clickY[id]) {
            clickY[id] = [y]
        } else {
            clickY[id].push(y)
        }

        if (!clickDrag[id]) {
            clickDrag[id] = [dragging]
        } else {
            clickDrag[id].push(dragging)
        }

    }

    function clearCanvas() {
        context[id].clearRect(0, 0, width_height[id][0], width_height[id][1])
        context[id].fillStyle = "white";
        context[id].fillRect(0, 0, width_height[id][0], width_height[id][1]);
    }

    function resetCanvas() {
        clickX[id] = []
        clickY[id] = []
        clickDrag[id] = []
        clearCanvas()
    }

    function drawCanvas() {
        clearCanvas()
        for (let i = 0; i < clickX[id].length; i++) {
            context[id].beginPath()
            if (clickDrag[id][i] && i) {
                context[id].moveTo(clickX[id][i - 1], clickY[id][i - 1])
            } else {
                context[id].moveTo(clickX[id][i] - 1, clickY[id][i])
            }
            context[id].lineTo(clickX[id][i], clickY[id][i])
            context[id].closePath()
            context[id].stroke()
        }
    }

    function getPixels() {
        let rawPixels = context[id].getImageData(0, 0, width_height[id][0], width_height[id][1]).data
        let _pixels = []
        let pixels = []
        console.log(rawPixels)
        for (i = 0; i < rawPixels.length; i += 4) {
            _pixels.push(rawPixels[i + 3])
        }
        console.log(_pixels)
        for (i = 0; i < _pixels.length; i += 800) {
            for (j = 0; j < width_height[id][0]; j += 4) {
                pixels.push(_pixels[i + j])
            }
        }
        console.log(pixels)
        return pixels
    }

    function addDataAction() {
        let pixels = getPixels()
        document.getElementById("pixels").value = pixels
        document.getElementById("add-data-form").submit()
    }


    async function practiceAction(id, canvas_id) {
        const canvas = document.getElementById(canvas_id);
        canvas.toBlob((blob) => {
            const file = new File([blob], "mycanvas.png");
            const dT = new DataTransfer();
            dT.items.add(file);
            document.getElementById("file_" + id).files = dT.files;
            document.getElementById(id + "_form").submit()
        });
    }

    return {
        resetCanvas: resetCanvas,
        practiceAction: practiceAction
    };

}

function performPost() {
    console.log($(this).text())
    $.ajax({
        url: '/check_digit',
        method: 'POST',
        contentType: 'application/json',
        data: {
            type: $('#type_letter_canvas').val(),
            file: $('#file_pixels_letter_canvas').val()
        },
        success: (function (response) {
            console.log(response.result)
            $('#result').text(response.result).show()
        })

    })
        .done(function (data) {
            console.log(data.result)
            $('#result').text(data.result).show()
        })

}

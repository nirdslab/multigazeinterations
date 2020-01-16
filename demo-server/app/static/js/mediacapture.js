//Get camera video
var img = "";
var isPlaying = false;
var gotMetadata = false;
var videoElement = document.getElementById("myVideo");
let drawCanvas = document.createElement('canvas');
let imageCanvas = document.createElement('canvas');
var apiUrl = window.location.origin + '/frame-process';
var uploadWidth = 1280;
document.body.appendChild(drawCanvas);
let drawCtx = drawCanvas.getContext("2d");
let imageCtx = imageCanvas.getContext("2d");


const constraints = {
    audio: false,
    video: {
        width: {min: 640, ideal: 1280, max: 1920},
        height: {min: 480, ideal: 720, max: 1080}
    }
};

function show_image(img){
    var ctx = document.querySelector("#canvasOutput").getContext("2d");

    var height = img.length;
    var width = img[0].length;

    ctx.canvas.height = height;
    ctx.canvas.width = width;

    var h = ctx.canvas.height;
    var w = ctx.canvas.width;

    var imgData = ctx.getImageData(0, 0, w, h);
    var data = imgData.data;  // the array of RGBA values

    for(var i = 0; i < height; i++) {
        for(var j = 0; j < width; j++) {
            var s = 4 * i * w + 4 * j;  // calculate the index in the array
            var x = img[i][j];  // the RGB values

            avg = (x[0] + x[1] + x[2]) / 3;
            data[s] = avg;
            data[s + 1] = avg;
            data[s + 2] = avg;

            // Check code
            //data[s] = x[0];
            //data[s + 1] = x[1];
            //data[s + 2] = x[2];
            data[s + 3] = 255;  // fully opaque
        }
    }

    ctx.putImageData(imgData, 0, 0);
    // grayScale(context, canvas);
}

function postFile(file) {

    //Set options as form data
    let formdata = new FormData();
    formdata.append("image", file);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', apiUrl, true);
    xhr.onload = function () {
        if (this.status === 200) {
            img = JSON.parse(this.response);
            show_image(img);

            //Save and send the next image
            imageCtx.drawImage(videoElement, 0, 0, videoElement.videoWidth, videoElement.videoHeight, 0, 0, uploadWidth, uploadWidth * (videoElement.videoHeight / videoElement.videoWidth));
            imageCanvas.toBlob(postFile, 'image/jpeg');
        }
        else {
            console.error(xhr);
        }
    };
    xhr.send(formdata);
}

function startObjectDetection() {

    // console.log("starting object detection");
    //
    // //Set canvas sizes base don input video
    // drawCanvas.width = videoElement.videoWidth;
    // drawCanvas.height = videoElement.videoHeight;


    imageCanvas.width = uploadWidth;
    imageCanvas.height = uploadWidth * (videoElement.videoHeight / videoElement.videoWidth);

    imageCtx.drawImage(videoElement, 0, 0, videoElement.videoWidth, videoElement.videoHeight, 0, 0, uploadWidth, uploadWidth * (videoElement.videoHeight / videoElement.videoWidth));
    imageCanvas.toBlob(postFile, 'image/jpeg');

    // imageCanvas.width = uploadWidth;
    // imageCanvas.height = uploadWidth * (videoElement.videoHeight / videoElement.videoWidth);
    //
    // //Some styles for the drawcanvas
    // // drawCtx.lineWidth = 4;
    // // drawCtx.strokeStyle = "cyan";
    // // drawCtx.font = "20px Verdana";
    // // drawCtx.fillStyle = "cyan";
    //
    // //Save and send the first image
    // imageCtx.drawImage(videoElement, 0, 0, videoElement.videoWidth, videoElement.videoHeight, 0, 0, uploadWidth, uploadWidth * (videoElement.videoHeight / videoElement.videoWidth));
    // imageCanvas.toBlob(postFile, 'image/jpeg');

}

navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        videoElement.srcObject = stream;
        console.log("Got local user video");

    })
    .catch(err => {
        console.log('navigator.getUserMedia error: ', err)
    });

videoElement.onplaying = () => {
    isPlaying = true;
    if(gotMetadata){
        startObjectDetection();
    }
};

videoElement.onloadedmetadata = () => {
    gotMetadata = true;
    if (isPlaying){
        startObjectDetection();
    }
};

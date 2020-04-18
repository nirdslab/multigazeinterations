onOpenCvReady = function(){}

async function bind(){

    const video = document.getElementById('video');

    const canvas = document.getElementById('output');

    const context = canvas.getContext('2d', {alpha: false});

    const infoP = document.getElementById("info");

    const dataP = document.getElementById("data");

    const fpsP = document.getElementById("fps");

    video.srcObject = await navigator.mediaDevices.getUserMedia({
        audio: false,
        video: {facingMode: 'user'}
    });
    await video.play();

    const videoHeight = video.videoHeight
    const videoWidth = video.videoWidth;

    let posenetConfig = {
        architecture: 'MobileNetV1',
        outputStride: 16,
        inputResolution: { width: videoWidth, height: videoHeight },
        multiplier: 0.75,
        quantBytes: 2
    };
    const net = await posenet.load(posenetConfig);

    infoP.append("Posenet loaded \n");

    const gazenet = await tf.loadGraphModel('/static/estimation-regularization/model.json');

    infoP.append('Gazenet loaded \n');

    async function startDetection(){

        canvas.height = video.videoHeight;
        canvas.width = video.videoWidth;

        await poseDetectionFrame();

    }

    async function poseDetectionFrame(){
        let startTime = new Date();

        frame = tf.browser.fromPixels(video)

        const poses = await net.estimateMultiplePoses(frame, {
            flipHorizontal: false,
            maxDetections: 5,
            scoreThreshold: 0.5,
            nmsRadius: 20
        });

        tf.browser.toPixels(frame, canvas);

        if (poses.length > 0) {

            // context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

            let frameData = Uint8ClampedArray.from(await frame.data());
            let frameShape = frame.shape;

            // draw_tensor(frameData, frameShape, context);

            let imageSlices = new Array();

            for (let i = 0; i < poses.length; i++) {
                let pose = poses[i];

                context.strokeStyle = "#ffffff"

                context.beginPath();
                context.arc(pose.keypoints[1].position.x, pose.keypoints[1].position.y, 5, 0, 2 * Math.PI);
                context.stroke();
                imageSlices.push(sliceImage(frame, pose.keypoints[1].position.x, pose.keypoints[1].position.x));

                context.beginPath();
                context.arc(pose.keypoints[2].position.x, pose.keypoints[2].position.y, 5, 0, 2 * Math.PI);
                context.stroke();
                imageSlices.push(sliceImage(frame, pose.keypoints[2].position.x, pose.keypoints[2].position.x));


            }

            let imageSliceTensors = tf.stack(imageSlices).toFloat();

            const gazenetOut = gazenet.predict(imageSliceTensors, {verbose: true});

            // console.log(gazenetOut);

            const predictions = await gazenetOut[2].data();

            dataP.innerText = JSON.stringify(predictions);

            imageSliceTensors.dispose();

        }
        let endTime = new Date();

        let fps = 1000/ (endTime.getTime() - startTime.getTime());

         fpsP.innerHTML = "FPS : " + fps;

        window.requestAnimationFrame(poseDetectionFrame);

    }

    await startDetection();

}

function draw_tensor(tensorData, tensorShape, context) {

    //get the tensor shape
    const [height, width] = tensorShape;
    //create a buffer array
    const buffer = new Uint8ClampedArray(width * height * 4);

    const imageData = new ImageData(width, height);

    //map the values to the buffer
    let i = 0;
    for(let y = 0; y < height; y++) {

        for(let x = 0; x < width; x++) {

            let pos = (y * width + x) * 4;      // position in buffer based on x and y
            buffer[pos  ] = tensorData[i]             // some R value [0, 255]
            buffer[pos+1] = tensorData[i+1]           // some G value
            buffer[pos+2] = tensorData[i+2]           // some B value
            buffer[pos+3] = 255;                // set alpha channel
            i+=3
        }
    }
    //set the buffer to the image data
    imageData.data.set(buffer)
    //show the image on canvas
    context.putImageData(imageData, 0, 0);
}


function sliceImage(tensor, centrex, centrey){
    const startx = Math.min(Math.floor(Math.max(centrex - 18, 0)), 200);
    const starty = Math.min(Math.floor(Math.max(centrey - 30, 0)), 550);
    return frame.slice([startx, starty, 0], [36, 60, 1]);
}


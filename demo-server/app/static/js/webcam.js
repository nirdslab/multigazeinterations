onOpenCvReady = function(){}

async function bind(){

    const video = document.getElementById('video');

    const canvas = document.getElementById('output');

    const context = canvas.getContext('2d');

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

    console.log(net);

    async function startDetection(){

        canvas.height = video.videoHeight;
        canvas.width = video.videoWidth;

        await poseDetectionFrame();

    }

    async function poseDetectionFrame(){

        frame = tf.browser.fromPixels(video)

        const poses = await net.estimateMultiplePoses(frame, {
            flipHorizontal: false,
            maxDetections: 5,
            scoreThreshold: 0.5,
            nmsRadius: 20
        });

        context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);


        for(i =0; i < poses.length; i++){
            let  pose = poses[i];

            context.strokeStyle = "#ffffff"

            context.beginPath();
            context.arc(pose.keypoints[1].position.x, pose.keypoints[1].position.y, 5, 0, 2 * Math.PI);
            context.stroke();

            context.beginPath();
            context.arc(pose.keypoints[2].position.x, pose.keypoints[2].position.y, 5, 0, 2 * Math.PI);
            context.stroke();
        }

        window.requestAnimationFrame(poseDetectionFrame);

    }

    await startDetection();

}


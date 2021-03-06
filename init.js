$(document).ready(function() {
  run()
})
    
async function run() {
  // load the models
  await faceapi.loadMtcnnModel('/')
  await faceapi.loadFaceRecognitionModel('/')
  
  // try to access users webcam and stream the images
  // to the video element
  const videoEl = document.getElementById('inputVideo')
  navigator.getUserMedia(
    { video: {} },
    stream => videoEl.srcObject = stream,
    err => console.error(err)
  )
}
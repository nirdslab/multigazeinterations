# Multi Gaze Interactions - Docs

Multi Gaze Interactions provides multi user gaze tracking using any common camera in real time. The application includes
a pretained model trained using [Columbia Gaze Dataset](http://www.cs.columbia.edu/CAVE/databases/columbia_gaze)
for gaze prediction and Haar cascade filters for face and facial feature detection.

Source : [https://github.com/nirdslab/multigazeinterations](https://github.com/nirdslab/multigazeinterations)


## Online Demo

## Desktop Demo Application

## Running from Source
#### Requirements: 
  * Python 3.7 or higher
  * Pip 19.3 or higher
  
#### Clone the source

```shell 
git clone https://github.com/nirdslab/multigazeinterations.git
```

#### Install Dependencies
```shell 
pip3 install -r requirements.txt 
```

#### Runnning Application

```shell
# Realtime Gaze tracking with webcam (or equivalent)
python realtime.py 
```

```shell 
# Testing gaze tracking on images
python image_test.py <image path>
# Example
python image_test.py test.jpg
```

## API Usage


## About Us

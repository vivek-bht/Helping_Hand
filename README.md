
# ParaConnect: A Hands-Free Computer Navigation System

## Introduction
ParaConnect is an innovative project aimed at transforming computer navigation for individuals with physical disabilities, such as those who are paralyzed, have experienced accidents, or suffer from repetitive strain injuries like carpal tunnel syndrome. This system integrates advanced computer vision and machine learning technologies to create a user-friendly interface that allows individuals to control their computers using eye blinks, winks, and voice commands.

## Project Motivation
The motivation behind ParaConnect is to bridge the accessibility gap by creating a software-based solution that allows hands-free computer navigation. By leveraging advanced technologies, this project aims to provide a seamless and efficient way for individuals with physical disabilities to interact with their computers, enhancing their quality of life by enabling them to perform tasks that would otherwise require manual dexterity.



## Features
- ### Cursor Movement: 
    Achieved using a simplistic angle and distance model with the OpenCV Python library. The cursor moves according to the angle created by the line joining the nose tip with the center of the circle and the horizontal line. The nose tip is identified using Google's Mediapipe library along with the system's webcam. The motion is controlled by the pivotal movement of the head, requiring minimal head movement.

- ### Wink and Blink Detection: 
    Implemented by training a convolutional neural network, resulting in more effective detection than calculating eye aspect ratio values using Mediapipe. Gestures included are:

    Left wink: Click\
    Right wink: Right click\
    Holding left wink for more than a second: Double click\
    Squinting eyes: Toggles scroll mode on and off

- ### Virtual Keyboard: 
    Created using Kivy technology. It highlights keys according to the angle and distance of the nose from the center of the circle. Keys and sectors are highlighted along the way and can be clicked by holding a left wink. The pressing of keys is achieved using the PyAutoGUI library.

- ### Voice Mode: 
    Accessible by clicking a button in the Kivy window. Voice mode allows users who cannot wink to give commands like click, double click, right click, scroll up or down just by their voice. If connected to the internet, users can also browse sites by saying commands like "open YouTube" or "open Google". The application includes Gemini AI Assistant, which can be accessed using the Open AI assistant command and can answer questions. It also includes a typing mode for typing via voice and commands like shutdown, sleep, and other system commands.

- ### Multiprocessing: 
    All processes run in parallel, sharing information through a multiprocessing manager dictionary. This ensures smooth operation without disturbances between processes and effective use of the system's resources.


## Installation

Copy code:

```bash
  git clone https://github.com/yourusername/paraconnect.git
```
Navigate to the project directory:
```bash
  cd paraConnect
```
To install the required dependencies copy code:
```bash
  pip install -r requirements.txt
```
To install the required dependencies copy code:
```bash
  pip install -r requirements.txt
```
Now run index.py and follow the on-screen instructions which will further guide you on how to operate the application. 
That's it! you will not be able to operate your system without using your hands :)
## License
This project is licensed under the MIT License. See the [MIT LICENSE](https://choosealicense.com/licenses/mit/)  file for more details.



## Contributing

We welcome contributions to ParaConnect! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to our coding standards and includes appropriate tests.


# FlappyBrainTeam

## Summary

People suffering from permanent or temporary mobility issues can be limited when trying to participate with today’s conventional entertainment measures. Brain Computer-interfaces can play a role in broadening access for those requiring alternative means outside of typical muscle control.

Two BioAmp EXG Pill sources are used (beside each eye and above and below one eye). The sources are fed in through an Arduino microcontroller. A series of python code is used to run the application:

#### Testing.py:

Used to initiate the application. It calls the required functions from the other files and facilitates the data pipeline from the devices into usable logical code for mouse movement; data is also saved externally for machine learning training.

#### Processing.py:

Used to pull data from the end devices and transform into a useful language. Raw data is currently used to determine the direction the user indicates through EOG artifacts. Data is transformed into a frequency and used to determine when an activity threshold is reached.

#### Control.py:

Used to implement the action of the mouse. It is continuously called by Testing.py. The code actions the mouse movement based on the provided direction outputted from the processing class.

#### CSVgen.py and Training.py:

These classes are used for future application improvement. Both raw and transformed data is written to csv whenever the program is run. The data is manipulated in the Training class which uses TensorFlow to build a machine learning model.

#### Future improvements:

Use TensorFlow to improve recognition of the inputs. Use EEG data rather than EOG artifacts.

#### Video tutorial

[![Watch the video](https://q5n8c8q9.rocketcdn.me/wp-content/uploads/2019/09/YouTube-thumbnail-size-guide-best-practices-top-examples.png.webp)](https://youtu.be/8hNw2gWGpAQ)

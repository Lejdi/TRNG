# TRNG

True random number generator which uses microphone as a source of entrophy.  
The program first takes sound recording providing random bits in number dependend of `recSize` value (default: 100000).  
When random bits are ready, user is prompted to enter the word size.  
In the end user can display entrophy calculated by algorithm and display words histogram.

#### Requirements

To use TRNG you need the following libraries:
 - [numpy](https://pypi.org/project/numpy/)
 - [matplotlib](https://pypi.org/project/matplotlib/)
 - [sounddevice](https://pypi.org/project/sounddevice/)

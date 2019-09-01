# Controller for Meccanoid servos.


This is based on the Arduino C program MeccaBrain.cpp that can be found here: http://www.meccano.com/meccanoid-opensource

I wanted to be able to use a RaspberryPi and Python so cloned the code
and made it more pythonic and more OO.

There are some unit tests in the Tests folder and integration tests in each of the components.
This organization was used because I wanted to be able to run
unit tests on my mac but integration tests needed to be run on the
actual raspberry pi since that was where the HW was.
Feel free to criticize as long as you provide a suggestion for improvement
along with that. :-)

You can run the application with run_app.sh.
It will wiggle the servos and change their colors.  It is really just a
sample so you can start using the library.


#### KEYWORDS: meccano smart module meccabrain servo python raspberry pi

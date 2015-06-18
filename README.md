# img2ascii

inspired by [jzlikewei/img2ascii](https://github.com/jzlikewei/img2ascii)

###Use
run.py: curses interface to show ascii graph

Commands are shown in curses interface.

* o : open image file
* +/- : zoom in/out the ascii graph in shown window
* hjkl/arrow keys : move around
* r : restore ascii graph to original place
* c : clean shown window
* d : dump ascii graph in current shown size
* q : quit

Tested with python 3.4 on Linux/Mac.

Don't know why on Mac calling curses window.box will crash python (homebrew version). It's prettier with the box...

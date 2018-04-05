# watermark-script
Python script that pastes selected watermark to pictures.


Features:
- user can select a file with watermark
- user can select file or directory with pictures
- user can select watermark mode: central or tile
- user can select output folder
- user can exit the script at any step
- script validates the path to files and selects only images from folder
- watermark is resized accordingly to the source image
- image with watermark is saved with the same extension and modified filename
- script can be called with arguments

Call examples:
> python Watermark.py -s C:\User\images\ -w C:\User\images\watermark.png -o C:\User\images\result\ -t

> python Watermark.py -s images\test.jpg -w watermark.png -o .\ -c

All arguments are optional and script can be called without them. In this case, user will be prompted to enter necessary info by steps.
Use -h key to see help about arguments.

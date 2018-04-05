import os
from PIL import Image
import argparse


# list of extensions to check if file is image
ext = ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff', '.webp']


def selectWm():
    while True:
        wmSource = input("Please enter path to the watermark file >>> ")
        if os.path.exists(wmSource) & os.path.isfile(wmSource):
            orig = Image.open(wmSource)
            wm = orig.copy()
            return wm
        elif wmSource == 'x':
            quit()
        else:
            print('Error: invalid path')
            continue


def isImage(file):
    for i in ext:
        if os.path.splitext(file)[1].lower() == i:
            return True
    return False


def getImages(path):
    pics = []
    if os.path.isfile(path):
        if isImage(path):
            pics.append(os.path.basename(path))
        else:
            print('Error: not an image file')
            selectSource()
        path = os.path.abspath(path)
        path = os.path.dirname(path) + '/'
        return pics, path
    elif os.path.isdir(path):
        pics = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) & isImage(f)]
        if len(pics) == 0:
            print('Error: no images in folder')
            selectSource()
        return pics, path


def selectSource():
    while True:
        imSource = input("Please enter path to the image file or a folder >>> ")
        if os.path.exists(imSource):
            pics, path = getImages(imSource)
            return pics, path
        elif imSource == 'x':
            quit()
        else:
            print('Error: invalid path')
            continue


def selectOut():
    while True:
        outpath = input("Please enter path to the output folder >>> ")
        if os.path.exists(outpath):
            return os.path.abspath(outpath) + '/'
        elif outpath == 'x':
            quit()
        else:
            print('Error: invalid path')
            continue


def central(pics, wm, filepath, outpath):
    for n in pics:
        im = Image.open(filepath + n)
        imWidth, imHeight = im.size
        wmWidth = (int(imWidth * 0.85))
        wmHeight = (int(wm.size[1] * (wmWidth / wm.size[0])))
        wmres = wm.resize((wmWidth, wmHeight))
        im.paste(wmres, (int(imWidth / 2) - int(wmWidth / 2), int(imHeight / 2) - int(wmHeight / 2)), wmres)
        newname = os.path.splitext(outpath + n)[0] + '_wm' + os.path.splitext(filepath + n)[1]
        im.save(newname)
        print(newname)


def tile(pics, wm, filepath, outpath):
    wmrot = wm.rotate(45, expand=True)
    for n in pics:
        im = Image.open(filepath + n)
        imWidth, imHeight = im.size
        wmWidth = (int(imWidth * 0.20))
        wmHeight = (int(wmrot.size[1] * (wmWidth / wmrot.size[0])))
        wmres = wmrot.resize((wmWidth, wmHeight))
        for w in range(0, imWidth, wmWidth):
            for h in range(0, imHeight, wmHeight):
                im.paste(wmres, (w, h), wmres)
        newname = os.path.splitext(outpath + n)[0] + '_wm' + os.path.splitext(filepath + n)[1]
        im.save(newname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help='enter path to source image file or folder', default='')
    parser.add_argument('-w', '--watermark', help='enter path to watermark file', default='')
    parser.add_argument('-o', '--output', help='enter path to output folder', default='')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--central", action="store_true", help='place watermark in center')
    group.add_argument("-t", "--tile", action="store_true", help='tile watermark')
    args = parser.parse_args()

    path = ''
    pictures = []
    output = ''
    mode = ''
    wmark = Image.new('RGB', (0, 0))

    # check path to source
    if (args.source != '') & os.path.exists(args.source):
        pictures, path = getImages(args.source)
    else:
        print('Welcome to the Watermark Script! Follow the instructions or press x to exit.')
        pictures, path = selectSource()
        print(path)
        print(pictures)

    # check path to watermark
    if (args.watermark != '') & os.path.exists(args.watermark) & isImage(args.watermark):
        if os.path.isfile(args.watermark) & isImage(args.watermark):
            wmark = Image.open(args.watermark).convert("RGBA").copy()
    else:
        wmark = selectWm()

    # check path to output folder
    if (args.output != '') & os.path.exists(args.output):
        output = os.path.abspath(output) + '/' + args.output
    else:
        output = selectOut()

    # check watermark paste mode
    if args.central:
        mode = 'central'
    elif args.tile:
        mode = 'tile'
    else:
        mode = input("Select watermark mode: central or tile >>> ")

    if mode == 'central':
        central(pictures, wmark, path, output)
    elif mode == 'tile':
        tile(pictures, wmark, path, output)
    elif mode == 'x':
        quit()
    else:
        print('Error: not a valid mode')

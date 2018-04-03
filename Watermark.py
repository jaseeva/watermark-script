import os
from PIL import Image


# list of extensions to check if file is image
ext = ['.png', '.jpg', '.jpeg', '.bmp']


def selectWm():
    while True:
        wmSource = input("Please enter path to the watermark file >>> ")
        if os.path.exists(wmSource) & os.path.isfile(wmSource):
            orig = Image.open(wmSource).convert("RGBA")
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


def selectSource():
    while True:
        pics = []
        imSource = input("Please enter path to the image file or a folder >>> ")
        if os.path.exists(imSource):
            if os.path.isfile(imSource):
                if isImage(imSource):
                    pics.append(os.path.basename(imSource))
                else:
                    print('Error: not an image file')
                    continue
                imSource = os.path.dirname(imSource) + '/'
                return pics, imSource
            elif os.path.isdir(imSource):
                pics = [f for f in os.listdir(imSource) if os.path.isfile(os.path.join(imSource, f)) & isImage(f)]
                if len(pics) == 0:
                    print('Error: no images in folder')
                    continue
                return pics, imSource
        elif imSource == 'x':
            quit()
        else:
            print('Error: invalid path')
            continue


def central(pics, wm, filepath):
    for n in pics:
        im = Image.open(filepath + n)
        imWidth, imHeight = im.size
        wmWidth = (int(imWidth * 0.85))
        wmHeight = (int(wm.size[1] * (wmWidth / wm.size[0])))
        wmres = wm.resize((wmWidth, wmHeight))
        im.paste(wmres, (int(imWidth / 2) - int(wmWidth / 2), int(imHeight / 2) - int(wmHeight / 2)), wmres)
        newname = os.path.splitext(filepath + n)[0] + '_wm' + os.path.splitext(filepath + n)[1]
        im.save(newname)


def tile(pics, wm, filepath):
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
        newname = os.path.splitext(filepath + n)[0] + '_wm' + os.path.splitext(filepath + n)[1]
        im.save(newname)


if __name__ == "__main__":
    print('Welcome to the Watermark Script! Follow the instructions or press x to exit.')
    wmark = selectWm()
    pictures, path = selectSource()
    mode = input("Select watermark mode: central or tile >>> ")
    if mode == 'central':
        central(pictures, wmark, path)
    elif mode == 'tile':
        tile(pictures, wmark, path)
    elif mode == 'x':
        quit()
    else:
        print('Error: not a valid mode')

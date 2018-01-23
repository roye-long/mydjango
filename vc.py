from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter

import random
import numpy as np
#matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import scipy.signal as signal
import sys
import math
import time

def denoise(image, noiseSize, rangeSize):
    (width, high) = image.size
    blackPoints = []
    for w in xrange(width):
        for h in xrange(high):
            if(image.getpixel((w, h)) == 0):
                blackPoints.append((w, h))
                
    groups = scanBlackGroup(blackPoints, image.size, rangeSize)
    imgAccess = image.load()

    noise = []
    
    for group in groups:
        #print group
        #print "group length: ",len(group)
        if(len(group) <= noiseSize):
            noise.append(group)
            for pix in group:
                #print "cover: ",pix[0],pix[1]
                imgAccess[pix[0], pix[1]] = 1
    return (image, noise)

def scanBlackGroup(blackPoints, picSize, rangeSize):
    scanned = set()
    needScan = []
    group = []
    groups = []
    bp = set(blackPoints)
    for blackPoint in blackPoints:
        #print "blackPoint: ",blackPoint
        if(blackPoint not in scanned):
            scanned.add(blackPoint)
            group.append(blackPoint)
            needScan.extend((genAroundPoints(blackPoint, picSize, rangeSize) - scanned) & bp)
            #print "first scan around: ", group
            while(len(needScan) > 0):
                scan = needScan.pop()
                #print "scan: ",scan
                group.append(scan)
                scanned.add(scan)
                needScan.extend(((genAroundPoints(scan, picSize, rangeSize) - scanned) & bp) - set(needScan))
            if(len(group) > 0):
                groups.append(group)
            group = []
    return groups

def genAroundPoints(point, picSize, rangeSize):
    #print "point: ",point
    (width, high) = picSize
    points = set()
    for x in xrange(point[0] - rangeSize, point[0] + rangeSize + 1):
        for y in xrange(point[1] - rangeSize, point[1] + rangeSize + 1):

            #print "x,y: ",x,y
            
            if(x >= 0 and x < picSize[0] and y >= 0 and y < picSize[1]):
                if(x == point[0] and y == point[1]):
                    continue
                else:
                    points.add((x, y))
    #print "from point ",point,"genPoints: ",points
    return points


def shape2(image):
    (width, high) = image.size
    img = Image.new('L', (width, high), "white")
    #img = image.crop((0,0,width - 1,high - 1))
    pixels = img.load()
    shapes = scanShape2(image)
    #print "shapes: ",shapes
    for (w,h) in shapes:
        #print "shape: ",(w,h)
        pixels[w, h] = 1
    return img.point(pointTable(140), '1')

def scanShape2(image):
    (width, high) = image.size
    shapes = []
    scanned = set()
    scanning = []
    
    for w in xrange(width):
        for h in xrange(high):
            index = (w, h)
            if(index not in scanned):
                scanned.add(index)
                if(image.getpixel((w, h)) == 0):
                    shapes.append((w, h))
                    pixs = list(set(scanAroundBlackPoint(image, w, h, scanned)) - scanned)
                    if(len(pixs) > 0):
                        shapes.extend(pixs)
                    scanning.extend(pixs)
                    while(len(scanning) != 0):
                        #print len(scanning)
                        (x, y) = scanning.pop(0)
                        scanned.add((x, y))
                        pixs = list(set(scanAroundBlackPoint(image, w, h, scanned)) - scanned)
                        if(len(pixs) > 0):
                            shapes.extend(pixs)
                        scanning.extend(pixs)
                scanning = []
    return shapes

def shape(image, noisThreshold):
    (width, high) = image.size
    img = Image.new('L', (width, high), "white")
    pixels = img.load()
    shapes = scanShape(image)
    #print shapes
    for shape in shapes:
        #print "shape: ",shape
        if(len(shape) < noisThreshold):
            for (w, h) in shape:
                pixels[w, h] = 0
    img.point(pointTable(140), '1')
    return img
    
def scanShape(image):
    (width, high) = image.size
    shapes = []
    shape = []
    scanned = set()
    scanning = []
    
    for w in xrange(width):
        for h in xrange(high):
            index = (w, h)
            if(index not in scanned):
                scanned.add(index)
                if(image.getpixel((w, h)) == 0):
                    shape.append((w, h))
                    pixs = list(set(scanAroundBlackPoint(image, w, h, scanned)) - scanned)
                    shape.extend(pixs)
                    scanning.extend(pixs)
                    while(len(scanning) != 0):
                        print len(scanning)
                        (x, y) = scanning.pop(0)
                        scanned.add((x, y))
                        pixs = list(set(scanAroundBlackPoint(image, w, h, scanned)) - scanned)
                        shape.extend(pixs)
                        scanning.extend(pixs)
                if(len(shape) > 0):
                    shapes.append(shape)
                shape = []
                scanning = []
    return shapes

def scanAroundBlackPoint(image, w, h, scanned):
    (width, high) = image.size
    blackPoints = []
    for x in xrange(w - 1,w + 2):
        for y in xrange(h - 1, h + 2):
            if(w + x >= 0 and h + y >= 0 and x < width and y < high and x <> y):
                #print "x,y = ",x, ",",y
                if((x, y) not in scanned and image.getpixel((x, y)) == 0):
                    blackPoints.append((x, y))
                scanned.add((x, y))
    return blackPoints
                    
def effectiveRange(image):
    
    (width, high) = image.size
    
    lefter = (False, width - 1)
    righter = (False, 0)
    upper = (False, 0)
    lower = (False, high - 1)
    
    for i in xrange(width):
        for j in xrange(high):
            if(not lefter[0]):
                #print "i: ",i,"j: ",j
                if(image.getpixel((i, j)) == 0):
                    lefter = (True, i)
            if(not righter[0]):
                #print "width - i - 1: ",width - i - 1,"j: ",j
                if(image.getpixel((width - i - 1, j)) == 0):
                    righter = (True, width - i - 1)
            if(lefter[0] and righter[0]):
                break
        if(upper[0] and lower[0]):
            break
    
    for i in xrange(high):
        for j in xrange(width):
            if(not upper[0]):
                #print "i: ",i,"j: ",j
                if(image.getpixel((j, i)) == 0):
                    upper = (True, i)
            if(not lower[0]):
                #print "high - i - 1: ",high - i - 1,"j: ",j
                if(image.getpixel((j, high - i - 1)) == 0):
                    lower = (True, high - i - 1)
            if(upper[0] and lower[0]):
                break
        if(upper[0] and lower[0]):
            break
    if(not lefter[0]):
        lefter = (False, -1)
    if(not righter[0]):
        righter = (False, -1)
    if(not upper[0]):
        upper = (False, -1)
    if(not lower[0]):
        lower = (False, -1)
    return (lefter[1], upper[1], righter[1], lower[1])

def effectiveRange2(image, size):
    
    (width, high) = size
    
    lefter = (False, width - 1)
    righter = (False, 0)
    upper = (False, 0)
    lower = (False, high - 1)
    
    for i in xrange(width):
        for j in xrange(high):
            if(not lefter[0]):
                #print "i: ",i,"j: ",j
                if(image[j][i] == 0):
                    lefter = (True, i)
            if(not righter[0]):
                #print "width - i - 1: ",width - i - 1,"j: ",j
                if(image[j][width - i - 1] == 0):
                    righter = (True, width - i - 1)
            if(lefter[0] and righter[0]):
                break
        if(upper[0] and lower[0]):
            break
    
    for i in xrange(high):
        for j in xrange(width):
            if(not upper[0]):
                #print "i: ",i,"j: ",j
                if(image[i][j] == 0):
                    upper = (True, i)
            if(not lower[0]):
                #print "high - i - 1: ",high - i - 1,"j: ",j
                if(image[high - i - 1][j] == 0):
                    lower = (True, high - i - 1)
            if(upper[0] and lower[0]):
                break
        if(upper[0] and lower[0]):
            break
    if(not lefter[0]):
        lefter = (False, -1)
    if(not righter[0]):
        righter = (False, -1)
    if(not upper[0]):
        upper = (False, -1)
    if(not lower[0]):
        lower = (False, -1)
    return (lefter[1], upper[1], righter[1], lower[1])

def pointTable(threshold = 140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0) 
        else:
            table.append(1)
    return table

def rotate2(pic):
    (width, high) = pic.size
    
    img = Image.new('L', (width, high), "white")
    pixels = img.load()
    
    (lefter, upper, righter, lower) = effectiveRange(pic)

    print "effectiveRange",(lefter, upper, righter, lower)
    
    scanNum = (lower - upper) / 2

    if(scanNum == 0):
        return pic.crop((0,0,width - 1,high - 1))
    
    start = scanNum
    
    for h in xrange(high):
        if(scanNum > 0):
            for w in xrange(scanNum):
                if(pic.getpixel((w, h)) == 0):
                    start = w
                    break
            #print "start: ", start
            for i in xrange(start, width):
                #print "mv pic[",i,",",h,"] to pixels[",i - start,",",h,"]"
                #print pic.getpixel((i, h))
                pixels[i - start, h] = pic.getpixel((i, h)) * 255
            scanNum = scanNum - 1
            start = scanNum
        else:
            for w in xrange(width):
                pixels[w, h] = pic.getpixel((w, h)) * 255
    img.point(pointTable(140), '1')
    return img

def rotate(pic, pixNumber):
    (width, high) = pic.size

    if(pixNumber == 0):
        return pic.crop((0,0,width - 1,high - 1))
    
    img = Image.new('L', (width, high), "white")
    pixels = img.load()
    
    scanNum = pixNumber
    start = scanNum
    
    for h in xrange(high):
        if(scanNum > 0):
            for w in xrange(scanNum):
                if(pic.getpixel((w, h)) == 0):
                    start = w
                    break
            print "start: ", start
            for i in xrange(start, width):
                print "mv pic[",i,",",h,"] to pixels[",i - start,",",h,"]"
                print pic.getpixel((i, h))
                pixels[i - start, h] = pic.getpixel((i, h)) * 255
            scanNum = scanNum - 1
            start = scanNum
        else:
            for w in xrange(width):
                pixels[w, h] = pic.getpixel((w, h)) * 255
    img.point(pointTable(140), '1')
    return img

def easySplit(sourceImage):

    #point = sourceImage.convert('L').point(pointTable(140), '1')
    (pointImage, noises) = denoise(sourceImage.convert('L').point(pointTable(140), '1'), 2, 1)
    copyImage = sourceImage.copy()
    copyImageAccess = copyImage.load()
    for noise in noises:
        for pix in noise:
            #print "cover: ",pix[0],pix[1]
            copyImageAccess[pix[0], pix[1]] = (255,255,255)
    vertical = verticalSplit(copyImage, pointImage, 3)

    #pics = []
    
    #for pic in vertical:
    #    tanPic = tanSplit(sourceImage, pointImage, 30, 2)
    #    if(len(tanPic) > 1):
    #        pics.extend(tanPic)
    #    else:
    #        pics.append(pic)
    return vertical

def split(sourceImage, subImageNumber=4, noisePointThreshold=2, pixThreshold=3):

    (pointImage, noises) = denoise(sourceImage.convert('L').point(pointTable(140), '1'), noisePointThreshold, 1)
    
    copyImage = sourceImage.copy()
    copyImageAccess = copyImage.load()
    for noise in noises:
        for pix in noise:
            #print "cover: ",pix[0],pix[1]
            copyImageAccess[pix[0], pix[1]] = (255,255,255)
    
    images = verticalSplit(copyImage, pointImage, pixThreshold)

    if(len(images) < subImageNumber):
        images = deepSplit(images, subImageNumber, noisePointThreshold)
    return images

def deepSplit(images, targetNum, noisePointThreshold):
    
    (isSplit, avgWidth) = bigImage(images, targetNum)
    subTanImages = []
    for index in xrange(len(images)):
        #images[index].show()
        if(isSplit[index] > 1):
            (pointImage, noises) = denoise(images[index].convert('L').point(pointTable(140), '1'), noisePointThreshold, 1)
            copyImageAccess = images[index].load()
            for noise in noises:
                for pix in noise:
                    #print "cover: ",pix[0],pix[1]
                    copyImageAccess[pix[0], pix[1]] = (255,255,255)
            subTanImages.extend(tanSplit(images[index], pointImage))
        else:
            subTanImages.append(images[index])
    
    if(len(subTanImages) == targetNum):
        return subTanImages
    
    (isSplit, avgWidth) = bigImage(subTanImages, targetNum)
    subForceImages = []
    for index in xrange(len(subTanImages)):
        if(isSplit[index] > 1):
            subForceImages.extend(avgSplit(subTanImages[index], isSplit[index]))
        else:
            subForceImages.append(subTanImages[index])
    return subForceImages

def bigImage(images, targetNum):
    sumWidth = 0
    sizes = []
    for image in images:
        (width, high) = image.size
        sumWidth = sumWidth + width
        sizes.append((width, high))
    avgWidth = sumWidth / targetNum
    details = []
    for index in xrange(len(sizes)):
        (width, high) = sizes[index]
        details.append(int(round(float(width) / float(avgWidth))))
    return (details, avgWidth)

def verticalSplit(sourceImage, pointImage, splitThreshold):
    (width, high) = pointImage.size
    #resize = pointImage.resize((width * 10, high * 10), Image.ANTIALIAS)
    #(width, high) = resize.size
    lines = []
    split = []
    pics = []
    for w in xrange(width):
        isClear = True
        for h in xrange(high):
            isClear = isClear & pointImage.getpixel((w, h))
            if(not isClear):
                break
        if(isClear):
            lines.append(w)
    #print lines,len(lines)
    lines = list(set(xrange(width)) - set(lines))
    #print lines,len(lines)
    if(len(lines) < 1):
        return pics
    head = (0, lines[0])
    for i, el in enumerate(lines[1:]):
        #print i,el
        if(el <> lines[i] + 1 and i - head[0] > splitThreshold - 1):
            split.append((head[1], lines[i]))
            head = (i + 1, el)
        if(i == len(lines) - 2 and i - head[0] > splitThreshold - 1):
            split.append((head[1], el))
    #print split

    margin = 2
    
    for (h, t) in split:
        upper = (False, 0)
        lower = (False, high)
        for i in xrange(high):
            for j in xrange(h, t + 1):
                if(not upper[0]):
                    #print "i: ",i,"j: ",j
                    if(pointImage.getpixel((j, i)) == 0):
                        upper = (True, i)
                if(not lower[0]):
                    #print "high - i - 1: ",high - i - 1,"j: ",j
                    if(pointImage.getpixel((j, high - i - 1)) == 0):
                        lower = (True, high - i - 1)
                if(upper[0] and lower[0]):
                    break
            if(upper[0] and lower[0]):
                if(h > margin - 1):
                    h = h - margin
                if(upper[1] > margin - 1):
                    #upper[1] = upper[1] - 1
                    upper = (upper[0], upper[1] - margin)
                if(t < width - margin - 1):
                    t = t + margin
                if(lower[1] < high - margin - 1):
                    #lower[1] = lower[1] + 1
                    lower = (lower[0], lower[1] + margin)
                pics.append(sourceImage.crop((h, upper[1], t, lower[1])))
                break
    #print pics
    return pics

def avgSplit(image, targetNum):
    (width, high) = image.size
    if(targetNum < 1):
        return [image.crop((0, 0, width - 1, high - 1))]
        
    avg = width / targetNum
    mod = width % targetNum
    wheel = []
    splits = []
    for i in xrange(mod):
        wheel.append(1)
    for i in xrange(targetNum - mod):
        wheel.append(0)
    
    start = 0
    #print "pic: ",pic
    for i in xrange(targetNum):
        if(i == targetNum - 1):
            #print "subPic", start, pic[1], pic[2], pic[3]
            splits.append(image.crop((start, 0, width - 1, high - 1)))
            #print (start, 0, width - 1, high - 1)
            break
        end = start + avg + random.choice(wheel) - 1
        #print "subPic", start, pic[1], end, pic[3]
        splits.append(image.crop((start, 0, end, high - 1)))
        #print (start, 0, end, high - 1)
        start = end + 1
    return splits

def tanSplit(sourceImage, pointImage, tanThreshold=30, splitThreshold=2):
    #sourceImage.show()
    #pointImage.show()
    tanLines = tanScan(pointImage, tanThreshold, splitThreshold)
    #print tanLines
    if(len(tanLines) == 0):
        return [sourceImage]
    return extractTanImage(sourceImage, tanLines)

def extractTanImage(image, tanLines):
    (width, high) = image.size
    pics = []
    headLine = []
    endLine = []
    sourceAccess = image.load()
    for h in xrange(high):
        headLine.append((0, h))
        endLine.append((width - 1, h))
    tanLines.append(endLine)
    for tanLine in tanLines:
        (start, maxWidth) = size(headLine, tanLine, high)
        target = Image.new('RGB', (maxWidth, high), 'white')
        targetAccess = target.load()
        for h in xrange(high):
            for w in xrange(headLine[h][0], tanLine[h][0]):
                targetAccess[w - start,h] = sourceAccess[w,h]
        pics.append(target)
        headLine = tanLine
    return pics

def size(headLine, tanLine, length):
    maxWidth = 0
    minWidth = sys.maxint
    for i in xrange(length):
        if(maxWidth < tanLine[i][0]):
            maxWidth = tanLine[i][0]
        if(minWidth > headLine[i][0]):
            minWidth = headLine[i][0]
    return (minWidth, maxWidth - minWidth)

def tanScan(image, tanThreshold, splitThreshold):
    (width, high) = image.size
    #image.show()
    imageArray = np.array(image.getdata()).reshape((high, width))
    #for i in xrange(high):
    #    for j in xrange(width):
    #        if(imageArray[i][j]):
    #            print 1,
    #        else:
    #            print 0,
    #    print
    #print

    splitLines = []

    #print imageArray
    
    effective = effectiveRange2(imageArray, (width, high))
    index = effective[0]
    
    while(effective[0] >= 0 and index >= 0 and index < width - splitThreshold):
        #print effective[0]
        lines = genTanLine((width, high), index, effective[0], index + tanThreshold)
        #print lines
        for key in lines:
            
            #printArray = np.copy(imageArray)

            whiteLine = True
            for (x, y) in lines[key]:
                #printArray[y][x] = 3
                #print lines[key]
                if(not imageArray[y][x]):
                    whiteLine = False
                    break

            if(whiteLine):
                #for i in xrange(high):
                #    for j in xrange(width):
                #        print printArray[i][j],
                #    print
                #print
                if(scanClearance(imageArray, (width, high), lines[key], splitThreshold)):
                    #print 'goodline'
                    splitLines.append(lines[key])
                    #print 'before brush effectiveRange: ',effective
                    brush(imageArray, lines[key], 1) 
                    effective = effectiveRange2(imageArray, (width, high))
                    index = effective[0]
                    #print 'after brush effectiveRange: ',effective
                    break
        #index = index + splitThreshold
        index = index + 1
    #print splitLines
    if(len(splitLines) <= 1):
        return splitLines
    return splitLines[0 : len(splitLines) - 1]

def brush(imageArray, line, color):
    #print line
    for (x, y) in line:
        for index in xrange(x):
            #print (x,index)
            imageArray[y][index] = color
    #high = len(imageArray)
    #width = len(imageArray[0])
    #for i in xrange(high):
    #    for j in xrange(width):
    #        if(imageArray[i][j]):
    #            print 1,
    #        else:
    #            print 0,
    #    print
    #print
                
def scanClearance(imageArray, size, line, splitThreshold):
    (width, high) = size
    clear = True
    for (x, y) in line:
        count = 0
        for index in xrange(x - splitThreshold, x + splitThreshold):
            if(index > 0 and index < width):
                if(imageArray[y][index]):
                    count = count + 1
                else:
                    count = 0
        if(count < splitThreshold):
            clear = False
            break
    return clear
        

def genTanLine(size, index, start, end, interval=3):
    (width, high) = size
    lines = {}
    for w in xrange(start, end, interval):
        if(w >=0 and w < width):
            #print w
            tan = float(abs(index - w)) / float(high)
            #print tan
            line = []
            if(w <= index):
                for h in xrange(high):
                    #print h, math.ceil(tan * h), tan * h
                    line.append((index - int(math.ceil(tan * h)), h))
            else:
                for h in xrange(high):
                    #print h, math.ceil(tan * h), tan * h
                    line.append((index + int(math.ceil(tan * h)), h))
            lines[w] = line
    return lines

def zoom(images, size):
    resizeImages = []
    for image in images:
        ratio = []
        (width, high) = image.size
        ratio.append(float(size) / float(width))
        ratio.append(float(size) / float(high))
        minRatio = min(ratio)
        resize = (int(float(width) * minRatio), int(float(high) * minRatio))
        #print(width, high),ratio,resize,size
        resizeImage = image.resize(resize, Image.ANTIALIAS)
        #print 'after resize:',resizeImage.size
        resizeImages.append(resizeImage)
    return resizeImages

def binarization(images, pointThreshold):
    table = pointTable(pointThreshold)
    
    points = []
    for image in images:
        point = image.convert('L').point(table, '1')
        points.append(point.crop(effectiveRange(point)))
    return points

def standard(images, size):
    table = pointTable(140)
    standardImage = []
    for image in images:
        (width, high) = image.size
        if(width == size and high == size):
            #image.show()
            standardImage.append(image)
        else:
            standardImage.append(copyImage(Image.new('1', (size,size), 'white').point(table), image))
    return standardImage

def copyImage(targetImage, sourceImage):
    (targetWidth, targetHigh) = targetImage.size
    sourceWidth, sourceHigh = sourceImage.size
    image = sourceImage.copy()
    if(sourceWidth > targetWidth):
        image = zoom([image], targetWidth)[0]
        sourceWidth, sourceHigh = image.size
    if(sourceHigh > targetHigh):
        image = zoom([image], targetHigh)[0]
        sourceWidth, sourceHigh = image.size
    
    deviationWidth = abs((targetWidth - sourceWidth) / 2)
    deviationHigh = abs((targetHigh - sourceHigh) / 2)

    targetAccess = targetImage.load()
    sourceAccess = image.load()

    for w in xrange(sourceWidth):
        for h in xrange(sourceHigh):
            targetAccess[w + deviationWidth, h + deviationHigh] = sourceAccess[w, h]
    #targetImage.show()
    return targetImage

#name = 'C:\\workspace\\python\\VerificationCode\\img2\\1475892043024.jpg'
#im = Image.open(name)
#(width, high) = im.size
#print im.size
#im.show()
#imgry = im.convert('L')
#imgry.show()
#point = imgry.point(pointTable(140), '1')
#point.show()
#denoise = denoise(point, 2, 1)
#denoise.show()

#effectRange = imgry.crop(effectiveRange(imgry))
#effectRange.show()
#resize = effectRange.resize((width*10, high*10), Image.ANTIALIAS)
#resize.show()
#point = resize.point(pointTable(140), '1')
#point.show()
#denoise = denoise(point, 400, 1)
#denoise.show()
#effectRange = denoise.crop(effectiveRange(denoise))
#effectRange.show()
#shape = shape2(point)
#shape.show()
#gf = gaussianFuzzy(point)
#gf.show()

#shape = shape(point, 2)
#shape = shape2(point)

#rotate = rotate(denoise, 0)
#rotate = rotate2(denoise)
#rotate.show()

#pics = split(denoise, 5)

#for pic in pics:
#    pic.show()

#print pics

#print "pics: ",len(pics)

#for box in pics:
    #print "split: ",box[0],box[1],box[2],box[3]
    #point.crop(box).show()

#if(len(pics) == 1):
    #pics = forceSplit(pics, 4)

#for box in pics:
    #print "forceSplit: ",box[0],box[1],box[2],box[3]
    #denoise.crop(box).show()
    #rotate2(denoise.crop(box)).show()
    #print box
#lines = genSplitLine((100, 30), 50)
#for key in lines:
#    print key
#    print lines[key]
#    print
#start = time.time()
#pics = tanSplit(im, denoise, 30, 2)
#end = time.time()

#pics = binarization(zoom(split(im, 4), 30), 140)

#print end - start
#for pic in pics:
#    print pic.size
#    pic.show()
#splitLine = genSplitLine((width, high), 50, 0, width, 2)

#denoiseAccess = denoise.load()
                
#for line in splitLine:
#    for (x, y) in line:
#        denoiseAccess[x, y] = 0
#    #print line
#denoise.show()

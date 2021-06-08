
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import math

import imageIO.png

def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array

#Computes the greyscale representation of the color channels
def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            g = round(0.299 * pixel_array_r[i][j] + 0.587 * pixel_array_g[i][j] + 0.114 * pixel_array_b[i][j])
            greyscale_pixel_array[i][j] = g
    return greyscale_pixel_array

def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    contrastArray = createInitializedGreyscalePixelArray(image_width, image_height)
    minMaxValues = computeMinAndMaxValues(pixel_array, image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            if minMaxValues[0] != minMaxValues[1]:
                k = (pixel_array[i][j] - minMaxValues[0]) * (255 / (minMaxValues[1] - minMaxValues[0]))
                if k < 0:
                    contrastArray[i][j] = 0
                elif k > 255:
                    contrastArray[i][j] = 255
                else:
                    contrastArray[i][j] = round(k)
            else:
                contrastArray[i][j] = 0
    return contrastArray

#Returns smallest and largest value of a pixel array image
def computeMinAndMaxValues(pixel_array, image_width, image_height):
    tuple_array = [pixel_array[0][0], 0]
    for i in range(image_height):
        for j in range(image_width):
            if pixel_array[i][j] < tuple_array[0]:
                tuple_array[0] = pixel_array[i][j];
            if pixel_array[i][j] > tuple_array[1]:
                tuple_array[1] = pixel_array[i][j];
    return tuple_array

def computeEdgeMagnitude(px_x_sobeled,px_y_sobeled,image_width,image_height):
    edge_magnitude = []
    for i in range(0,len(px_x_sobeled)):
        edge_magnitude_line = []
        for j in range(0,len(px_x_sobeled[0])):
            if px_x_sobeled[i][j] < 3 or px_y_sobeled[i][j] < 3: sumvalue = 0
            else: sumvalue = px_x_sobeled[i][j]+px_y_sobeled[i][j]
            if sumvalue < 0: sumvalue = 0
            elif sumvalue > 255: sumvalue = 255
            edge_magnitude_line.append(px_x_sobeled[i][j]+px_y_sobeled[i][j])
        edge_magnitude.append(edge_magnitude_line)
    return edge_magnitude

#Computes and returns an image of the vertical edges.
def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    verticalEdge = [[0  for x in range(image_width)] for y in range(image_height)]
    for i in range (1, image_height -1):
        for j in range (1, image_width -1):
            verticalEdge[i][j] = pixel_array[i-1][j-1]+ pixel_array[i][j-1]*2 +pixel_array[i+1][j-1] - (pixel_array[i-1][j+1] + pixel_array[i][j+1]*2 + pixel_array[i+1][j+1])
            verticalEdge[i][j] /= 8
            verticalEdge[i][j] = abs(verticalEdge[i][j])
    return verticalEdge

#Computes and returns an image of the vertical edges.
def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    horiztonalEdge = [[0 for x in range(image_width)] for y in range(image_height)]
    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            horiztonalEdge[i][j] = pixel_array[i - 1][j - 1] + pixel_array[i - 1][j] * 2 + pixel_array[i - 1][j + 1] - (
                        pixel_array[i + 1][j - 1] + pixel_array[i + 1][j] * 2 + pixel_array[i + 1][j + 1])
            horiztonalEdge[i][j] /= 8
            horiztonalEdge[i][j] = abs(horiztonalEdge[i][j])
    return horiztonalEdge

# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)

# This method packs together three individual pixel arrays for r, g and b values into a single array that is fit for
# use in matplotlib's imshow method
def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage

# Computes & returns a mean (or average, or box) filtered image.
def computeBoxAveraging3x3(pixel_array, image_width, image_height):
    newBoxAverage = [[0 for x in range(image_width)] for y in range(image_height)]
    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            for k in range(i - 1, i + 2):
                for l in range(j - 1, j + 2):
                    newBoxAverage[i][j] += pixel_array[k][l]
            newBoxAverage[i][j] /= 9
    return newBoxAverage

def computeThresholdGE(pixel_array, threshold_value, image_width, image_height):
    res = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range (image_height):
        for j in range (image_width):
            if pixel_array[i][j] >= threshold_value:
                res[i][j]= 255
            else:
                res[i][j]= 0
    return res
    

# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()



def main():
    filename = "./images/covid19QRCode/poster1small.png"
    threshold_value = 70
    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)
    greyscale_pixel_array = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    contrastArray = scaleTo0And255AndQuantize(greyscale_pixel_array, image_width, image_height)
    verticalEdge = computeVerticalEdgesSobelAbsolute(contrastArray, image_width, image_height)
    horiztonalEdge = computeHorizontalEdgesSobelAbsolute(contrastArray, image_width, image_height)
    edge_magnitude = computeEdgeMagnitude(horiztonalEdge,verticalEdge,image_width,image_height)
    print("Sorry! The box average takes some time to generate!")
    boxAverage = computeBoxAveraging3x3(edge_magnitude, len(edge_magnitude[0]), len(edge_magnitude))
    for i in range(9): #I iterated 9 times to render it to the correct image, don't know if implemented correctly
        boxAverage = computeBoxAveraging3x3(boxAverage, len(boxAverage[0]), len(boxAverage))
    reContrastArray = scaleTo0And255AndQuantize(boxAverage, len(boxAverage[0]),len(boxAverage))
    threshold = computeThresholdGE(reContrastArray, threshold_value, len(reContrastArray[0]),len(reContrastArray))

    pyplot.imshow(greyscale_pixel_array, cmap="gray") #Step 1: read the input image, convertRGB data to greyscale and stretchthe values to lie between 0 and 255
    pyplot.imshow(contrastArray, cmap="gray") #Step 5: stretch contrast to 0 and 255
    pyplot.imshow(verticalEdge, cmap="gray") #Step 3: compute vertical edges
    pyplot.imshow(horiztonalEdge, cmap="gray") #Step 2: compute horizontal edges
    pyplot.imshow(edge_magnitude, cmap="gray") #Step 4: compute Edge magnitude
    pyplot.imshow(boxAverage, cmap="gray") #Step 5: smooth over the edgemagnitude (mean or Gaussain)
    pyplot.imshow(threshold, cmap="gray") #Step 6: perform a thresholding operation
    #pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height))

    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    rect = Rectangle( (10, 30), 70, 50, linewidth=3, edgecolor='g', facecolor='none' )
    # paint the rectangle over the current plot
    axes.add_patch(rect)

    # plot the current figure
    pyplot.show()


if __name__ == "__main__":
    main()
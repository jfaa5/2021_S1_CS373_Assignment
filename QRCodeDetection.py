
from matplotlib import pyplot
from matplotlib.patches import Rectangle

import imageIO.png

def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array

def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)

    # STUDENT CODE HERE
    for i in range(image_height):
        for j in range(image_width):
            g = round(0.299 * pixel_array_r[i][j] + 0.587 * pixel_array_g[i][j] + 0.114 * pixel_array_b[i][j])
            greyscale_pixel_array[i][j] = g

    return greyscale_pixel_array

def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    newPixelArray = createInitializedGreyscalePixelArray(image_width, image_height)
    minMaxValues = computeMinAndMaxValues(pixel_array, image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            if minMaxValues[0] != minMaxValues[1]:
                k = (pixel_array[i][j] - minMaxValues[0]) * (255 / (minMaxValues[1] - minMaxValues[0]))
                if k < 0:
                    newPixelArray[i][j] = 0
                elif k > 255:
                    newPixelArray[i][j] = 255
                else:
                    newPixelArray[i][j] = round(k)
            else:
                newPixelArray[i][j] = 0
    return newPixelArray

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



def computeMinAndMaxValues(pixel_array, image_width, image_height):
    tuple_array = [pixel_array[0][0], 0]
    for i in range(image_height):
        for j in range(image_width):
            if pixel_array[i][j] < tuple_array[0]:
                tuple_array[0] = pixel_array[i][j];
            if pixel_array[i][j] > tuple_array[1]:
                tuple_array[1] = pixel_array[i][j];
    return tuple_array

def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    resultPixel = [[0  for x in range(image_width)] for y in range(image_height)]

    for i in range (1, image_height -1):
        for j in range (1, image_width -1):
            resultPixel[i][j] = pixel_array[i-1][j-1]+ pixel_array[i][j-1]*2 +pixel_array[i+1][j-1] - (pixel_array[i-1][j+1] + pixel_array[i][j+1]*2 + pixel_array[i+1][j+1])
            resultPixel[i][j] /= 8
            resultPixel[i][j] = abs(resultPixel[i][j])
    return resultPixel


def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    horizontal_resultPixel = [[0 for x in range(image_width)] for y in range(image_height)]

    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            horizontal_resultPixel[i][j] = pixel_array[i - 1][j - 1] + pixel_array[i - 1][j] * 2 + pixel_array[i - 1][j + 1] - (
                        pixel_array[i + 1][j - 1] + pixel_array[i + 1][j] * 2 + pixel_array[i + 1][j + 1])
            horizontal_resultPixel[i][j] /= 8
            horizontal_resultPixel[i][j] = abs(horizontal_resultPixel[i][j])
    return horizontal_resultPixel

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

def conv2d(inputim, fliter, width, height):
    # height, width = len(inputim), len(inputim[0])
    heightf, widthf = len(fliter), len(fliter[0])
    new_height = height - heightf + 1
    new_width = width - widthf + 1
    new_image = []
    for i in range(0,new_height):
        new_image_line = []
        for j in range(0,new_width):
            sumconv = 0.0
            for x in range(0,heightf):
                for y in range(0,widthf):
                    sumconv+=inputim[i+x][j+y]*fliter[x][y]
            if sumconv < 0: sumconv = 0
            elif sumconv > 255: sumconv = 255
            else: sumconv = int(sumconv)
            new_image_line.append(sumconv)
        new_image.append(new_image_line)
    return new_image

def computeGaussianAveraging3x3RepeatBorder(pixel_array, image_width, image_height):
    def create_gauss_mask(sigma):
        mask_height = mask_width = sigma * 2 + 1
        mask_array = createInitializedGreyscalePixelArray(mask_width, mask_height)

        sumvalue = 0.0
        for i in range(-sigma, sigma + 1):
            for j in range(-sigma, sigma + 1):
                mask_array[i + sigma][j + sigma] = math.exp(-0.5 * (i ** 2 + j ** 2) / sigma ** 2)
                sumvalue += mask_array[i + sigma][j + sigma]

        for i in range(0, len(mask_array)):
            for j in range(0, len(mask_array[0])):
                mask_array[i][j] /= sumvalue

        return mask_array

    gaussiankernel = create_gauss_mask(3)
    # gaussedimage = inputim
    # for i in range(times):
    #     gaussedimage = conv2d(gaussedimage,gaussiankernel)
    return conv2d(pixel_array, gaussiankernel, image_width, image_height)
    

# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()



def main():
    filename = "./images/covid19QRCode/poster1small.png"

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)
    greyscale_pixel_array = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    newPixelArray = scaleTo0And255AndQuantize(greyscale_pixel_array, image_width, image_height)
    resultPixel = computeVerticalEdgesSobelAbsolute(newPixelArray, image_width, image_height)
    horizontal_resultPixel = computeHorizontalEdgesSobelAbsolute(newPixelArray, image_width, image_height)
    edge_magnitude = computeEdgeMagnitude(horizontal_resultPixel,resultPixel,image_width,image_height)
    #pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height))

    pyplot.imshow(greyscale_pixel_array, cmap="gray")
    pyplot.imshow(newPixelArray, cmap="gray")
    pyplot.imshow(resultPixel, cmap="gray")
    pyplot.imshow(horizontal_resultPixel, cmap="gray")
    pyplot.imshow(edge_magnitude, cmap="gray")
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
#coding: utf-8

u"""
Smart resizer
"""
from skimage import img_as_float
from skimage.color import rgb2gray
from scipy import fftpack, ndimage, misc
from scipy.ndimage import uniform_filter
import numpy as np


def find_prop_size(im, width, height):
    current_height, current_width, _ = im.shape
    prop_ratio = max(float(width) / current_width, float(height) / current_height)
    new_width = int(round(current_width * prop_ratio))
    new_height = int(round(current_height * prop_ratio))
    return new_width, new_height


def get_saliency_map(im_array, sigma=2.5):
    """Taken from:
    http://stackoverflow.com/questions/16571545/why-is-the-output-different-for-code-ported-from-matlab-to-python
    """
    # convert to gray-scale
    image = img_as_float(rgb2gray(im_array))

    # Spectral Residual
    fft = fftpack.fft2(image)
    log_amplitude = np.log(np.abs(fft))
    phase = np.angle(fft)
    avg_log_amp = uniform_filter(log_amplitude, size=3, mode="nearest")
    spectral_residual = log_amplitude - avg_log_amp
    sm = np.abs(fftpack.ifft2(np.exp(spectral_residual + 1j * phase))) ** 2

    # After Effect
    sm = ndimage.gaussian_filter(sm, sigma=sigma)
    #import matplotlib.pyplot as plt
    #import matplotlib.cm as cm
    #plt.imshow(sm, cmap = cm.Greys_r)
    #plt.show()
    return sm


def crop_by_width(im_array, new_width):
    sm = get_saliency_map(im_array)
    rows_count, columns_count = sm.shape
    l_offset = r_offset = 0
    threshold = rows_count / 2
    while (columns_count - l_offset - r_offset) != new_width:
        left_column = sm[:, l_offset]
        right_column = sm[:, columns_count - r_offset - 1]
        delta = sum(left_column < right_column)
        if delta > threshold:
            l_offset += 1
        else:
            r_offset += 1
    return im_array[:, l_offset:-r_offset] if r_offset > 0 else im_array[:, l_offset:]


def crop_by_height(im_array, new_height):
    sm = get_saliency_map(im_array)
    rows_count, columns_count = sm.shape
    u_offset = d_offset = 0
    threshold = columns_count / 2
    while (rows_count - u_offset - d_offset) != new_height:
        up_row = sm[u_offset, :]
        down_row = sm[rows_count - d_offset - 1, :]
        delta = sum(up_row < down_row)
        if delta > threshold:
            u_offset += 1
        else:
            d_offset += 1
    return im_array[u_offset:-d_offset, :] if d_offset > 0 else im_array[u_offset:, :]


def resize_to(image_path, new_width, new_height, with_crop=False):
    im = imread(image_path)
    if with_crop:
        pre_width, pre_height = find_prop_size(im, new_width, new_height)
        pre_image = misc.imresize(im, (pre_height, pre_width))
        if pre_width != new_width:
            res_image = crop_by_width(pre_image, new_width)
        elif pre_height != new_height:
            res_image = crop_by_height(pre_image, new_height)
        else:
            raise Exception(u"Invalid width & height")
    else:
        res_image = misc.imresize(im, (new_height, new_width))
    return res_image


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image_path', type=str, help=u'input image path')
    parser.add_argument('-o', default="result.jpg", type=str, dest="output_path",
                        help=u'output file path. By default: result.jpg')
    parser.add_argument('-W', type=int, dest="width", help=u"new width")
    parser.add_argument('-H', type=int, dest="height", help=u"new height")
    parser.add_argument("-c", action="store_true", dest="with_crop", help=u"use crop")
    args = parser.parse_args()

    # gstreamer help message overrides argparse message
    from skimage.io import imread, imsave
    
    res_im = resize_to(args.image_path, args.width, args.height, args.with_crop)
    imsave(args.output_path, res_im)



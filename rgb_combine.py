from optparse import OptionParser
import numpy as np
from osgeo import gdal, gdalconst
from skimage.exposure import rescale_intensity


def read_geotif(tif):
    src = gdal.Open(tif, gdalconst.GA_ReadOnly)
    data = src.GetRasterBand(1).ReadAsArray()
    nodata = getattr(np, str(data.dtype))(
        src.GetRasterBand(1).GetNoDataValue())
    mask = data == nodata
    return np.ma.MaskedArray(data=data,
                             mask=mask,
                             fill_value=nodata)


def rgb_combine(blue_raster, green_raster, red_raster, input_tif, output_tif):

    blue = read_geotif(blue_raster)
    green = read_geotif(green_raster)
    red = read_geotif(red_raster)

    # rescale to 0-256, 256 because we later save as gdt_byte
    blue = rescale_intensity(blue, out_range=(0, 256))
    green = rescale_intensity(green, out_range=(0, 256))
    red = rescale_intensity(red, out_range=(0, 256))

    # source information
    src_ds = gdal.Open(input_tif, gdalconst.GA_ReadOnly)

    # output ds
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(output_tif,
                           xsize=src_ds.RasterXSize,
                           ysize=src_ds.RasterYSize,
                           bands=3,
                           eType=gdal.GDT_Byte
                           )
    out_ds.SetGeoTransform(src_ds.GetGeoTransform())
    out_ds.SetProjection(src_ds.GetProjection())

    # write data in the three bands
    out_ds.GetRasterBand(1).WriteArray(red)
    out_ds.GetRasterBand(2).WriteArray(green)
    out_ds.GetRasterBand(3).WriteArray(blue)

    out_ds.FlushCache()
    out_ds = None


if __name__ == '__main__':
    parser = OptionParser(usage='%prog -b blue_raster  -g green_raster \n'
                                '-r red_raster -o output_raster')
    parser.add_option('-b', '--blue_raster', type=str, dest='blue_raster',
                      help='name of input blue raster file')

    parser.add_option('-g', '--green_raster', type=str, dest='green_raster',
                      help='name of input green raster file')

    parser.add_option('-r', '--red_raster', type=str, dest='red_raster',
                      help='name of the input red raster file')

    parser.add_option('-o', '--output_raster', type=str, dest='output_raster',
                      help='name of the output rgb raster file')

    options, args = parser.parse_args()

    if not options.red_raster:  # if filename is not given
        parser.error('Input red raster filename must be provided.')
    if not options.green_raster:  # if filename is not given
        parser.error('Input green raster filename must be provided.')
    if not options.blue_raster:  # if filename is not given
        parser.error('Input blue raster filename must be provided.')

    if not options.output_raster:  # if filename is not given
        parser.error('Output raster filename must be provided.')
    rgb_combine(options.blue_raster, options.green_raster, options.red_raster,
                options.blue_raster, options.output_raster)

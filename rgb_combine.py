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


def rgb_combine(local, meso, broad, input_tif, output_tif):

    loc = read_geotif(local)
    mes = read_geotif(meso)
    bro = read_geotif(broad)

    # rescale to 0-256, 256 because we later save as gdt_byte
    loc = rescale_intensity(loc, out_range=(0, 256))
    mes = rescale_intensity(mes, out_range=(0, 256))
    bro = rescale_intensity(bro, out_range=(0, 256))

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
    out_ds.GetRasterBand(1).WriteArray(bro)
    out_ds.GetRasterBand(2).WriteArray(mes)
    out_ds.GetRasterBand(3).WriteArray(loc)

    out_ds.FlushCache()
    out_ds = None


if __name__ == '__main__':
    rgb_combine('out_mb.tif', 'out_mb1.tif', 'out_mb2.tif', 'out_mb.tif',
                'rgb.tif')

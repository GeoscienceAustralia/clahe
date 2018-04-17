import numpy as np
from osgeo import gdal, gdalconst

def read_geotif(tif):
    src = gdal.Open(tif, gdalconst.GA_ReadOnly)
    data = src.GetRasterBand(1).ReadAsArray()
    nodata = getattr(np, str(data.dtype))(
        src.GetRasterBand(1).GetNoDataValue())
    mask = data == nodata
    return np.ma.MaskedArray(data=data,
                             mask=mask,
                             fill_value=nodata)


def multiscale(local, meso, broad, input_tif, output_tif, cutoff=2.58):

    loc = read_geotif(local)
    mes = read_geotif(meso)
    bro = read_geotif(broad)

    # standardise and take absolute, and scale by cutoff
    loc = (np.ma.abs(loc - loc.mean()) / loc.std()) * 255/cutoff
    mes = (np.ma.abs(mes - mes.mean()) / mes.std()) * 255/cutoff
    bro = (np.ma.abs(bro - bro.mean()) / bro.std()) * 255/cutoff


    # import IPython; IPython.embed(); import sys; sys.exit()
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
    multiscale('out_mb.tif', 'out_mb1.tif', 'out_mb2.tif', 'out_mb.tif',
               'rgb.tif')
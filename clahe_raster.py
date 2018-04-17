"""
Currently only supports single band raster.
"""
import numpy as np
from osgeo import gdal, gdalconst
from skimage.exposure import equalize_adapthist, rescale_intensity

input_raster = 'clip_test.tif'
output_raster = 'clip_stretched.tif'
output_nodata = -999.0

# don't change the next two lines
src = gdal.Open(input_raster, gdalconst.GA_ReadOnly)
data = src.GetRasterBand(1).ReadAsArray()
nodata = getattr(np, str(data.dtype))(
    src.GetRasterBand(1).GetNoDataValue())
mask = data == nodata


"""
rescale the data as the adapthist expects data in (-1, 1)
specify in_range=(min_value_to_limit, max_value_to_limit), 
in_range="image" to use min and max in the image values.
"""

rescaled_data = rescale_intensity(data.astype(np.float32),
                                  in_range=(182, 3653),
                                  out_range=(0, 1))
"""
kernel_size: integer or list-like, optional
Defines the shape of contextual regions used in the algorithm. 
If iterable is passed, it must have the same number of elements 
as image.ndim (without color channel). 
If integer, it is broadcasted to each image dimension. By default, 
kernel_size is 1/8 of image height by 1/8 of its width.
 
clip_limit : float, optional
Clipping limit, normalized between 0 and 1 (higher values give more contrast).
 
nbins : int, optional
Number of gray bins for histogram (“data range”).

"""

stretched_data = equalize_adapthist(rescaled_data,
                                    kernel_size=1000,
                                    clip_limit=0.1,
                                    nbins=256)


# don't change anything below this

driver = gdal.GetDriverByName('GTiff')

out_ds = driver.Create(output_raster,
                       xsize=src.RasterXSize,
                       ysize=src.RasterYSize,
                       bands=1,
                       eType=gdal.GDT_Float32  # change dtype manually
                       )
out_ds.SetGeoTransform(src.GetGeoTransform())
out_ds.SetProjection(src.GetProjection())

rescaled_data[mask] = output_nodata
out_ds.GetRasterBand(1).WriteArray(rescaled_data)
# might have to change dtype manually
out_ds.GetRasterBand(1).SetNoDataValue(output_nodata)
out_ds.FlushCache()

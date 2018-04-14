"""
Currently only supports single band raster.
"""
import numpy as np
import rasterio as rio
from skimage.exposure import equalize_adapthist, rescale_intensity

input_raster = 'dem4000.tif'

output_raster = 'out_mb.tif'

# don't change the next two lines
src = rio.open(input_raster)
data = src.read(1, masked=True)  # read band 1


"""
rescale the data as the adapthist expects data in (-1, 1)
specify in_range=(min_value_to_limit, max_value_to_limit), 
in_range="image" to use min and max in the image values.
"""

rescaled_data = rescale_intensity(data.data.astype(np.float32),
                                  in_range=(0, 1000), out_range=(0, 1))

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
                                    kernel_size=400,
                                    clip_limit=0.3,
                                    nbins=256)


# don't change anything below this

profile = src.profile
profile.update(dtype=rio.float32, count=1, compress='lzw',
               nodata=-999)
out_data = np.ma.MaskedArray(data=stretched_data,
                             mask=data.mask,
                             dtype=np.float32,
                             fill_value=-999.0)
with rio.open(output_raster, 'w', **profile) as dst:
    dst.write(out_data.astype(rio.float32), indexes=1)


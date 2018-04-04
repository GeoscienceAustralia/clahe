"""
Currently only supports single band raster.
"""
import sys
import rasterio as rio
from skimage.exposure import equalize_adapthist, rescale_intensity

input_raster = '/home/sudipta/Documents/GA-cover2/k_15v5.tif'

output_image = 'out.tif'

# don't change the next two lines
src = rio.open(input_raster)
data = src.read(1, masked=True)  # read band 1


"""
rescale the data as the adapthist expects data in (-1, 1)
specify in_range=(min_value_to_limit, max_value_to_limit), 
in_range="image" to use min and max in the image values.
"""

resacled_data = rescale_intensity(data, in_range="image", out_range=(-1, 1))

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

stretched_data = equalize_adapthist(resacled_data,
                                    kernel_size=200,
                                    clip_limit=0.75,
                                    nbins=256)


# don't change anything below this

profile = src.profile
profile.update(dtype=rio.float32, count=1, compress='lzw',
               nodata=-999)

dst = rio.open(output_image, 'w', **profile)
dst.write(stretched_data.astype(rio.float32), indexes=1)
dst.close()


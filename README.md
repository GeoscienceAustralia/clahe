CLAHE on RASTER
===============
This is an application of the [clahe image stretching algorithm](https://en.wikipedia.org/wiki/Adaptive_histogram_equalization#Contrast_Limited_AHE) 
on raster data. [We use the `scikit-image` implementation of `CLAHE`](http://scikit-image.org/docs/dev/api/skimage.exposure.html#skimage.exposure.equalize_adapthist).

Requirements
------------

```
numpy
scipy
scikit-image==0.14.dev0
GDAL
```


More details about CLAHE:
1. https://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html
2. https://au.mathworks.com/help/images/ref/adapthisteq.html
3. http://scikit-image.org/docs/dev/api/skimage.exposure.html#skimage.exposure.equalize_adapthist

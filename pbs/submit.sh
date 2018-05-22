#!/usr/bin/env bash
#PBS -P ge3
#PBS -q expressbw
#PBS -l walltime=2:00:00,mem=256GB,ncpus=28,jobfs=100GB
#PBS -l wd
#PBS -j oe

module load python3/3.5.2 python3/3.5.2-matplotlib
module load hdf5/1.8.10 gdal/2.0.0 geos/3.5.0
module load openmpi/1.8 gcc/4.9.0

# setup environment
export PATH=/g/data/ge3/john/venvs/catboost/bin:$HOME/.local/bin:$PATH
export PYTHONPATH=$HOME/.local/lib/python3.5/site-packages:$PYTHONPATH
export VIRTUALENVWRAPPER_PYTHON=/apps/python3/3.5.2/bin/python3
export LC_ALL=en_AU.UTF-8
export LANG=en_AU.UTF-8
export WORKON_HOME=/g/data/ge3/john/venvs/
source $HOME/.local/bin/virtualenvwrapper.sh

# start the virtualenv
workon catboost


# run clahe on the three bands in parallel
python clahe_raster_gdal.py -i landsatTM_8_1.tif  -o landsatTM_8_1_stretched.tif -r '0 5771' -k 2000 -c 0.05 &
	python clahe_raster_gdal.py -i landsatTM_8_2.tif  -o landsatTM_8_2_stretched.tif -r '0 7272' -k 2000 -c 0.05 &
	python clahe_raster_gdal.py -i landsatTM_8_3.tif  -o landsatTM_8_3_stretched.tif -r '0 8174' -k 2000 -c 0.05

wait

# rgb combine
python rgb_combine.py -r landsatTM_8_3_stretched.tif -g landsatTM_8_2_stretched.tif \
        -b landsatTM_8_1_stretched.tif -o rgb_landsatTM_8_clip_p05.tif

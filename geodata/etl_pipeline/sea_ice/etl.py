# Sea ice data download url
# https://www.polarview.aq/images/27_AMSR2/20200705/20200705.antarctic.tar.gz
import os
from django.conf import settings
import shutil
import urllib
import tarfile
from .util import (get_yesterday_str, get_default_file_name,
                   get_tiff_file_name, get_png_file_name)
from osgeo import gdal
# from geodata.utils.tiff_io import GetDimension
# import mapnik


class ETL():
    def __init__(self):
        self.save_path = None
        self.tiff_name = None
        polar_host = "https://www.polarview.aq/"
        self.source_url_template = polar_host \
            + "images/27_AMSR2/{}/{}.antarctic.tar.gz"

    def download(self, date_str=None):
        if date_str is None:
            date_str = get_yesterday_str()

        self.save_path = get_default_file_name(date_str)

        url = self.source_url_template.format(date_str, date_str)
        urllib.request.urlretrieve(url, self.save_path)
        return self.save_path

    def extract(self, file_name=None):
        # Unpacks downloaded data file and only keep the GeoTiff file
        tar_file = get_default_file_name(file_name)

        tar = tarfile.open(tar_file, "r:gz")
        member = "data/polarview/27_AMSR2/{}/{}.antarctic.tif" \
                 .format(file_name, file_name)

        tar.extract(member, path=os.path.join(settings.GIS_DATA_DIR,
                                              settings.SEA_ICE_DATA_DIR_NAME))
        tar.close()

        self.tiff_name = get_tiff_file_name(file_name)

        shutil.move(os.path.join(settings.GIS_DATA_DIR,
                                 settings.SEA_ICE_DATA_DIR_NAME,
                                 member),
                    self.tiff_name)

        # Clear tar file and unpacked dir
        os.remove(tar_file)
        shutil.rmtree(os.path.join(settings.GIS_DATA_DIR,
                                   settings.SEA_ICE_DATA_DIR_NAME,
                                   'data'))

        return self.tiff_name

    def transform(self, file_name=None):
        tif_file = get_tiff_file_name(file_name)
        png_file = get_png_file_name(file_name)

        ##
        # TODO: If color table not work, use mapnik to render PNG image
        ##
        # x_size, y_size = GetDimension(tif_file)
        # m = mapnik.Map(x_size, y_size)
        # m.srs = settings.EPSG_3031_DEF

        # Use GDAL translate generate PNG image, only worked with color table
        gdal.Translate(png_file, tif_file, format='PNG')

        return png_file

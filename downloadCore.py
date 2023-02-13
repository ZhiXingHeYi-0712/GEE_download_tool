from cmath import log
from ctypes import Union
from email.mime import image
from fileinput import filename
import os
from turtle import down
from typing import List
from unicodedata import name
import ee
import logging
from downloadPool import DownloadPool

def downloadImage(image: ee.Image, region: Union[ee.FeatureCollection, ee.Geometry], bands: List[str], download_path: str, file_name: str, pool: DownloadPool):
    """This is the major function of this project, which you can download your data with a download thread pool.

    Parameters
    ----------
    image : ee.Image
        The GEE image that you want to download. Note that this must be ee.Image, not ee.ImageCollection.
    region : ee.FeatureCollection or ee.Geometry
        The region feature that you want to download. Note that you should first upload the geojson or shp to the GEE platform, and invoke it by its name in your code.
    bands : List[str]
        The bands you want to download. However, I'm not sure how it will be when you try to download 2 bands simultaneously, so you can try it by yourself, or just download one-by-one.
    download_path : str
        The image save path. You should manually create the folder first.
    file_name : str
        The image file name.
    pool : DownloadPool
        The `DownloadPool` object. You can instantiate it in the top of your code, follow line 9 in `main.py`.
    """
    
    if type(region) != ee.Geometry:
        roi = region.geometry()
    else:
        roi = region

    download_url = image.getDownloadURL(params={
        'name': file_name,
        'bands': bands,
        'region': roi,
        'scale': 500
    })

    logging.log(0, f'start download file {file_name}, band {bands}, destination {download_path}, url {download_url}')
    pool.submit(download_url, download_path, file_name)
   
    

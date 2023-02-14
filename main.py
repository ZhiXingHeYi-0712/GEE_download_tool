import socks
import socket
import ee
from dateloop import getMonthRange
from downloadCore import downloadImage
from concurrent.futures import ThreadPoolExecutor, as_completed
from downloadPool import DownloadPool

# The download pool object, you can instantiate it here.
# The param `5` represents the count of the parallel download thread. 
# In most circumstance, the higher it is, the faster it will be, but
# setting a too large value may cause you be banned by GEE. 
# So I recommend you set the value less or equal than 8.
pool = DownloadPool(5)

# Those 2 lines below is used for setting the proxy of the code.
# Since you know you cannot directly connect to GEE, the proxy is
# essential.
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 12345)
socket.socket = socks.socksocket

# de-comment this code if it's your first time using GEE in your PC.
# You should finish the authenticate to start using GEE.
# Please keep your proxy working.
# You can comment it after authentication.
# ee.Authenticate()

# Please note that Initialize() cannot be removed or commented.
ee.Initialize()

# Invoke roi and datasets.
guangdong_all = ee.FeatureCollection('users/zxhy1210/guangdong_all')
roi = guangdong_all
modis = ee.ImageCollection("MODIS/006/MOD13Q1")
terra_climate = ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE")
modis_LULC = ee.ImageCollection("MODIS/006/MCD12Q1")

# generate a month range list. Please see getMonthRange() 
# docstring if you want to know more details.
month_range_list = getMonthRange(2000, 1, 2000, 3)

download_NDVI = False
download_climate = True
download_LULC = False
download_NDVI_year = False


# ! Here is an example of downloading numerous images.
if download_NDVI:
    # MODIS images download
    # first, pick up start_date and end_date in the month_range_list
    for start_date, end_date in month_range_list:
        # then, using filterDate(), filterBounds() and some other functions to determine the image you need.
        img: ee.Image = modis.filterDate(start_date, end_date).filterBounds(roi).max().select('NDVI')

        # Then, reproject if you need.
        img = img.reproject(crs='EPSG:4326',scale=500)
        
        # set a file name. It cannot be duplicated.
        file_name = start_date[:-2].replace('-', '_')

        # print some log
        print('start download {} NDVI'.format(file_name))

        # invoke downloadImage() to start your download. See `downloadImage()` for more details.
        downloadImage(img, roi, ['NDVI'], './NDVI', file_name, pool)

if download_climate:
    # Terra Climate data download
    for start_date, end_date in month_range_list:
        # all bands
        cli_img_all: ee.Image = terra_climate.filterDate(start_date, end_date).filterBounds(roi).mean()

        # precipitation: 
        precipitation: ee.Image = cli_img_all.select('pr').reproject(crs='EPSG:4326',scale=500)

        # radiation:
        radiation: ee.Image = cli_img_all.select('srad').reproject(crs='EPSG:4326',scale=500)

        # min temperature
        min_temperature: ee.Image = cli_img_all.select('tmmn').reproject(crs='EPSG:4326',scale=500)

        # max temperature
        max_temperature: ee.Image = cli_img_all.select('tmmx').reproject(crs='EPSG:4326',scale=500)

        file_name = start_date[:-2].replace('-', '_')
        print('start download {} TerraClimate'.format(file_name))

        downloadImage(precipitation, roi, ['pr'], './pr', file_name, pool)
        downloadImage(radiation, roi, ['srad'], './srad', file_name, pool)
        downloadImage(min_temperature, roi, ['tmmn'], './tmmn', file_name, pool)
        downloadImage(max_temperature, roi, ['tmmx'], './tmmx', file_name, pool)

if download_LULC:
    # MODIS classification download
    for start_year in range(2000, 2021):
        lulc_image: ee.Image = modis_LULC.filterDate(f'{start_year}-01-01', f'{start_year}-12-31').filterBounds(roi).mean().select('LC_Type1')
        lulc_image = lulc_image.reproject(crs='EPSG:4326',scale=500)
        print('start download {} LULC'.format(start_year))
        file_name = str(start_year)
        downloadImage(lulc_image, roi, ['LC_Type1'], './LULC', file_name, pool)
    
if download_NDVI_year:
    for start_year in range(2020, 2021):
        NDVI_year_img: ee.Image = modis.filterDate(f'{start_year}-01-01', f'{start_year}-12-31').filterBounds(roi).mean().select('NDVI').reproject(crs='EPSG:4326')
        NDVI_year_img = NDVI_year_img.resample()
        file_name = str(start_year)
        print('start download {} NDVI'.format(file_name))
        downloadImage(NDVI_year_img, roi, ['NDVI'], './NDVI_year_mean', file_name, pool)


# Finally, call pool.wait() to wait all the download mission finished.
print('Waiting...')
pool.wait()

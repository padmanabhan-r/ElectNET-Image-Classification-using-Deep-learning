import pandas as pd
from google_images_download import google_images_download
import optparse, sys, os
import re


def Scrape_from_file(keyword_file, Images_per_category=1500, Download_Folder="Downloads", delay=0.1,
                     Image_Size="medium", chromedriver_location="chromedriver"):
    # Get Current Working Directory
    cwd = os.getcwd()

    data_rows = keyword_file.count()[0]

    for i in range(keyword_file.count()[0]):
        Path_List = {}
        overall_path = {}

        keyword = str(keyword_file.Keywords[i])
        prefix = str(keyword_file.Prefixes[i])

        # Adding 4 as a buffer to compensate for errors while downloading images
        image_per_iter = int(Images_per_category / keyword_file.Total_Items[i]) + 4

        response = google_images_download.googleimagesdownload()  # class initialization

        prefix_keyword = "-" + keyword + "-"

        arguments = {
            "keywords": keyword,
            "limit": image_per_iter,
            "prefix_keywords": prefix,
            "prefix": prefix_keyword,
            "print_urls": False,
            "delay": delay,
            "chromedriver": chromedriver_location,
            "no_numbering": "no_numbering",
            "output_directory": str(cwd + "/" + Download_Folder + "/" + keyword),
            "format": "jpg",
            "no_directory": "no_directory",
            "size": Image_Size
        }  # creating list of arguments
        paths = response.download(arguments)  # passing the arguments to the function
        Path_List.update(paths)


optparser = optparse.OptionParser()
optparser.add_option("-f", "--file", dest="file", default="./static_files/keywords.csv",
                     help="data directory (default=./static_files/keywords.csv)")
optparser.add_option("-n", "--num_images", dest="num_images", default="1500",
                     help="No. of Imagesto download per Category")
optparser.add_option("-o", "--output_folder", dest="output_folder", default="data",
                     help="""Directory to save images (Default= data)""")
optparser.add_option("-s", "--size", dest="size", default="medium", help="""Size of Images to Download (Default= medium)
Possible values: large, medium, icon, >400*300, >640*480, >800*600, >1024*768, >2MP, >4MP, >6MP, >8MP, >10MP, >12MP,>15MP, >20MP, >40MP, >70MP""")
optparser.add_option("-d", "--delay", dest="delay", default=0.1, help="Delay between downloading images (Default= 0.1)")
optparser.add_option("-c", "--chromedriver", dest="chromedriver", default="chromedriver",
                     help="Location of Chromedriver Installation (Default= chromedriver)")

(opts, _) = optparser.parse_args()

# Provide the path of the csv file containing the keywords
keyword_file = pd.read_csv(opts.file)
Scrape_from_file(keyword_file, Images_per_category=int(opts.num_images), Download_Folder=opts.output_folder,
                 Image_Size=opts.size, delay=int(opts.delay), chromedriver_location=opts.chromedriver)
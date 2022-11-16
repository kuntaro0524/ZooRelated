import glob
import os

img_path_list = glob.glob("*/raster.jpg")
img_path_list = sorted(img_path_list)

header_info = """
<!DOCTYPE html>
 <html>
 <head>
 <meta charset="UTF-8">

 <style>
 .dataset_table {
     font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
     width: 100%%;
     border-collapse: collapse;
 }

 .dataset_table td, .dataset_table th {
     font-size: 1em;
     border: 1px solid #FF49AD;
     text-align: center;
     padding: 3px 7px 2px 7px;
 }

 .dataset_table th {
     font-size: 1.1em;
     text-align: center;
     padding-top: 5px;
     padding-bottom: 4px;
     background-color: #FF49AD;
     color: #ffffff;
 }

 .dataset_table tr.alt td {
     color: #000000;
     background-color: #EAF2D3;
 }
 .dataset_table tr.alt td {
     color: #000000;
     background-color: #EAF2D3;
 }
 .mygif img{
     width: 300px;
     height: 300px;
 }
</style>
<h2> Check 'raster.jpg' </h2>

<table class="dataset_table">
<tr>
<th> Puck-Pin ID </th>
<th> Raster.jpg </th>
</tr>
"""

html_str = header_info
for img_path in img_path_list:
    puck_pin = img_path.split("/")[0]
    img_relpath = os.path.relpath(img_path, ".")
    html_str += """<tr><td>%s</td><td><img src="%s"></td></tr>""" % (puck_pin, img_relpath)


html = "check_rasterJPG.html"

with open(html, "w") as f:
    f.write(html_str)


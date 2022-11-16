#!/bin/bash

imgfiles=`find . -name 'raster.jpg'`

for imgfile in $imgfiles; do
echo "<h1>$imgfile</h1>"
echo "<a href="show"><img src="$imgfile"></a>"
done

#!/bin/bash

imgfiles=`cat wrong_images.log`

for imgfile in $imgfiles; do
echo "<h1>$imgfile</h1>"
echo "<a href="show"><img src="$imgfile"></a>"
done


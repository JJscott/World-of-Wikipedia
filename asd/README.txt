Reading Points in Shapes
>>> import shapefile
>>> sf = shapefile.Reader("shapefiles/blockgroups")
>>> shapes = sf.shapes()
>>> # Read the bounding box from the 4th shape
>>> shapes[3].bbox
	[-122.485792, 37.786931000000003, -122.446285, 37.811019000000002]
>>>#  Read the 8th point in the 4th shape
>>> shapes[3].points[7]
	[-122.471063, 37.787402999999998]
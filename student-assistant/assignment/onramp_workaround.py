# Workaround for 
regions = ["us-central1", "us-central1",]

last_region_used=0
#create a function that looks at the last last_region_used and return the next region from regions, if there no more at the end, move to the begining 
def get_next_region():
    global last_region_used 
    last_region_used = (last_region_used + 1) % len(regions)
    return regions[last_region_used]

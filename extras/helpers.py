# %%
import pystac_client
import planetary_computer
#import odc.stac
import matplotlib.pyplot as plt
from pystac.extensions.eo import EOExtension as eo

# %%
def get_catalog():
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )
    return catalog
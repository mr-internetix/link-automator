# imports
from enum import Enum


# Enum for browser configs
# If you want to change change browser config or orientation change this enum class

class BrowserConfig(Enum):
    ''' ALL ENUMS HERE '''
    browser_width = "1920"
    browser_height = "1080"
    browser_type = "--headless"


class Links(Enum):
    ''' Links for tesing'''
    cortex = "https://enter.ipsosinteractive.com/landing/?rType=0&id=&ci=en-us&pid=S23007177&redirectStage=1&routerID=78&supplierID=1090&surveyid=882325&testCortex=1"
    main_script = "https://staging01.ipsosinteractive.com/surveys/25b6acb2-de68-11e2-a28f-0800200c9a66"


if __name__ == "__main__":
    pass
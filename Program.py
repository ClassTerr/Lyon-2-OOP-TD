import pandas as pd

from ConsoleUI import ConsoleUI

pd.set_option('display.max_rows', 1500)
pd.set_option('display.max_columns', 1500)
pd.set_option('display.width', 1500)

ui = ConsoleUI()

ui.start()

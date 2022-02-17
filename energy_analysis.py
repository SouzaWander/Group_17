from urllib.request import urlretrieve
import os  # we want python to be able to read what we have in our hard drive

import pandas as pd

class EnergyAnalysis:
    def __init__(self, url, output_file):
        print("here")
        self.url = url
        self.output_file = output_file

    def download_file(self):
        """
        Downloads a file from an URL into your hard drive.

        Parameters
        ------------
        file_link: str
            A string containing the link to the file you wish to download.
        output_file: str
            A string containing the name of the output file. The default value is 'file.csv'
            at the location you are running the function.

        Returns
        ---------
        Nothing


        Example
        ---------
        download_file("https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip", output_file='student.zip')
        """

        # If file doesn't exist, download it. Else, print a warning message.
        if not os.path.exists(self.output_file):
            urlretrieve(self.url, filename=self.output_file)
        else:
            print("File already exists!")


object = EnergyAnalysis(
    "https://nyc3.digitaloceanspaces.com/owid-public/data/energy/owid-energy-data.csv",
    "energy_data.csv",
)
object.download_file()

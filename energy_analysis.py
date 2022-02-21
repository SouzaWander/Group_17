from urllib.request import urlretrieve
import os  # we want python to be able to read what we have in our hard drive

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


class EnergyAnalysis:
    def __init__(self, url, output_file):
        self.url = url
        self.output_file = output_file
        self.df = None

    # method 1 --> download file and read the csv to df attribute the pandas dataframe.
    def download_file(self):
        """
        Downloads a file from the object.url address into your hard drive and read the dataset into the df attribute which it is a pandas dataframe.

        Parameters
        -----------

        Returns
        ---------
        Nothing


        Example
        ---------
        object.download_file()
        """
        try:
            # If file doesn't exist, download it. Else, print a warning message.
            fullfilename = os.path.join("./downloads/" + self.output_file)
            if not os.path.exists(fullfilename):
                print(urlretrieve(self.url, filename=fullfilename))
            else:
                print("File already exists!")

            self.df = pd.read_csv(fullfilename)
            self.df = self.df[(self.df["year"] >= 1970)]
        except Exception:
            raise Exception("Error 404") from Exception

from urllib.request import urlretrieve
import os  # we want python to be able to read what we have in our hard drive

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


class EnergyAnalysis:
    """
    Class that controls all class methods and finally
    delivers the requested information.
    It analyses energy data.

    Attributes
    ----------------
    url: str
        The url for the requested file
    output_file: str
        Desired name to the file
    df: pandas.DataFrame
        The padas dataframe with the content of the file downloaded

    Methods
    ----------------
    __init__: Init method
        Class constructor to inizialize the attributes of the class.
    """

    def __init__(self, url: str, output_file: str):
        self.url = url
        self.output_file = output_file
        self.df = None

    # method 1 --> download file and read the csv to df attribute the pandas dataframe.
    def download_file(self):
        """
        Downloads a file from the object.url address into your hard drive and read the dataset into the df attribute which it is a pandas dataframe.

        Parameters
        -----------
        None


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

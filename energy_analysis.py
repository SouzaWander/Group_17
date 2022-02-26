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

    download_file: Download method
        Download a file base on the url strored in the object of the class,
        and reurns a pandas dataframe with the data
    """


    def __init__(self, url: str, output_file: str):
        """
        Class constructor to inizialize the attributes of the class.

        Parameters
        ----------------
        url: str
            The url for the requested file
        output_file: str
            The name of the output file
        df: pandas dataframe
            The columns included in the correlation matrix
        """

        self.url = url
        self.output_file = output_file
        self.df = None


    #method 1 --> download file and read the csv to df attribute the pandas dataframe.
    def download_file(self):
        """
        Downloads a file from the object.url address into your hard drive and read the dataset into the df attribute which it is a pandas dataframe.

        Parameters
        -----------
        None


        Returns
        ---------
        dataset: pandas dataframe


        Example
        ---------
        object.download_file()
        """
        try:
            # If file doesn't exist, download it. Else, print a warning message.
            fullfilename = os.path.join("./downloads/"+self.output_file)
            if not os.path.exists(fullfilename):
                print(urlretrieve(self.url, filename=fullfilename))
            else:
                print("File already exists!")

            self.df = pd.read_csv(fullfilename)
            self.df = self.df[(self.df["year"] >= 1970)]
        except Exception:
            raise Exception("Error 404") from Exception

    # method 2 --> list all the available countries
    def list_countries(self):
        """
        Returns a list of all available countries in the dataset

        Parameter
        ----------------
        None

        Raises
        -----------------
        None

        Returns
        -----------------
        Array
        """
        region_list = ['Africa','Asia Pacific','CIS','Central America',
       'Eastern Africa','Europe', 'Europe (other)','Middle Africa',
       'Middle East',
       'North America', 'OPEC',
       'Other Asia & Pacific', 'Other CIS', 'Other Caribbean',
       'Other Middle East', 'Other Northern Africa',
       'Other South America', 'Other Southern Africa',
       'South & Central America','USSR','Western Africa', 'Western Sahara',
       'World']
        return self.df[(~self.df["country"].isin(region_list))].country.unique()

    # method 3 -->
    def show_consumption(self, country:str , normalize:bool):
        """
        Plots the normalized or not normalized consumptions of the past years of a given country.

        Parameter
        ----------------
        country: str
        Name of the country that we want to analyze the consumption.

        normalize: bool
        Option if we want or not to normalize the consuption data.

        Raises
        -----------------
        ValueError
        If the country is not present on teh dataset

        Returns
        -----------------
        None
        """
        if country in self.list_countries():
            aux = self.df[(self.df["country"] == country)]
            # selects the "_consumption" columns
            cols = [col for col in self.df.columns if "_consumption" in col]

            aux = aux.fillna(value=0)

            norm = aux[cols]
            norm
            # normalize the consumptions values to percentages
            if(normalize):
                norm[cols] = norm[cols].apply(lambda x: (x / x.sum()) * 100, axis=1)
            x = norm
            x["year"] = aux["year"]
            # plot
            plt.style.use("seaborn")
            x.plot.area(x="year")
            plt.show()
        else:
            raise ValueError("Country does not exist.")

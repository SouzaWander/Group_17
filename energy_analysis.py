from urllib.request import urlretrieve
import os  # we want python to be able to read what we have in our hard drive

import pandas as pd

from matplotlib import cm
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

    def __init__(self):
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

        self.url = "https://nyc3.digitaloceanspaces.com/owid-public/data/energy/owid-energy-data.csv"
        self.output_file = "energy_data.csv"
        self.df = None
        self.download_file()

    # method 1 --> download file and read the csv to df attribute the pandas dataframe.
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
        fullfilename = os.path.join("./downloads/" + self.output_file)
        if not os.path.exists("./downloads/"):
            os.makedirs("./downloads/")
            urlretrieve(self.url, filename=fullfilename)
        elif not os.path.exists(fullfilename):
            urlretrieve(self.url, filename=fullfilename)
        else:

            print("File already exists!")
        try:
            # If file doesn't exist, download it. Else, print a warning message.

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
        region_list = [
            "Africa",
            "Asia Pacific",
            "CIS",
            "Central America",
            "Eastern Africa",
            "Europe",
            "Europe (other)",
            "Middle Africa",
            "Middle East",
            "North America",
            "OPEC",
            "Other Asia & Pacific",
            "Other CIS",
            "Other Caribbean",
            "Other Middle East",
            "Other Northern Africa",
            "Other South America",
            "Other Southern Africa",
            "South & Central America",
            "USSR",
            "Western Africa",
            "Western Sahara",
            "World",
        ]
        return self.df[(~self.df["country"].isin(region_list))].country.unique()

    # method 3 -->
    def show_consumption(self, country: str, normalize: bool):
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
            aux = aux[(aux["year"] <= 2019)]
            # selects the "_consumption" columns
            cols = [col for col in self.df.columns if "_consumption" in col]
            cols.remove("renewables_consumption")
            cols.remove("fossil_fuel_consumption")
            cols.remove("primary_energy_consumption")

            aux = aux.fillna(value=0)

            norm = aux[cols]
            # normalize the consumptions values to percentages
            if normalize:
                norm[cols] = norm[cols].apply(lambda x: (x / x.sum()) * 100, axis=1)
            x = norm
            x["year"] = aux["year"]
            # plot
            plt.style.use("seaborn")
            x.plot.area(x="year", cmap=cm.get_cmap("Paired"))
            plt.title("Consumption in " + country, fontsize=14)
            plt.xlabel("Year", fontsize=14)
            plt.ylabel("Consumption", fontsize=14)
            plt.show()
        else:
            raise ValueError("Country does not exist.")

    # method 4 -->
    def consumption_country(self, countries: str):
        """
        Select the Countries, sum up the total per year and plot it

        Parameters
        ------------
        countries: list
            A list with all countries to be analyzed

        Returns
        ---------
        Plot with consumption and countries


        Example
        ---------
        object.consumption_country(["Switzerland", "Portugal", "Chile"])
        """

        # Create a list with all _consumption columns and create a new dataframe
        consumption_list = self.df.filter(like="_consumption").columns
        consumption_data = self.df[
            [
                "country",
                "year",
                "biofuel_consumption",
                "coal_consumption",
                "fossil_fuel_consumption",
                "gas_consumption",
                "hydro_consumption",
                "low_carbon_consumption",
                "nuclear_consumption",
                "oil_consumption",
                "other_renewable_consumption",
                "primary_energy_consumption",
                "renewables_consumption",
                "solar_consumption",
                "wind_consumption",
            ]
        ]

        # calculate the sum of all consumption per year
        consumption_data["total"] = consumption_data[consumption_list].sum(axis=1)

        # Create a dataframe for every country needed and drop NaN
        for i in countries:
            globals()[i] = consumption_data[consumption_data["country"] == i]
            indexNames = globals()[i][globals()[i]["total"] < 1].index
            globals()[i].drop(indexNames, inplace=True)

        # plot the total consumption
        for i in countries:
            plt.plot(globals()[i]["year"], globals()[i]["total"], label=i)
        plt.title("Consumption per Year", fontsize=14)
        plt.xlabel("Year", fontsize=14)
        plt.ylabel("Total Consumption", fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.show()

    # method 5 -->
    def gdp_country(self, countries: str):
        """
        Select the Countries, and plot the gdp over the years

        Parameters
        ------------
        countries: list
            A list with all countries to be analyzed

        Returns
        ---------
        Plot with gdp and countries


        Example
        ---------
        object.gdp_country(["Switzerland", "Portugal", "Chile"])
        """

        # Select the columns Country, Year and gdp and create a new dataframe
        gdp_data = self.df[["country", "year", "gdp"]]

        # Create a dataframe for every country needed and drop NaN
        for i in countries:
            globals()[i] = gdp_data[gdp_data["country"] == i]
            gdp_data.dropna(subset=["gdp"], inplace=True)

        # plot the total consumption
        for i in countries:
            plt.plot(globals()[i]["year"], globals()[i]["gdp"], label=i)
        plt.title("GDP per Year", fontsize=14)
        plt.xlabel("Year", fontsize=14)
        plt.ylabel("GDP per Year", fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.show()

    # method 6 -->
    def gapminder(self, y: int):

        """
        Plots a scatter Plot comparing the Gdp of each country and its Total Energy Consumption of a given year.
        The population of each country can also be compared by the size of the data points.

        Parameter
        _______________

        year: int
        Year that we want to analyse countries' GDP and Total Energy Consumption


        Raises
        -----------------
        ValueError
        If the input given is not an 'int'

        Returns
        -----------------
        Scatter plot

        """

        # From the Dataset only the columns of the problem were Selected
        dataframe = self.df.filter(regex="year|country|population|consumption|gdp")

        total_consumption = dataframe[list(dataframe.filter(regex='_consumption'))].sum(axis=1)
        dataframe = dataframe.assign(total_consumption=total_consumption.values)

        # Define the size of the plot for better visualization
        fig = plt.figure(figsize=(20, 15))

        year = dataframe[dataframe["year"] == y]

        if type(y) != int:
            raise TypeError("Variable 'y' is not int.")

        else:

            # x-axis values
            x = year["gdp"]
            # y-axis values
            y = year["total_consumption"]
            p = year["population"]
            # size = [2*n for n in range(len(p))]
            size = year["population"]

            # plotting points as a scatter plot
            plt.scatter(
                x,
                y,
                label="Population Size",
                edgecolors="black",
                marker="o",
                lw=1,
                c=year.population,
                s=year.population / 2 ** 18,
            )

            plt.colorbar(label="Total Energy Consumption", shrink=1)
            plt.tick_params(labelsize=20)

            # x-axis label
            plt.xlabel("GDP", fontsize=20)
            # x-axis label
            plt.ylabel("Total Energy Consumption", fontsize=20)
            # plot title
            plt.title(
                "Countries GDP and Energy Consumption in a given Year", fontsize=20
            )

            # Editing the Legend
            pws = [500000, 10000000, 100000000, 1000000000]
            for pw in pws:
                plt.scatter(
                    [], [], s=pw / 2 ** 18, c="k", label=str(pw), cmap="viridis"
                )

            h, l = plt.gca().get_legend_handles_labels()
            plt.legend(
                h[1:],
                l[1:],
                labelspacing=1.9,
                title="Population",
                borderpad=0.9,
                frameon=True,
                framealpha=0.6,
                edgecolor="blue",
                facecolor="lightblue",
                fontsize=20,
                title_fontsize=25,
            )

            # Change the X and Y axis scale for better visualization
            plt.xscale("log")
            plt.yscale("log")

            plt.grid()

            # function to show the plot

            f = plt.show()

        return f

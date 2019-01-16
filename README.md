# Weather prediction (IN PROGRESS)
Using a Machine Learning model, try to predict weather temperatures.

Steps so far accomplished:
1. Aquired daily historical weather dataset from Open Weather for the city of Kyoto, Japan (between January 1, 2017 and December 31, 2018)
2. Extracted paramenters from JSON file, such as Temperature, Max Temperature, Min Temperature, Humidity, Atm Pressure, Wind Speed.
3. Converted all temperatures from Kelvin into Celsius, this step was necessary in order to calculate Dew Point Temperatures in the next step.
4. Calculated Dew Point Temperatures.
5. Checked for linearity of features to decide which features to utilize in the model.

### Tools/Resources
Python: Pandas, Sklearn, Numpy
File type: JSON 
Source: www.openweathermap.org

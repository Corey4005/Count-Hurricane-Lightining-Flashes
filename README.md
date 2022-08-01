# Count-Hurricane-Lightining-Flashes
Welcome to the Count-Hurricane-Lightning-Flashes repo!

This repo contains the tools needed to count lightning flash events between two hurricane time-event points. The code assumes that the speed of the hurricane is the same throughout and that it follows a straight line, which is interpolated by the assumed speed of the hurricane over an observation time-interval. 

Check out [main.py](./src/main.py), which shows how 17 lines of code can be used to download a large set of files automatically (in this case 540 netCDFs) via the Amazon Web Service (AWS) Command Line Interface (CLI) and analyzed to produce a plot of lightning count flashes over hurricane Ana in 2021. 

Here is an example of the plot that is returned of that 3 hour period:

<p align="center">
  <img src=./src/plots/HurricaneAnaExample.png
</p>

x-axis is time and y axis is the flash counts. 

Here is an image showing how interpolation points are generated between two storm-event-times:

<p align="center">
  <img src=./src/plots/interpolationExample.png
</p>

x axis is longitude and y axis is latitude. 

Note: The box size used to count a lightning event is 111km x 111km or ~1 degree in latitude and longitude from each point along the interpolated storm-event line. 

To use this software follow these steps: 

1. Install aws-cli version 2.7.19.

* The docs for installing a specific version is found [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-version.html)

2. Configure aws-cli with the appropriate fields. 

* The docs for configurating aws-cli with your secret keys are found [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html). If you do not already have an AWS account with IAM credentials, follow [these](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html) steps. 

3. Install the following packages using a command line:

```bash
pip install pandas==1.0.5, geopy==2.2.0, numpy==1.21.2, matplotlib==3.5.0, netCDF4==1.5.7
```

4. Run [main.py](./src/main.py) via the command line or from an interactive development environment. 
```python
python main.py
```
[main.py](./src/main.py) can be easily updated with a different parameters to count flashes over a different storm event. Or, because this is an object-oriented program, you could download an entire storm track [here](https://coast.noaa.gov/hurricanes/#map=4/32/-80) and generate giant dataframes of lightning flash data using a simple for loop. I intend to upload a file later showing how this can be done, so press that star button and follow along!

# This program scrapes weather data for the region for the week
# It then prints the information to the console as well as creating a text file of the data.
# Import needed libraries
from bs4 import BeautifulSoup as bs
import requests
from time import gmtime, strftime

# Set up browser information
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"

# getWeatherData extracts all weather information and return it as a library
# url Url to be used
def getWeatherData(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)
    # create a new soup
    soup = bs(html.text, "html.parser")

    # Storing all of the information
    result = {}
    # Region
    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    # Temperature
    result['temp'] = soup.find("span", attrs={"id": "wob_tm"}).text
    # Day and hour
    result['dayHour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    # Actual weather
    result['actWeather'] = soup.find("span", attrs={"id": "wob_dc"}).text
    # Precipitation
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    # Humidity
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    # Wind
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text

    # Get next few days weather
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        # Day name
        dayName = day.find("div", attrs={"class": "QrNVmd"}).attrs['aria-label']
        # get weather status for that day
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        # maximum temparature in fahrenheit (temp[1] for cel)
        maxTemp = temp[0].text
        # minimum temparature in fahrenheit (temp[3] for cel)
        minTemp = temp[2].text
        next_days.append({"name": dayName, "weather": weather, "maxTemp": maxTemp, "minTemp": minTemp})
    # append to result
    result['nextDays'] = next_days
    return result


if __name__ == "__main__":
    URL = 'https://www.google.com/search?client=firefox-b-1-d&q=google+weather'
    import argparse
    parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
    parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                        Default is your current location determined by your IP Address""", default="")
    # Parse arguments
    args = parser.parse_args()
    region = args.region
    URL += region
    # Get data
    data = getWeatherData(URL)

# Print data
print("Weather for:", data["region"])
print("Now:", data["dayHour"])
print(f"Temperature now: {data['temp']}°F")
print("Description:", data['actWeather'])
print("Precipitation:", data["precipitation"])
print("Humidity:", data["humidity"])
print("Wind:", data["wind"])
print("Next days:")
for dayweather in data["nextDays"]:
    print("="*40, dayweather["name"], "="*40)
    print("Description:", dayweather["weather"])
    print(f"Max temperature: {dayweather['maxTemp']}°F")
    print(f"Min temperature: {dayweather['minTemp']}°F")

# Write data to file
actualTime = strftime("%Y-%m-%d %H-%M-%S", gmtime())
file = open("weather - " + str(actualTime) + ".txt", "w")
line = ["Weather for:", data["region"], "\n"]
file.writelines(line)
line = ["Now:", data["dayHour"], "\n"]
file.writelines(line)
line = [f"Temperature now: {data['temp']}°F", "\n"]
file.writelines(line)
line = ["Description:", data['actWeather'], "\n"]
file.writelines(line)
line = ["Precipitation:", data["precipitation"], "\n"]
file.writelines(line)
line = ["Humidity:", data["humidity"], "\n"]
file.writelines(line)
line = ["Wind:", data["wind"], "\n"]
file.writelines(line)
line = ["Next days:", "\n"]
file.writelines(line)
for dayweather in data["nextDays"]:
    line = ["="*40, dayweather["name"], "="*40, "\n"]
    file.writelines(line)
    line = ["Description:", dayweather["weather"], "\n"]
    file.writelines(line)
    line = [f"Max temperature: {dayweather['maxTemp']}°C", "\n"]
    file.writelines(line)
    line = [f"Min temperature: {dayweather['minTemp']}°C", "\n"]
    file.writelines(line)

file.close()
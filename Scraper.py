from lxml import html
import requests
import ctypes  # for MessageBoxW
import datetime
import JobsRepository

curDate = datetime.datetime.now().date()
range = 20

repo = JobsRepository.JobsRepository("C:\\temp\\JobsDatabase.db")

cities = repo.getAllCities()
jobs = repo.getAllJobDescriptions()

for city in cities:
    print(city.ToUrlString())
for job in jobs:
    print(job.ToUrlString())


def getNumberOfResultsForCityAndJob():
    requestUrl = 'https://careers.stackoverflow.com/jobs?searchTerm=' + job.ToUrlString() + '&location=' + city.ToUrlString() + '&range=' + str(
        range) + '&distanceUnits=Miles'
    page = requests.get(requestUrl)
    tree = html.fromstring(page.text)
    resultsDiv = tree.xpath('//div[@id="index-hed"]/h2/span/text()')
    return (resultsDiv[0].split(" ")[0])


for city in cities:
    for job in jobs:
        jobsInCity = getNumberOfResultsForCityAndJob()
        repo.insertOrUpdateJobResults(curDate, city, job, jobsInCity)

repo.close()

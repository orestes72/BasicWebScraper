from lxml import html
import requests
import ctypes  # for MessageBoxW
import datetime
import JobsRepository

RESULTS_XPATH = '//div[@id="index-hed"]/h2/span/text()'



curDate = datetime.datetime.now().date()
range = 20

repo = JobsRepository.JobsRepository("C:\\temp\\JobsDatabase.db")

repo.deleteAllJobResultsOnDate(curDate)
cities = repo.getAllCities()
jobs = repo.getAllJobDescriptions()

def getNumberOfResults(dom):
    resultsDiv = dom.xpath('//div[@id="index-hed"]/h2/span/text()')
    return (resultsDiv[0].split(" ")[0])

def getCompanyNames(dom):
    companies = []
    companyTags = dom.xpath('//strong[@class="-employer"]')
    for company in companyTags:
        companies.extend([company.text])
    return (companies)

def getDomTreeForCityAndJobSearch():
    requestUrl = 'https://careers.stackoverflow.com/jobs?searchTerm=' + job.ToUrlString() + '&location=' + city.ToUrlString() + '&range=' + str(range) + '&distanceUnits=Miles'
    page = requests.get(requestUrl)
    tree = html.fromstring(page.text)
    return tree

for city in cities:
    for job in jobs:
        dom = getDomTreeForCityAndJobSearch()
        jobsInCity = getNumberOfResults(dom)
        repo.insertOrUpdateJobResults(curDate, city, job, jobsInCity)
        companies = getCompanyNames(dom)
        for company in companies:
            repo.insertCompany(city,job,company)
repo.close()


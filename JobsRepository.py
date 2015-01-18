__author__ = 'John'
import sqlite3
import urllib

class JobsRepository:
    def __init__(self, filename="JobsDatabase.db"):
        self.conn = sqlite3.connect(filename)  #Once you have a Connection, you can create a Cursor object and call its execute() method to perform SQL commands:
        self.c = self.conn.cursor()

    def deleteAllJobResultsOnDate(self, date):
        self.c.execute('DELETE FROM JobsPerCityAndKeyword WHERE date = :date', {"date":date})
        self.conn.commit()

    def getAllCities(self):
        cities = []
        for row in self.c.execute('SELECT cityId, cityName, stateInitials FROM City order by stateInitials'):
            city = CityModel(int(row[0]),row[1],row[2])
            cities.extend([city])
        return cities

    def getAllJobDescriptions(self):
        jobs = []
        for row in self.c.execute('SELECT jobKeywordId, keywordName FROM JobKeyword order by keywordName'):
            job = JobModel(int(row[0]),row[1])
            jobs.extend([job])
        return jobs

    def getAllJobsPerCity(self, city, jobType):
        results = []
        for row in self.c.execute('select jc.date, c.cityname, c.stateInitials, j.keywordname, jc.numberofjobs from city c, jobkeyword j, jobspercityandkeyword jc where jc.cityid = c.cityid and jc.jobkeywordid = j.jobkeywordid and c.cityname = :city and j.keywordName = :keyWord  order by jc.date asc', {"city":city.cityName, "keyWord":jobType.keywordName}):
            result = JobSearchModel(row[0], row[1], row[2], row[3], int(row[4]))
            results.extend([result])
        return results

    def insertOrUpdateJobResults(self, date, city, job, numJobs):
        self.c.execute('INSERT INTO JobsPerCityAndKeyword (date, cityId, jobKeywordId, numberOfJobs) VALUES (:date, :cityId, :jobKeywordId, :numberOfJobs)', {"date":date, "cityId":city.cityId, "jobKeywordId":job.jobKeywordId, "numberOfJobs":numJobs})
        #self.c.execute('IF NOT EXISTS (SELECT 1 FROM JobsPerCityAndKeyword WHERE date = :date AND cityId = :cityId and jobKeywordId = :jobKeywordId) BEGIN 	INSERT INTO JobsPerCityAndKeyword (date, cityId, jobKeywordId, numberOfJobs)  	VALUES (:date, :cityId, :jobKeywordId, :numberOfJobs) END ELSE  	UPDATE JobsPerCityAndKeyword SET numberOfJobs = :numberOfJobs WHERE date = :date AND cityId = :cityId and jobKeywordId = :jobKeywordId 	', {"date":date, "cityId":city.cityId, "jobKeywordId":job.jobKeywordId, "numberOfJobs":numJobs})
        self.conn.commit()

    def insertCompany(self, city, job, name):
        self.c.execute('DELETE FROM Company WHERE cityId = :cityId AND jobKeywordId = :jobKeywordId AND companyName = :companyName', {"cityId":city.cityId, "jobKeywordId": job.jobKeywordId, "companyName":name})
        self.c.execute('INSERT INTO Company (cityId, jobKeywordId, companyName) VALUES (:cityId, :jobKeywordId, :companyName)', {"cityId":city.cityId, "jobKeywordId": job.jobKeywordId, "companyName":name})
        self.conn.commit()


    def close(self):
        self.conn.commit()
        self.conn.close()

class CityModel:
    def __init__(self, cityId, cityName, stateInitials):
        self.cityId = cityId
        self.cityName = cityName
        self.stateInitials = stateInitials
    def __str__(self):
        return str(self.cityId) + " " + self.cityName + ' ' + self.stateInitials
    def ToUrlString(self):
        return urllib.parse.quote_plus(self.cityName + ' ' + self.stateInitials)

class JobModel:
    def __init__(self, jobKeywordId, keywordName):
        self.jobKeywordId = jobKeywordId
        self.keywordName = keywordName
    def __str__(self):
        return str(self.jobKeywordId) + " " + self.keywordName
    def ToUrlString(self):
        return urllib.parse.quote_plus(self.keywordName)


class JobSearchModel:
    def __init__(self, date, cityName, stateInitials, keywordName, numberOfJobs):
        self.date = date
        self.cityName = cityName
        self.stateInitials = stateInitials
        self.keywordName = keywordName
        self.numberOfJobs = numberOfJobs

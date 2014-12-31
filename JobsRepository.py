__author__ = 'John'
import sqlite3
import re
import urllib

class JobsRepository:
    def __init__(self, filename="JobsDatabase.db"):
        self.conn = sqlite3.connect(filename)  #Once you have a Connection, you can create a Cursor object and call its execute() method to perform SQL commands:
        self.c = self.conn.cursor()

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

    def insertOrUpdateJobResults(self, date, city, job, numJobs):
        #self.c.execute('INSERT INTO JobsPerCityAndKeyword (date, cityId, jobKeywordId, numberOfJobs) VALUES (:date, :cityId, :jobKeywordId, :numberOfJobs)', {"date":date, "cityId":city.cityId, "jobKeywordId":job.jobKeywordId, "numberOfJobs":numJobs})
        self.c.execute('IF NOT EXISTS (SELECT 1 FROM JobsPerCityAndKeyword WHERE date = :date AND cityId = :cityId and jobKeywordId = :jobKeywordId) BEGIN 	INSERT INTO JobsPerCityAndKeyword (date, cityId, jobKeywordId, numberOfJobs)  	VALUES (:date, :cityId, :jobKeywordId, :numberOfJobs) END ELSE  	UPDATE JobsPerCityAndKeyword SET numberOfJobs = :numberOfJobs WHERE date = :date AND cityId = :cityId and jobKeywordId = :jobKeywordId 	', {"date":date, "cityId":city.cityId, "jobKeywordId":job.jobKeywordId, "numberOfJobs":numJobs})
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

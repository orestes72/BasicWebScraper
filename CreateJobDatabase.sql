CREATE TABLE JobKeyword(
	jobKeywordId INT PRIMARY KEY NOT NULL,
	keywordName CHAR(50)
);

CREATE TABLE City(
	cityId INT PRIMARY KEY NOT NULL,
	cityName CHAR(50),
	stateInitials CHAR(2)
);

CREATE TABLE JobsPerCityAndKeyword(
	date DATE, 
	cityId integer, 
	jobKeywordId integer, 
	numberOfJobs integer,
	FOREIGN KEY(jobKeywordId) REFERENCES JobKeyword(jobKeywordId),
	FOREIGN KEY(cityId) REFERENCES City(cityId)
);







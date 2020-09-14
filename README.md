# [#CloudGuruChallenge](https://acloudguru.com/blog/news/introducing-the-cloudguruchallenge)
## [Event-Driven Python on AWS](https://acloudguru.com/blog/engineering/cloudguruchallenge-python-aws-etl)

- [ ] ETL Job - Create a job that runs once a day to perform some task
- [ ] Extraction - Load the data from [this](https://github.com/nytimes/covid-19-data/blob/master/us.csv?opt_id=oeu1598130766489r0.9183835738508552) CSV into an object in memory
- [ ] Transformation - Perform data manipulations
    - Cleaning
    - Joining with [this](https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv?opt_id=oeu1598130766489r0.9183835738508552) csv
    - Filtering (to remove non-US stats)
- [ ] Code cleanup - Move data manipulation into a python module
- [ ] Load - Load transformed data into a DB
- [ ] Notification - Notify using SNS that the ETL job is complete
- [ ] Error handling - Handle the following:
    - Initial load versus update
    - Notify if the data is malformed
- [ ] Tests - Unit test the code
- [ ] IaC - Use IaC to bring up infrastructure
- [ ] Source Control - Store code in Github
- [ ] Dashboard - Report the data using some visualisation/BI tool
- [ ] Blog Post - Post about the experience and challenges
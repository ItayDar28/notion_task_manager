# notion_task_manager

In order to arrange my time in the most efficient way, throughout the exam period, I build a task manager and a time tracker that helps me knows how I spend my time each day. It is funny to realize that I'm spending almost 20% of my time on housekeeping tasks.

In order to collect the relevant data, I created a notion table that contains several tasks that cover almost everything that I'm doing during my day, such as shower, dishwashing, studying, sport and etc. 

To this frontend table i create a connection to a mysql database using the api of notion and sqlalchemy orm library.

With this data, that I collect day-by-day, I will be able to get a good understanding of how my time is being spent and may have changed the way I choose to spend it.

this is how the table is looks like:

by pressing start on some task, the crawler is adding the task to a python dictionary and when press on finish, the data is being sent straight into mysql database with all the relevant data.

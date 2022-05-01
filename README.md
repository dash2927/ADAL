# Recipeezy

## Project Video

https://youtu.be/z3xI3RSsC04

## Project Presentation

https://cdn-uploads.piazza.com/paste/kjxdp5zv62l45q/25543021b4133657d5f225efb7f08fcd18f8398568c646178bd05bd5db925ea9/Recipeezy_Presentation.pdf

## Team Members

* Luis Mendoza
* Alex Plazas
* David Shackelford
* Adhir Uchil

## Vision

Recipeezy is a website which will collect and organize recipes from around the world. This will give people the opportunity to share their own personal or family recipes, while also exploring different foods and finding new ideas for their culinary adventure. 

**Use Cases**:
  
<ins>Main Use Cases</ins>:

:mag: **Recipe Lookup** - The user will be able to look up recipes based on a wide range of input criteria.

:inbox_tray: **Recipe Submission** - The user will be able to submit their own recipe utilizing a simple user interface 

:+1: **Voting System** - The user will be allowed to vote on other people's recipes, which affect an accumilated "score" for the recipe and will affect the order that the recipe appears when doing a recipe lookup.
  
<ins>Expanded/Potential Use Cases</ins>:

:bread: **Pantry List** - Will recommend recipes to use based on ingredients you list

:heavy_check_mark: **Recommendation System** - Recipes will be recommended to the user based on what they vote for

:calendar: **Recipe of the Day** - Every day users will be sent a new recipe to try based on set preferences

:runner: **Calorie Tracker** - Track your calories/macros and suggest recipes that will help you meet your goals

## Motivation
At some point we've all experienced searching for that perfect recipe. Even if you do find 'the one', it usually comes after a wall of text wherein the author explains how this recipie was their great-grandmother's-aunt's-brother's favorite meal after a hard day on the farm. Our team wishes to simplify the recipe discovery process by delivering an experience built around the aspiring home chef. The motivation behind this project is our desire to make a system where our friends and family can share recipes with each other. We think that it will be engaging and useful to include a rating system for each recipe in a similar manner to the popular social website, Reddit.com. 

## To Run

**To run recipeezy locally:** 

1. Fork/clone the github repo. 
2. Create a new virtual environment
3. `pip install -r requirements.txt`
4. `python wsgi.py`
5. Go to local host listed on console

Alternatively, you can visit http://recip-eezy.herokuapp.com/ to see/use the public app.

# Other information about this project:

This project was created for the CU Boulder Post-Baccaleureate degree program for Applied Computer Science. The following categories detail our development process:

## Risks

* **New language** - We will be working with javascript which not everyone in our group has worked with yet. This produces two challenges. One is that some people might not be able to do certain tasks. Another is that our team might have an uneven level of experience, possibly making it so certain team members have to do more work to complete a project feature.
* **Availability of API** - Upon the initial concept of this project, we will probably not need to utilize a separate API. However, in the future we may find that we have to get one to either reduce workload or because the task is too complicated to code something from scratch. This creates a risk where we would need to ensure the API works and that the API can perform the task needed.
* **IP Blocking** - If we choose to use an API (maybe to webscrape recipes and build a collection of recipes), we need to be careful about how many times we send a request. This can lead to IP blocking which means that if we send too many requests, the receiving party can block any more requests from the IP. This is a problem that could potentially slip through testing.
* **Team coordination** - Team coordination is extremely important. Some team members are in completely different time zones. While this is easily manageable, it may create a potential challenge as the project progresses with coordinating times to meet and with meeting important deadlines.
* **Getting initial recipe data** - In order to fully test our project, we need a database that is already populated with recipes. Therefore, one risk that may come up is that we will need to be able to find a database which has enough data entries and has features that line-up with our project scope.
* **Scope** - The final goal of this project will to have a feature-rich system that will allow users to do many different tasks. Our team runs the risk of adding too many features in the short amount of time we are given, which could cause our team to become overwhelmed.

## Mitigation Strategy

* **New language** - This risk can be mitigated by utilyzing good project management. Ensuring that certain group memebers work on things they are either very interested in, or know a lot about can ensure every group memeber contributes enough to the entire project. We will also have consistant check-ins to ensure every member is working on something useful.
* **Availability of API** - To mitigate this risk, we will go through a tech analysis process before we choose an API to use. We will weigh pros/cons, and determine if it will be useful for our project. The risk of having a problem with an API is fairly low since our original idea probably wont require the use of an API.
* **IP Blocking** - This will be mitigated through test driven development. If we use some sort of tool that requires requests, we will ensure that multiple requests wont impact performance.
* **Team coordination** - To reduce any problems with team coordination, we will maintain constant contact through Discord and Notion. We will do our best to accomindate all group member's optimal times by setting major meetings in either the early morning or late evening. For deadlines, we will practice good time management skills and ensure that everyone knows before-hand task timelines and create an understanding when each member needs to hand-off their work.
* **Getting initial recipe data** - Early in development, we will conduct a database search and ensure that we can get data which is in an acceptable format and has the feature data we need. If a database can't be found, we will dedicate a few days to create a simplified database to use in testing.
* **Scope** - This issue can be mitigated by having a good project plan outlined at the begining and designing our project to expand. We have designed the scope of our project to feature set of a fairly simple main use-cases. We then have multiple "stretch-goals" to implement as development progresses. This way if a feature doesn't work out, we can fall back and try a different feature. 

## Development Method

**Scrum** - Scrum development is a widely successful development methodology based on iterative and incremental processes. We chose this development method due to our project scope and how we plan to iteratively add to our project throughout the development cycle, and due to it's reduced risk compared to other methods.

## Project Tracking Method

**Notion** - (https://www.notion.so/) Notion is a project management software. We are using this due to its great ability to easily track our roadmap, documents, and project progress. It also has dedicated functionality for development sprints. It is also the prefered project tracking method of many companies in the industry including Pixar and Spotify.

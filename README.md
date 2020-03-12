# User Artifact Repository
A singular environment to store user persona's, upper level product descriptions and documentation

Still figuring out what to call this..... open to suggestions. something aeronotical themed would be nice like: Takeoff coordinator, or Bording Agent

# Description

There are three "artifacts" that this product aims to capture:

### Personas
personas are an alias for a set of users, they come to represent a market segment by using common lanuguge and empthy driving dialogue to help product teams coalese around a common user understanding. 

Persona's are typically unique to each product, and each product team, they often do not contain the same fields as personas generated b others. the way we see persona's used for this application is a little more broad, that is why the fields contained are standard boilerplate but optional. you have the ability to mearly store your visually rich powerpoint or PDF in the repository instead. persona's here aim to cast a wide net over your target market and help others quickly see who's needs you product is aimed at serving. 

Persona Fields:
- Name
- Title
- Internal or External
- Market Size
- Quote
- Needs
- Wants
- Pain Points
- Opportunities

### Insights
insights are what is often refered to as the subatomic granual of user information. Insights drive persona's often multiple, and persona's can be a collection of insights. Insights aim to capture the user experience journey at a specific time and place, yet their applicability can be very broad and powerful when curated. Insights should help product managers drive consices and impactful user stories and features for their products. 

Insight Fields:
- Title
- Description
- Content ( Text , Picture, Video )
- Experience Vector
- Maginitude
- Frequency
- Emotions
- Props
- Journey Location

### Products
Products are digital assets designed to fulfill users unmet needs and create value through strategic positioning within a marketplace. We all work within the same orginization so ensuring that product vision is aligned between teams and we can efficently create and capture value is essential to working as a high performing orginization. 

Product Fields:
- Name
- Description
- Metrics 
- Features
- Goals
- Unfair Advantage(TODO)
- Unique Value Proposition (TODO)
- Lifecycle Phase (TODO) 

### Playlist
TODO: this



## Getting Started

0. Requirements - > 
- Python v3.6 and up
- NodeJS v12 and up

1. Fork/Clone

2. Open .ENV file and update connection string

3. Run the server-side Flask app in one terminal window:

```
$ cd server       
$ python3.7 -m venv env         
$ source env/bin/activate         
(env)$ pip install -r requirements.txt         
(env)$ python application.py          
Navigate to http://localhost:5000         
```

4. Run the client-side Vue app in a different terminal window:

```
$ cd client         
$ npm install         
$ npm run serve         
Navigate to http://localhost:8080         
```

## Contributing
TODO
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning
0.8.0 - Beta Testing

## Authors
John Azzinaro

## Acknowledgments
Thank you to Josh Musick for bringing in the Insights concept from external benchmarking     
Drew Reins for providing detailed insight into the role of persona's and key attributes that need to be considered for any type of product
Beta testers! Thank you for the energy and excitement we hope that this can meet your expectations. 

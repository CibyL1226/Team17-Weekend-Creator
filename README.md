## Weekend Creator: Event and Food Place Ranking Application

Welcome to our Github Repository for the application built to create a fun and eventful weekend. 
The files are seperated in 4 different catergories: data, functions, google_places, and models. requirements.txt as a part of the main branch. 

Here are the links to where we host our applications (feel free to test it out with your own simple prompt like: "Find me cafes open late in New York"):

[**Food Ranking App**](https://restaurant-ranking-app-o6gfgyxixq3jhnzshtdwxf.streamlit.app/)

[**Event Ranking App**](https://event-ranking-app-5tu4ifwhchfjfcbxodxnlo.streamlit.app/)

### Steps to running the code for Food Ranking Apps:
1) Go to **weak_label_gen.ipynb** and run eitehr resturant_table.csv (for yelp restaurant) or food_df.csv(for more restaurant training data) and **restaurant_queries.txt** for queries
2) Then pass the resulting weak-labeled dataset with selected features through **ranking_model.ipynb** to train the model where trained model will automatically save locally at the end of the file 
3) To host the model in cloud vis Streamlit. Create an empty Github repository, then upload app.py, requirements.txt, trained model, and dataset you chose to use from Step 1
4) Make a free account on Streamlit and set the endpoint as app.py then click **Deploy**, a link hosting the application would generate
5) Try it out with your query!
6) Repeat the same steps for Event Ranking App just make sure to use the files starting in **tm**

### Data Access Statement
Restaurant_table data was scrapped from [Yelp API Developer Page](https://docs.developer.yelp.com/). We scrapped the data using AWS lambda function found in **yelp_api_aws_lambda.py** file, then process the data using AWS Databrew, Glue Crawler, and Athena to save the data as csv file onto the computer for futher processing. You can find Yelp API Terms of Use [here](https://terms.yelp.com/developers/api_terms/20250113_en_us/).

Ticketmaster data data was scrapped from [Ticketmaster Discovery API](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/) using AWS lambda function and process with Databrew, Glue Crawler, PySpark and Athena. You can find Ticketmaster API Terms of Use [here](https://developer.ticketmaster.com/support/terms-of-use/partner/). 

Google_places data was scrappewd using python codes from **google_places.py** found in google_places folder. THen process with **json_to_csv.py** file. Then combined with restaurant_table data using **Combined_Capstone_Dataset.ipynb**. Google Places API Terms of Use can be found [here](https://developers.google.com/maps/documentation/places/web-service/policies)





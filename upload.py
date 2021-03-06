from os import listdir
from pymongo import MongoClient
from bs4 import BeautifulSoup
import json
import csv

#path where json files are located
path = 'C:/Users/anhai/Desktop/SMU/MSDS7330_Database/MSDS7330_FinalTermProject/Data/'
#Mongo is the chosen database, make sure your MongoDB is running before execution of this program
client = MongoClient()
#database name is "HotelReviews"
db = client.HotelReviews
#empty list to store all json files in directory
files = []
#empty library to store hotel and reviews data to be uploaded
filedata = {}
#logs of uploaded collections
reviewslog = [["HotelID", "ReviewID", "Upload Status"]]
hotelslog = [["HotelID", "Upload Status"]]

#save the names of all the json files in the directory saved to the path variable above
for f in listdir(path):
    if f.endswith('.json'):
        files.append(f)

#iterate trhough each json file   
for f in files:        
    with open(path + f, 'rb') as hotel:
        #extract json into filedata dictionary
        filedata = json.load(hotel)
        #"Hotel" collection to hold all hotel's data
        
        collection = db.Hotel
        try:
            #extract plain text from "Address"'s xml format
            if "Address" in filedata["HotelInfo"]:
                x = BeautifulSoup(filedata["HotelInfo"]["Address"], features='lxml').get_text().strip()
                filedata["HotelInfo"].update({"Address": x})
            #add data to collection
            collection.insert_one(filedata["HotelInfo"])
            #mark upload as "Success"
            hotelslog.append([filedata["HotelInfo"]["HotelID"], "Success"])
        except Exception as e:
            #mark unsuccessfull upload with error message generated by the system
            hotelslog.append([filedata["HotelInfo"]["HotelID"], e])
            
        #"Reviews" collection to hold all users' reviews data
        collection = db.Reviews
        #interate through each review
        for doc in filedata["Reviews"]:
            #add "HotelID" to each review for reference
            doc.update({'HotelID': filedata["HotelInfo"]["HotelID"]})
            #parse out key and value pairs inside each review
            for key, value in doc.items():
                #check for nested documents
                if isinstance(value, dict):
                    for key in sorted(value):
                        #replace "." inside keys with blank to avoid error
                        value[key.replace(".", "")] = value.pop(key)
                else:
                    #remove unicode characters within texts
                    value = value.encode('ascii','ignore').decode('unicode_escape')
                    doc.update({key: value})
            try:
                #add data to collection
                collection.insert_one(doc)
                #mark upload as "Success"
                reviewslog.append([doc["HotelID"], doc["ReviewID"], "Success"])
            except Exception as e: 
                #mark unsuccessfull upload with error message generated by the system
                reviewslog.append([doc["HotelID"], doc["ReviewID"], e])


#write logs to csv files           
out = open('ReviewsUploadLog.csv', 'w', newline='')
for item in reviewslog:
    csv.writer(out).writerow(item)
out.close()
    
out = open('HotelsUploadLog.csv', 'w', newline='')
for item in hotelslog:
    csv.writer(out).writerow(item)
out.close()

        

    
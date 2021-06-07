import csv
import pandas as pd
import numpy as np



def write_to_csv(Experience,Certifications,PG,Graduation,Linkedin,Github,Metro,LinkCount,CPP,SQL,GIT,WEB, CLASS):

    with open('dataset/records.csv', 'r') as f:
        reader = csv.reader(f)
        for header in reader:
            break
    with open('dataset/records.csv', "a", newline='\n') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        dict = {"Experience": Experience,"Certifications": Certifications,"PG": PG,"Graduation": Graduation,
        "Linkedin": Linkedin,"Github": Github,"Metro": Metro,"LinkCount": LinkCount,"CPP": CPP,"SQL": SQL,"GIT": GIT,"WEB": WEB, "class": CLASS}
        writer.writerow(dict)
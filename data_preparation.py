# Load pandas
import pandas as pd
import json
import ast
import writeCSV

Experience = 0
Certifications = 0
PG = 0
Graduation = 0
LinkedIn = 0
Github = 0
Link_Count = 0
Metro = 0
CPP = 0
SQL = 0
WEB = 0

metro_cities = ["delhi", "mumbai", "kolkata", "chennai", "bangalore", "hyderabad", "ahmedabad", "pune","visakhapatnam", "kanpur", "surat", "patna", "jaipur", "coimbatore", "nagpur", "madurai", "salem", "jodhpur"]
graduation_keywords = ["'BE", "BE", "Bachelor", "B.E", "BTech", "B.E.", "Bachelor's","Btech", "'Bachelor", "'B.E", "'BTech", "'B.E.", "'Bachelor's", "'Btech"]
pg_keywords = ["Masters", "Master's", "MTECH", "Mtech", "M.Tech", "M.tech","'Masters", "'Master's", "'MTECH", "'Mtech", "'M.Tech", "'M.tech"]
linkedin_link = ["linkedin"]
github_link = ["github"]
cpp_set = ["CPP", "cpp", "c++", "C++"]
sql_set = ["sql", "mysql", "SQL", "MYSQL", "Sql", "Mysql", "MySql"]
git_set = ["GIT", "git", "Git"]
web_set = ["HTML", "html", "css", "CSS", "javascript", "Javascript","JavaScript", "JS", "CSS3", "css3", "HTML5", "html5"]


def prepareDataset():
    try:
        df = pd.read_csv('dataset/resume_data.csv', header=0)
        # print(df.columns)
        # print(df)
        for index, row in df.iterrows():
            if df.empty:
                print("Row #" + str(index) + " is Blank")
            sum = 0
            CLASS = ""
            Metro = row["City"].lower() in metro_cities if row["City"] else 0
            Graduation = bool(set(row["Educations"].split()) & set(graduation_keywords)) if row["Educations"] else 0
            PG = bool(set(row["Educations"].split()) & set(pg_keywords)) if row["Educations"] or row["Educations"] != "" else 0
            LinkedIn = bool(set(row["Links"].split(".")).intersection(set(linkedin_link))) if row["Links"] or row["Links"] != "" else 0
            Github = bool(set(row["Links"].split(".")).intersection(set(github_link))) if row["Links"] else 0
            Link_Count = len(ast.literal_eval(row["Links"])) if row["Links"] else 0
            Certifications = len(ast.literal_eval(row["Certificates"])) if row["Certificates"] else 0
            Experience = len(ast.literal_eval(row["work_experiences"])) if row["work_experiences"] else 0
            CPP = bool(set(ast.literal_eval(row["Skills"])).intersection(set(cpp_set))) or any(item in row["Skills"] for item in cpp_set) if row["Skills"] else 0
            SQL = bool(set(ast.literal_eval(row["Skills"])).intersection(set(sql_set))) or any(item in row["Skills"] for item in sql_set) if row["Skills"] else 0
            GIT = bool(set(ast.literal_eval(row["Skills"])).intersection(set(git_set))) or any(item in row["Skills"] for item in git_set) if row["Skills"] else 0
            WEB = bool(set(ast.literal_eval(row["Skills"])).intersection(set(web_set))) or any(item in row["Skills"] for item in web_set) if row["Skills"] else 0
            # Adding class based on classified data
            sum = Experience+Certifications+int(PG)+int(Graduation)+int(LinkedIn)+int(Github)+int(Metro)+Link_Count+int(CPP)+int(SQL)+int(GIT)+int(WEB)
            # print("Sum is:" + str(sum))
            # print("PG:"+ str(PG) + ", Graduation: " + str(Graduation) + ", CPP: " + str(CPP) + ", LinkedIn: " + str(LinkedIn) + ", Github: " + str(Github) + ", SQL: " + str(SQL) + ", GIT: " + str(GIT) + ", WEB: " + str(WEB) + ", Metro: " + str(Metro))
            if sum >= 10:
                CLASS = "A" if (CPP or SQL or GIT or WEB) else "B"
            elif (sum > 6 and sum <= 9):
                CLASS = "B" if(not PG) else "A"
            elif (sum >= 3 and sum <= 6):
                CLASS = "C"
            elif (sum < 3):
                CLASS = "D"
            # print("Class Given : " + str(CLASS))
            # print("#"+ str(index) + " : " + str(int(WEB)))
            writeCSV.write_to_csv(Experience,Certifications,int(PG),int(Graduation),int(LinkedIn),int(Github),int(Metro),Link_Count,int(CPP),int(SQL),int(GIT),int(WEB), CLASS)
            print("Datarow #"+ str(index) +" appended in CSV")
        print("training set created successfully!")
        return True;
    except:
        return False;


def getSingleResult(resumeText, resumeData):
    # print(resumeData)
    link_set = [".com", "com/", "com"]

    Experience = resumeData['total_exp'] if resumeData['total_exp'] else 0
    Certifications = len(resumeData['certifications']) if len(resumeData['certifications']) > 0 else 0
    LinkedIn = 1 if (resumeData['linkedin'] and len(resumeData['linkedin']) > 0) else bool(set(resumeText.lower().split(".")).intersection(set(linkedin_link))) if resumeText or resumeText != "" else 0
    PG = bool(set(resumeData['degree']).intersection(set(pg_keywords))) if len(resumeData['degree']) > 0 else bool(set(resumeText.lower().split()) & set(pg_keywords)) if resumeText or resumeText != "" else 0
    Graduation = bool(set(resumeData['degree']).intersection(set(graduation_keywords))) if len(resumeData['degree']) > 0 else bool(set(resumeText.lower().split()) & set(graduation_keywords)) if resumeText else 0
    CPP = bool(set(resumeData['skills']).intersection(set(cpp_set))) if len(resumeData['skills']) > 0 else bool(set(resumeText.lower().split()).intersection(set(cpp_set))) or any(item in resumeText for item in cpp_set) if resumeText else 0
    SQL = bool(set(resumeData['skills']).intersection(set(sql_set))) if len(resumeData['skills']) > 0 else bool(set(resumeText.lower().split()).intersection(set(sql_set))) or any(item in resumeText for item in sql_set) if resumeText else 0
    GIT = bool(set(resumeData['skills']).intersection(set(git_set))) if len(resumeData['skills']) > 0 else bool(set(resumeText.lower().split()).intersection(set(git_set))) or any(item in resumeText for item in git_set) if resumeText else 0
    WEB = bool(set(resumeData['skills']).intersection(set(web_set))) if len(resumeData['skills']) > 0 else bool(set(resumeText.lower().split()).intersection(set(web_set))) or any(item in resumeText for item in web_set) if resumeText else 0
    Link_Count = len([item in resumeText.lower().split() for item in link_set]) if resumeText else 0
    Metro = any(item in resumeText.lower().split() for item in metro_cities) if resumeText else 0
    Metro = bool(set(resumeText.lower().split()).intersection(set(metro_cities))) if resumeText else 0
    Github = bool(set(resumeText.lower().split(".")).intersection(set(github_link))) if resumeText else 0

    result = [str(Experience),str(Certifications),str(int(PG)),str(int(Graduation)),str(int(LinkedIn)),str(int(Github)),str(int(Metro)),str(Link_Count),str(int(CPP)),str(int(SQL)),str(int(GIT)),str(int(WEB))]

    return result


if __name__ == "__main__":
    prepareDataset()

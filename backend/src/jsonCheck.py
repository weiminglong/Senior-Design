import json

def categoriesJsonCheck(category):
    #read the local json file
    json_file = open("categories.json")
    #with open('categories.json') as json_file:
    #load the json array
    jsonArray = json.load(json_file)
    if category in jsonArray:
        print("Yes, found in List : ", jsonArray)
    else:
        jsonArray.append(category)
        print("Appended new category : ", category)

    #write new changes to json file
    with open('categories.json', 'w', encoding='utf-8') as f:
        json.dump(jsonArray, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # categories = ["Math", "Computer Science", "Physics", "Statistics", "History"]
    # with open('categories.json', 'w', encoding='utf-8') as f:
    #     json.dump(categories, f, ensure_ascii=False, indent=4)
    # json_file = open("categories.json")
    # data = json.load(json_file)
    # if 'Computer Science' in data :
    #     print("Yes, found in List : " , data)
    categoriesJsonCheck("Political Science")

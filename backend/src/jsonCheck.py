import json

def categoriesJsonCheck(newCategory):
    #read the local json file
    json_file = open("categories.json")
    #with open('categories.json') as json_file:
    #load the json array
    data = json.load(json_file)
    if newCategory in data['categories']:
        print("\nYes, found in List : ", data)
    else:
        data['categories'].append(newCategory)
        print("\nAppended new category : ", newCategory)

    #write new changes to json file
    with open('categories.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return data

if __name__ == "__main__":
    """JSON ARRAY"""
    # categories = ["Math", "Computer Science", "Physics", "Statistics", "History"]
    # with open('categories.json', 'w', encoding='utf-8') as f:
    #     json.dump(categories, f, ensure_ascii=False, indent=4)
    # json_file = open("categories.json")
    # data = json.load(json_file)
    # if 'Computer Science' in data :
    #     print("Yes, found in List : " , data)
    categoriesJsonCheck("Political Science")
    '''NEW DICT'''
    # categories = {"categories": ["Math", "Computer Science", "Physics", "Statistics", "History"]}
    # with open('categories.json', 'w', encoding='utf-8') as f:
    #     json.dump(categories, f, ensure_ascii=False, indent=4)
    # json_file = open("categories.json")
    # data = json.load(json_file)
    # if 'History' in data['categories']:
    #     print("Yes, found in List : ", data)
    # data['categories'].append("newCatTest")
    # print(data)

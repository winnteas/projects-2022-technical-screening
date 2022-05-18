"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: We do not expect you to come up with a perfect solution. We are more interested
in how you would approach a problem like this.
"""
import json
import re


# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()
    
# Return the condition with stopwords removed
def simplify_condition(condition):
    # Remove stopwords
    for word in ("Prerequisite:", "Pre-req:", "Prequisite:", "Pre-requisite:", "Completion of"):
        condition = condition.replace(word, "")
    
    # Add COMP to the start of the condition if not there
    if re.match("^\d{4}$", condition):
        condition = "COMP" + condition
    return condition

def find_course(courses_list, course):
    if course in courses_list:
        return True
    return False

def solve_req(condition, courses_list):
    req_met = []
    print(condition)
    if len(condition.split()) == 1:
        # for UOC conditions
        if condition == "True":
            return True
        elif condition == "False":
            return False
        return find_course(courses_list, condition)
    operator = "" 
    for word in condition.split():
        if re.match("[A-Z]{4}[0-9]{4}", word):
            req_met.append(find_course(courses_list, word))

        elif word.lower() == "and" or word.lower() == "or":
            operator = word.lower()
        elif word == "True" or word == "False":
            if word == "True":
                req_met.append(True)
            else:
                req_met.append(False)

    if len(condition.split()) > 1:
        operator = condition.split()[1]
    else:
        operator = ""
    print(f"operatorrrr {operator}")
    print(f"req_met is {req_met}")
    if operator.lower() == "and":
        return all(req_met)
    elif operator.lower() == "or":
        return any(req_met)

def check_req(condition, courses_list):

    # Check uoc patterns
    total_uoc = 0
    uoc_pattern2 = re.findall("level \d [A-Z]{4} courses", condition)
    uoc_pattern0 = re.findall("\d+ units of credit in", condition)
    uoc_pattern3 = re.findall("\d+ units oc credit in", condition)
    uoc_pattern1 = re.findall("\d+ units of credit", condition)

    if uoc_pattern2:
        # lists should be the same length
        for i in range(len(uoc_pattern2)):
            total_uoc = int(uoc_pattern1[i].split()[0])
            print(f"initial uoc {total_uoc}")
            # find courses with the same level and faculty
            level_faculty = uoc_pattern2[i].split()[2] + uoc_pattern2[i].split()[1] 
            for c in courses_list:
                if c.startswith(level_faculty):
                    total_uoc -= 6

            # Replace both patterns as there can be irregular spacing
            if total_uoc <= 0:
                condition = condition.replace(uoc_pattern0[i],  "True")
                condition = condition.replace(uoc_pattern2[i], "")
            else:
                condition = condition.replace(uoc_pattern0[i], "False")
                condition = condition.replace(uoc_pattern2[i], "")
            print(f"total uoc is {total_uoc}, after uoc condition {condition}")
    elif uoc_pattern3:
        total_uoc = int(uoc_pattern3[0].split()[0])
        # find bracketed courses
        uoc_courses = condition.split(uoc_pattern3[0], 2)[1]
        uoc_courses = re.findall("[A-Z]{4}[0-9]{4}", uoc_courses)
        if uoc_courses:
            for c in uoc_courses:
                if find_course(courses_list, c):
                    total_uoc -= 6
        
        else:
            # COMP courses
            uoc_courses = re.findall("COMP[0-9]{4}", str(courses_list))
            print(f" my courses {uoc_courses}")
            total_uoc -= len(uoc_courses) * 6
            print(f" my total uoc {total_uoc}")

        if total_uoc <= 0:
            condition = condition.split(uoc_pattern3[0], 1)[0] + "True"
        else:
            condition = condition.split(uoc_pattern3[0], 1)[0] + "False"

            


    elif uoc_pattern0:
        total_uoc = int(uoc_pattern0[0].split()[0])
        # find bracketed courses
        uoc_courses = condition.split(uoc_pattern0[0], 2)[1]
        uoc_courses = re.findall("[A-Z]{4}[0-9]{4}", uoc_courses)
        if uoc_courses:
            for c in uoc_courses:
                if find_course(courses_list, c):
                    total_uoc -= 6
        
        else:
            # COMP courses
            uoc_courses = re.findall("COMP[0-9]{4}", str(courses_list))
            print(f" my courses {uoc_courses}")
            total_uoc -= len(uoc_courses) * 6
            print(f" my total uoc {total_uoc}")

        if total_uoc <= 0:
            condition = condition.split(uoc_pattern0[0], 1)[0] + "True"
        else:
            condition = condition.split(uoc_pattern0[0], 1)[0] + "False"

    elif uoc_pattern1:
        total_uoc = int(uoc_pattern1[0].split()[0])
        if len(courses_list) * 6 >= total_uoc:
            condition = condition.replace(uoc_pattern1[0], "True")
        else:
            condition = condition.replace(uoc_pattern1[0], "False")



    while condition.count("(") != 0:
        counter = 0
        for i, l in enumerate(condition):
            if l == "(":
                counter += 1
            if counter == condition.count("("):
                open_bracket_index = i
                closed_bracket_index = condition[i:].find(")") + open_bracket_index
                operand = condition[open_bracket_index + 1:closed_bracket_index]
                print(f"current operand {operand}")
                # check the operand 
                operand = str(solve_req(operand, courses_list))
                condition = condition.replace(condition[open_bracket_index:closed_bracket_index + 1], operand)
                print(f"final {condition}")
                # print(f"for brackets {brack} this is {req_met}")
    
    # if len(condition.split()) > 1:
    #     operator = condition.split()[1]
    # else:
    #     operator = ""
    # print(f"operator {operator}")
    return solve_req(condition, courses_list)


def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """
    


    condition = simplify_condition(CONDITIONS[target_course])
    print(f"this is my condition {condition}")
    if condition == "":
        return True
    
    return check_req(condition, courses_list)
 

if __name__ == '__main__':
    assert is_unlocked(["COMP1927"], "COMP3151") == True
    assert is_unlocked(["MATH1081"], "COMP3153") == True
    assert is_unlocked(["MATH1081"], "COMP3151") == False
    assert is_unlocked(["COMP1911", "COMP2000"], "COMP2121") == False
    assert is_unlocked(["MATH1081", "COMP2000"], "COMP9417") == False
    assert is_unlocked(["COMP4952"], "COMP4953") == True
    assert is_unlocked(["MATH5836"], "COMP9418") == True

    assert is_unlocked(["COMP6441", "COMP6443", "COMP1511"], "COMP9302") == False
    assert is_unlocked(["COMP6441", "COMP6443", "COMP6447"], "COMP9302") == True
    assert is_unlocked(["COMP6441", "COMP6443", "COMP6447", "COMP1511", "COMP2521", "COMP1531"], "COMP4951") == True
    assert is_unlocked(["COMP3901", "COMP3333", "COMP3331", "COMP3311", "COMP3131", "COMP3121"], "COMP3902") == True
    assert is_unlocked(["COMP3901", "COMP1151"], "COMP3902") == False

    assert is_unlocked(["COMP1921"], "COMP1531") == True

    # "COMP1531": "COMP1511 or DPST1091 or COMP1917 or COMP1921",
    # "COMP3151": "COMP1927    OR ((COMP1521 or DPST1092) AND COMP2521)",
    # "COMP2121": "COMP1917 OR COMP1921 OR COMP1511 OR DPST1091 OR COMP1521 OR DPST1092 OR (COMP1911 AND MTRN2500)",
    # "COMP9417": "MATH1081 and ((COMP1531 or COMP2041) or (COMP1927 or COMP2521))",
    # "COMP4953": "4952",
    # "COMP9418": "Prerequisite:  MATH5836 or COMP9417",
    # "COMP9302": "(COMP6441 OR COMP6841) AND 12 units of credit in (COMP6443, COMP6843, COMP6445, COMP6845, COMP6447)",
    # "COMP4951": "36 units of credit in COMP courses",

    # "COMP3900": "COMP1531 and (COMP2521 or COMP1927) and 102 units of credit",
    # "COMP3901": "Prerequisite: 12 units of credit in  level 1 COMP courses and 18 units of credit in level 2 COMP courses",
    # Does that include COMP3901?

    # "COMP3902": "Prerequisite: COMP3901 and 12 units of credit in level 3 COMP courses",

    assert is_unlocked(["COMP9417", "COMP9418", "COMP9447"], "COMP9491") == True
    assert is_unlocked(["COMP6441"], "COMP9302") == False
    assert is_unlocked(["COMP6441", "COMP64443", "COMP6843", "COMP6445"], "COMP9302") == True
    assert is_unlocked(["COMP1234", "COMP5634", "COMP4834"], "COMP9491") == False
    assert is_unlocked(["COMP3901"], "COMP3902") == False
    assert is_unlocked(["COMP3901", "COMP6441", "COMP6443"], "COMP3902") == False
    assert is_unlocked(["COMP3901", "COMP3441", "COMP3443"], "COMP3902") == True
    assert is_unlocked(["COMP1911", "MTRN2500"], "COMP2121") == True
    assert is_unlocked(["COMP1521"], "COMP2121") == True

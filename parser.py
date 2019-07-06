# -*- coding: utf-8 -*-
import modules
import collector
import xml.etree.ElementTree as ET
import mysql.connector








def parse_xml(file):
    base_url='http://cs.uoi.gr/en/'
    root = ET.parse(file).getroot()
    elemList = []
    for elem in root.iter():
      elemList.append(elem.tag)
    elemList=list(set(elemList))
    elemList.remove("announcements")
    elemList.remove("announcement")
    announcements=[]
    for announcement in root.findall('announcement'):
        details={}
        for id in elemList:
            if id=='url':
                details[id]=base_url+announcement.find(id).text
            else:
                details[id]=announcement.find(id).text
        announcements.append(details)
    return announcements

def get_values_for_mysql(array_dictionary):
    fields=set()

    for i in array_dictionary:
        for j in i:
            fields.add(j)
    fields=list(fields)
    values=[]
    for dict in array_dictionary:
        val=()
        for field in fields:
            val = val+(dict[field],)
        values.append(val)
    return [fields,values]



def write_to_database(db,data,table):
    values=""
    types=""
    for val in data[0]:
        values=values+val+","
        types=types+"%s,"
    values=values[0:-1]
    types=types[0:-1]
    sql = "INSERT IGNORE INTO "+table+" ("+values+") VALUES ("+types+")"
    val=data[1]

    mycursor = db.cursor()
    mycursor.executemany(sql, val)

    db.commit()

    print(mycursor.rowcount, "was inserted.")



if __name__ == '__main__':
    file="announcements.xml"
    collector.find_new_posts("http://cs.uoi.gr/en/index.php?menu=m5&page=",file)
    test=parse_xml(file)
    values=get_values_for_mysql(test)




    ##################################################################
    # Enter your credentials here
    # The table in which you enter the info should have the collumn named id as primary key
    ##################################################################
    mydb = mysql.connector.connect(
      host="localhost",
      user="porfanid",

      passwd="password",
      database="cse"
    )
    table="announcements"


    write_to_database(mydb,values,table)
    #print values

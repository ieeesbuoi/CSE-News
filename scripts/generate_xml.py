# data[0] = url
# data[1] = date
# data[2] = title
# data[3] = id
# data array consists of the above fields

def generate_xml(data):
    print ("Writing xml file...")

    f = open("announcements.xml", "w")

    f.write("<announcements>")

    for data in data:
        if data:
            f.write("<announcement>")

            f.write("<url>")
            f.write(data[0].replace("&","&amp;"))
            f.write("</url>")

            f.write("<date>")
            f.write(data[1])
            f.write("</date>")

            f.write("<title>")
            f.write(data[2].replace("&","&amp;"))
            f.write("</title>")

            f.write("<id>")
            f.write(str(data[3]))
            f.write("</id>")

            f.write("</announcement>")
    f.write("</announcements>")
    f.close()

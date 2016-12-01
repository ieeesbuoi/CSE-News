# data[0] = url
# data[1] = date
# data[2] = title
# data[3] = id
# data array consists of the above fields

def generate_html(data):
    print ("Writing html file...")

    f = open("announcements.html", "w")

    f.write("<h4>Announcements UOI</h4>")

    f.write("<table>")
    for data in data:
        if (data):
            f.write("<tr>")

            f.write("<td>")
            f.write(data[0].replace("&","&amp;"))
            f.write("</td>")

            f.write("<td>")
            f.write(data[1])
            f.write("</td>")

            f.write("<td>")
            f.write(data[2].replace("&","&amp;"))
            f.write("</td>")

            f.write("<td>")
            f.write(str(data[3]))
            f.write("</td>")

            f.write("</tr>")
    f.write("</table>")
    f.close()


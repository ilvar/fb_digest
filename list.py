import json
import os

files = list(os.listdir("./messages/"))
files.sort()

digest = open("digest.html", "w")

digest.write("<html>\n<body>\n")

for f in files:
    data = json.load(open("./messages/%s" % f))
    msg = data.get("message", "")
    if len(msg) < 200:
        continue
        
    link = "https://www.facebook.com/%s" % data['id']

    block = "<div class='post'>%s</br><a href='%s'>Link</a></div>\n" % (msg.replace("\n", "<br/>\n"), link)
    digest.write(block.encode("utf8"))
    
    print("%s %s" % (msg.replace("\n", " ")[:100], link))
    
digest.write("\n</body>\n</html>")
# Not evertything works yet
from generator import htmlPage, Text, Link, Image, Frame

# Create an htmlPage
Webpage1 = htmlPage(export_to_document=True)
# Add a title to the htmlPage
Webpage1.title = "Title"
# Add a stylesheet to the htmlPage
Webpage1.setStyle("style.css")
# OR add some css manually
Webpage1.addStyle("blue-text", "color: blue", htmltype='id')

# Add a text element
text1 = Text("This is some text.", header=2)
text1.setPosition(0)
text1.add_to(Webpage1)

# Add a text element with an id
text2 = Text("This is some other text.", htmlid="blue-text")
text2.setPosition(1)
text2.add_to(Webpage1)

# Add a link element
link = Link("This is a link which you shouldn't click.", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
link.setPosition(2)
link.add_to(Webpage1)

# Add an image
imgage = Image("https://github.com/AsinusGrandus/Project-Stingray/blob/master/favicon.png", (64,64))
imgage.setPosition(5)
imgage.add_to(Webpage1)

# Add a frame
frame = Frame("https://www.youtube.com/embed/dQw4w9WgXcQ", (942,530))
frame.setPosition(4)
frame.add_to(Webpage1)

# print the html file path or the raw html
print(Webpage1.get_html())
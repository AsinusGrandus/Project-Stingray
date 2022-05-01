class RangeError(Exception):
    pass

class Page():
    def __init__(self, export_to_document : bool = False) -> None:
        self.export_to_document = export_to_document

        self.HeadElements = {}
        self.BodyElements = {}

        self.customStyle = False
        self.StyleElements = {}
        self.stylesheet = "default"

        self.title = "Title"
        self.style = ""
        self.head = ""
        self.body = ""

        self.raw_html: str

    def setStyle(self, stylesheet : str) -> None:
        self.customStyle = True
        self.stylesheet = stylesheet
        self.HeadElements[0] = f'<link rel="stylesheet" href="{self.stylesheet}">'

    def addStyle(self, name : str, css : str, htmltype = None) -> None:
        key = name if htmltype == "class" else f'#{name}'
        self.StyleElements[key] = css

    def get_html(self) -> str:
        sortedHead = sorted(list(self.HeadElements.keys()))
        if len(sortedHead) == 0: self.head = ""
        for key in sortedHead:
            self.head += "\n\t" + self.HeadElements[key]
        
        sortedBody = sorted(list(self.BodyElements.keys()))
        if len(sortedBody) == 0: self.body = ""
        for key in sortedBody:
            self.body += "\n\t" + self.BodyElements[key]

        if not self.customStyle:
            sortedStyle = sorted(list(self.StyleElements.keys()))
            if len(sortedStyle) == 0: self.style = ""
            for key in sortedStyle:
                self.style += '\n\t\t' + key + ' {' + self.StyleElements[key] + ';}' + '\n'
            self.head += f'<style>{self.style}\t</style>'

        self.raw_html = f"""<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{self.title}</title>
    {self.head}
</head>
<body>{self.body}
</body>
""" 
        if self.export_to_document:
            path = fr"html-pages\{self.title}.html"
            with open(path, "w") as f:
                f.write(self.raw_html)
            return path

        return self.raw_html

class Element():
    def __init__(self) -> None:
        self.row : int
        self.html : str

    def setPosition(self, row : int) -> None:
        if row < 0: raise RangeError("The row number must be 0 or higher")
        self.row = row

    # def setInfo(self, Htmlid : str = "", Htmlclass : str = "") -> None:
    #     self.Htmlid = Htmlid
    #     self.Htmlclass = Htmlclass 
    
    def closeTag(self, tag : str) -> str:
        return "</" + tag[1:]
    
    def add_to(self, page : Page):
        page.BodyElements[self.row] = self.html

class Text(Element):
    def __init__(self, text : str, header : int = -1, htmlid: str = "", htmlclass : str = "") -> None:
        super().__init__()

        self.htmlid = htmlid
        self.htmlclass = htmlclass

        if header > 6: raise RangeError("Text size must be a number between 0 and 6")
        
        self.text = text.replace("\n", "<br>")

        self.tag = f'<p>' if header < 0 else f'<h{header}>'
        self.closeTag = super().closeTag(self.tag)
        cut = 2 if self.tag == "<p>" else 3
        self.tag = self.tag[:cut] + f' id="{self.htmlid}" class="{self.htmlclass}"' + self.tag[cut:]
        self.html = f"{self.tag}{self.text}{self.closeTag}"



class Image(Element):
    def __init__(self, source, size : tuple, altText : str = "Image") -> None:
        super().__init__()

        self.source = source
        self.altText = altText
        self.size = size
        self.width, self.heigt = self.size

        self.html = f'<img src="{self.source}" alt="{self.altText}" width="{self.width}" heigth="{self.heigt}" id="{self.Htmlid}" class="{self.Htmlclass}">'


class Link(Element):
    def __init__(self, text : Element, url : str) -> None:
        super().__init__()

        self.text = text
        self.url = url

        self.html = f'<a href="{self.url}">{self.text}</a>'

class Frame(Element):
    def __init__(self, source, size: tuple, title: str = "Frame") -> None:
        super().__init__()

        self.source = source
        self.title = title
        self.size = size
        self.width, self.heigt = self.size

        self.html = f'<iframe src="{self.source}" height="{self.heigt}" width="{self.width}" title="{self.title}" id="{self.Htmlid}" class="{self.Htmlclass}"></iframe>'


Webpage1 = Page(export_to_document=True)
# Webpage.setStyle("style.css")
Webpage1.title = "Title"

Webpage1.addStyle("blue-text", "color: blue")

text1 = Text("This is some text.", header=2)
text1.setPosition(0)
text1.add_to(Webpage1)

text2 = Text("This is some other text.", htmlid="blue-text")
text2.setPosition(1)

text2.add_to(Webpage1)

# link = Link("This is a link which you shouldn't click.", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
# link.setPosition(2)
# link.add_to(Webpage1)

# imgage = Image("favicon.png", (64,64))
# imgage.setPosition(5)
# imgage.add_to(Webpage1)

# frame = Frame("https://www.youtube.com/embed/dQw4w9WgXcQ", (942,530))
# frame.setPosition(4)
# frame.add_to(Webpage1)

print(Webpage1.get_html())

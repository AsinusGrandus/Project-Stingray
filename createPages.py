# element: id and class=""
# 

#  NOT FINAL IN ANY WAY!

class RangeError(Exception):
    pass

class Page():
    def __init__(self, export_to_document : bool = False) -> None:
        self.Elements = {}
    
    def createHtmlPage(self):
        print(self.Elements.keys())
        print(sorted(list(self.Elements.keys())))
        Htmlpage = ""
        sorted_keys = sorted(list(self.Elements.keys()))
        for key in sorted_keys:
            Htmlpage += self.Elements[key]
        print(Htmlpage)
        return Htmlpage


class Element():
    def __init__(self) -> None:
        self.row : int
        self.id : str
        self.html : str

    def setPosition(self, row : int) -> None:
        if row < 0: raise RangeError("The row number must be 0 or higher")
        self.row = row

    def setInfo(self, Htmlid : str = "", Htmlclass : str = "") -> None:
        self.Htmlid = Htmlid
        self.Htmlclass = Htmlclass 
    
    def closeTag(self, tag : str) -> str:
        return "</" + tag[1:]
    
    def add_to(self, page : Page):
        page.Elements[self.row] = self.html
    

class Text(Element):
    # <h1>This is heading 1</h1>
    # <h2>This is heading 2</h2>
    # <h3>This is heading 3</h3>
    # <h4>This is heading 4</h4>
    # <h5>This is heading 5</h5>
    # <h6>This is heading 6</h6>

    # <p>This is a paragraph</p>

    # Add bold, italic...
    def __init__(self, text : str, header : bool = False, size : int = -1) -> None:
        super().__init__()

        if header and size < 0 or size > 6: raise RangeError("Text size must be a number between 0 and 6")
        if header: self.tag = f"<h{size}>"

        self.text = text.replace("\n", "<br>")

        self.tag = "<p>"
        self.closeTag = super().closeTag(self.tag)

        self.html = self.tag + self.text + self.closeTag



class Image(Element):
    # <img src="imagePath" alt="altText" width="104" height="142">
    def __init__(self, imagePath, size : tuple, altText : str = "Image") -> None:
        super().__init__()

        self.imagePath = imagePath
        self.altText = altText
        self.size = size
        self.width, self.heigt = self.size

        self.html = f'<img src="{imagePath}" alt="{self.altText}" width="{self.width}" heigth="{self.heigt}">'


class Link(Element):
    # <a href="url">text</a>
    def __init__(self, element : Element, url : str) -> None:
        super().__init__()

        self.element = element
        self.url = url

        self.html = f'<a href="{self.url}">{self.element}</a>'

pagina = Page()

lbl1 = Text("Label 1", header=True, size=2)
lbl1.setPosition(0)
lbl1.add_to(pagina)

lbl2 = Text("Label 2")
lbl2.setPosition(1)
lbl2.add_to(pagina)

lnk = Link("This is a link", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
lnk.setPosition(2)
lnk.add_to(pagina)

img = Image("favicon.png", (64,64))
img.setPosition(3)
img.add_to(pagina)

print(pagina.Elements)
pagina.createHtmlPage()
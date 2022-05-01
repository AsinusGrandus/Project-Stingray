class RangeError(Exception):
    pass

class htmlPage():
    def __init__(self, export_to_document : bool = False) -> None:
        """
        Initiates a htmlPage class
        Arguments:
            self: self@htmlPage
            export_to_document: export the html code to a document
        Returns:
            None
        """
        # If the document needs to get exported as .html
        self.export_to_document = export_to_document

        # Dictionaries to add data too
        self.HeadElements = {}
        self.BodyElements = {}
        self.StyleElements = {}

        # If the user uses a custom css file (stylesheet) or not
        self.customStyle = False
        self.stylesheet = "default"

        # Variables used to generate the raw html
        self.title = "Title"
        self.style = ""
        self.head = ""
        self.body = ""

        # The html which gets returned or exported as file
        self.raw_html: str

    def setStyle(self, stylesheet : str) -> None:
        """
        Binds a stylesheet to an htmlPage.
        Arguments:
            self: self@htmlPage
            stylesheet: path to the .css file
        Returns:
            None
        """
        # When the function gets ran there will be a custom stylesheet
        self.customStyle = True
        self.stylesheet = stylesheet
        # Link the stylesheet in the html file
        self.HeadElements[0] = f'<link rel="stylesheet" href="{self.stylesheet}">'

    def addStyle(self, name : str, css : str, htmltype = None) -> None:
        """
        Adds a custom style to an htmlPage
        Arguments:
            self: self@htmlPage
            name: name from the id or class
            css: a string with css code
            htmltype: html 'id' or 'class'
        Returns:
            None
        """
        # Use the correct css syntax for an id or a class
        # If htmltype isn't a class, we treat it as an id
        key = name if htmltype == "class" else f'#{name}'
        # Add the accuired style information to the htmlPage StyleElements 
        self.StyleElements[key] = css

    def get_html(self) -> str:
        """
        Creates html code
        Arguments:
            self: self@htmlPage
        Returns:
            None
        """
        # Sort the elements in the head dictionary using their position
        sortedHead = sorted(list(self.HeadElements.keys()))
        # If there is nothing in the sorted list, self.head needs to be empty
        if len(sortedHead) == 0: self.head = ""
        # Add every element from HeadElements to the self.head string (\n and \t are purely for visuals)
        for key in sortedHead:
            self.head += "\n\t" + self.HeadElements[key]
        
        # Sort the elements in the body dictionary using their position
        sortedBody = sorted(list(self.BodyElements.keys()))
        # If there is nothing in the sorted list, self.body needs to be empty
        if len(sortedBody) == 0: self.body = ""
        # Add every element from BodyElements to the self.body string (\n and \t are purely for visuals)
        for key in sortedBody:
            self.body += "\n\t" + self.BodyElements[key]

        # If there is no custom style provided, we generate our own
        if not self.customStyle:
            # Sort the elements in the style dictionary using their position
            sortedStyle = sorted(list(self.StyleElements.keys()))
            # If there is nothing in the sorted list, self.style needs to be empty
            if len(sortedStyle) == 0: self.style = ""
            # Add every element from StyleElements to the self.style string with correct css syntax (\n and \t are purely for visuals)
            for key in sortedStyle:
                self.style += '\n\t\t' + key + ' {' + self.StyleElements[key] + ';}' + '\n'
            # Add the style string to it's correct place in head
            self.head += f'<style>{self.style}\t</style>'
        # Create the html, looks weird but otherwise you have unwanted tabs or enters
        self.raw_html = f"""<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{self.title}</title>
    {self.head}
</head>
<body>{self.body}
</body>
""" 
        # If it needs to be exported to a document, it gets exported
        if self.export_to_document:
            # Create a path to export to using the htmlPage title
            path = fr"html-pages\{self.title}.html"
            # Export the html
            with open(path, "w") as f:
                f.write(self.raw_html)
            # Return the path to the exported file
            return path

        # If it didn't get exported, return the raw html
        return self.raw_html

class Element():
    def __init__(self) -> None:
        """
        Initiates an Element class, used to create basic html elements
        Arguments:
            self: self@Element
        Returns:
            None
        """
        # The row determens the position in the html file
        self.row : int
        # Html from the Element
        self.html : str

    def setPosition(self, row : int) -> None:
        """
        Sets the row for an Element
        Arguments:
            self: self@Element
            row: position in the html file
        Returns:
            None
        """
        if row < 0: 
            # LOGG
            raise RangeError("The row number must be 0 or higher")
        # Give the row value to the variable
        self.row = row

    def closeTag(self, tag : str) -> str:
        """
        Generates a closing tag for the elements if it isn't hardcoded
        Arguments:
            self: self@Element
            tag: the html tag
        Returns:
            Closing tag
        """
        # </ is the sart from every closing tag, it gets pasted before the begin tag with < cut off
        return "</" + tag[1:]
    
    def add_to(self, page : htmlPage) -> None:
        """
        Adds an element to an htmlPage
        Arguments:
            self: self@Element
            page: htmlPage
        Returns:
            None
        """
        # Add the element the the htmlPages body
        page.BodyElements[self.row] = self.html

class Text(Element):
    def __init__(self, text : str, header : int = -1, htmlid: str = "", htmlclass : str = "") -> None:
        """
        Initiates a Text class
        Arguments:
            self: self@Text
            text: text
            header: (optional) html header value
            htmlid: (optional) html element id
            htmlclass: (optional) html element class
        Returns:
            None
        """
        # Initiate parent class
        super().__init__()

        self.htmlid = htmlid
        self.htmlclass = htmlclass

        # If the header value is greater then 6, make it 6
        # LOGG
        self.header = 6 if header > 6 else header
        
        # Replace line breaks with the html line break element
        self.text = text.replace("\n", "<br>")

        # Create the text tag: <p> if there isn't a header: if there is make a header tag
        self.tag = f'<p>' if header < 0 else f'<h{header}>'
        # Generate a closing tag
        self.closeTag = super().closeTag(self.tag)
        # Add id and class to the opening tag
        cut = 2 if self.tag == "<p>" else 3
        self.tag = self.tag[:cut] + f' id="{self.htmlid}" class="{self.htmlclass}"' + self.tag[cut:]

        # Generate the correct html for the element
        self.html = self.tag + self.text + self.closeTag


class Image(Element):
    def __init__(self, source, size : tuple, altText : str = "Image", htmlid: str = "", htmlclass : str = "") -> None:
        """
        Initiates an Image class
        Arguments:
            self: self@Image
            source: image source
            size: tuple with witdh and height
            altText: (optional) alt text for the image
            htmlid: (optional) html element id
            htmlclass: (optional) html element class
        Returns:
            None
        """
        super().__init__()

        self.htmlid = htmlid
        self.htmlclass = htmlclass

        self.source = source
        self.altText = altText
        self.size = size
        self.width, self.heigt = self.size

        # Generate the correct html for the element
        self.html = f'<img src="{self.source}" alt="{self.altText}" width="{self.width}" heigth="{self.heigt}" id="{self.htmlid}" class="{self.htmlclass}">'


class Link(Element):
    def __init__(self, text : str, url : str) -> None:
        """
        Initiates an Image class
        Arguments:
            self: self@Link
            text: text
            url: url
        Returns:
            None
        """
        super().__init__()

        self.text = text
        self.url = url
        
        # Generate the correct html for the element
        self.html = f'<a href="{self.url}">{self.text}</a>'

class Frame(Element):
    def __init__(self, source: str, size: tuple, title: str = "Frame", htmlid: str = "", htmlclass : str = "") -> None:
        """
        Initiates a Frame class
        Arguments:
            self: self@Frame
            source: url
            size: tuple with witdh and height
            titel: (optional) Frame titel
        Returns:
            None
        """
        super().__init__()

        self.htmlid = htmlid
        self.htmlclass = htmlclass

        self.source = source
        self.title = title
        self.size = size
        self.width, self.heigt = self.size

        # Generate the correct html for the element
        self.html = f'<iframe src="{self.source}" height="{self.heigt}" width="{self.width}" title="{self.title}" id="{self.htmlid}" class="{self.htmlclass}"></iframe>'

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Not Implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        formatted = ""
        for props in self.props:
            formatted += f' {props}=\"{self.props[props]}\"'
        return formatted
    
    def __repr__(self):
        formatted = f"HTMLNode(tag={self.tag}, value={self.value}, children={{ "
        if self.children:
            for child in self.children:
                formatted += f"{child}, "
        else:
            formatted += "None, "
        formatted += "}, props={ "
        if self.props:
            for prop in self.props:
                formatted += f"{prop}: {self.props[prop]}, "
        else:
            formatted += "None, "
        formatted += "})"
        return formatted

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Error: LeafNodes must have values")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        if not self.value:
            raise ValueError("Error: LeafNodes must have values")
        formatted = f"LeafNode(tag={self.tag}, value={self.value}, props={{ "
        if self.props:
            for prop in self.props:
                formatted += f"{prop}: {self.props[prop]}, "
        else:
            formatted += "None, "
        formatted += "})"
        return formatted

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Error: ParentNodes must have tags")
        if not self.children:
            raise ValueError("Error: ParentNodes must have children")
        children_html = ''.join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'
    
    def __repr__(self):
        if not self.tag:
            raise ValueError("Error: ParentNodes must have tags")
        if not self.children:
            raise ValueError("Error: ParentNodes must have children")
        formatted = f"ParentNode(tag={self.tag}, children={{ "
        for child in self.children:
            formatted += f"{child}, "
        formatted += "}, props={ "
        if self.props:
            for prop in self.props:
                formatted += f"{prop}: {self.props[prop]}, "
        else:
            formatted += "None, "
        formatted += "})"
        return formatted
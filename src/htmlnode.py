class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        html = ""
        for prop in self.props:
            html += f' {prop}="{self.props[prop]}"'
        return html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes require a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>'
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes require a tag")
        if self.children is None:
            raise ValueError("Parent nodes must have children")
        if len(self.children) == 1 and type(self.children[0]) is LeafNode:
            return f'<{self.tag}{super().props_to_html()}>{self.children[0].to_html()}</{self.tag}>'
        child_nodes = ''
        for child in self.children:
            child_nodes += child.to_html()
        return f'<{self.tag}>{child_nodes}</{self.tag}>'

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

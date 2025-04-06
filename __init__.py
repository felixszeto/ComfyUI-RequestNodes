

from .get_node import GetRequestNode
from .post_node import PostRequestNode
from .header_node import HeaderNode
from .key_value_node import KeyValueNode


NODE_CLASS_MAPPINGS = { 
    "Get Request Node": GetRequestNode,
    "Post Request Node": PostRequestNode,
    "Header Node": HeaderNode,
    "Key/Value Node": KeyValueNode
}

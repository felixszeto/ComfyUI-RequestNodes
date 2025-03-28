

from .get_node import GetRequestNode
from .post_node import PostRequestNode


NODE_CLASS_MAPPINGS = { 
    "GetRequestNode": GetRequestNode,
    "PostRequestNode": PostRequestNode
}

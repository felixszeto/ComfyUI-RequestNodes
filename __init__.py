

from .get_node import GetRequestNode
from .post_node import PostRequestNode
from .key_value_node import KeyValueNode
from .rest_api_node import RestApiNode
from .string_replace_node import StringReplaceNode
from .retry_setting_node import RetrySettingNode


NODE_CLASS_MAPPINGS = { 
    "Get Request Node": GetRequestNode,
    "Post Request Node": PostRequestNode,
    "Rest Api Node": RestApiNode,
    "Key/Value Node": KeyValueNode,
    "String Replace Node": StringReplaceNode,
    "Retry Settings Node": RetrySettingNode
}



from .get_node import GetRequestNode
from .post_node import PostRequestNode
from .key_value_node import KeyValueNode
from .rest_api_node import RestApiNode
from .string_replace_node import StringReplaceNode
from .retry_setting_node import RetrySettingNode
from .form_post_node import FormPostRequestNode
from .image_to_base64_node import ImageToBase64Node
from .image_to_blob_node import ImageToBlobNode
from .image_list_combiner_node import ChainableUploadImage



NODE_CLASS_MAPPINGS = {
    "Get Request Node": GetRequestNode,
    "Post Request Node": PostRequestNode,
    "Form Post Request Node": FormPostRequestNode,
    "Rest Api Node": RestApiNode,
    "Key/Value Node": KeyValueNode,
    "String Replace Node": StringReplaceNode,
    "Retry Settings Node": RetrySettingNode,
    "Image To Base64 Node": ImageToBase64Node,
    "Image To Blob Node": ImageToBlobNode,
    "Chainable Upload Image": ChainableUploadImage,
}
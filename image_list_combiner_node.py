import torch
import time
import torch.nn.functional as F

class ChainableUploadImage:
    """
    A node that allows uploading an image and adding it to an image batch.
    It can be chained with other nodes of the same type to build a batch of images,
    similar to the default 'Load Image' node but with chaining capability.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # This widget tells the frontend to show an upload button
                "image": ("IMAGE", {"image_upload": True})
            },
            "optional": {
                "image_batch_in": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image_batch_out",)
    FUNCTION = "load_and_chain"
    CATEGORY = "RequestNode/Utils"

    def load_and_chain(self, image, image_batch_in=None):
        # The 'image' parameter from the upload widget is already a tensor.
        # No file loading or conversion is needed.
        
        # 'image' is a tensor of shape [1, H, W, C]
        if image_batch_in is None:
            # Start a new batch with the uploaded image.
            return (image,)
        else:
            # Get the dimensions of the incoming batch
            target_h = image_batch_in.shape[1]
            target_w = image_batch_in.shape[2]

            # Get the dimensions of the new image
            current_h = image.shape[1]
            current_w = image.shape[2]

            # Resize if dimensions don't match
            if current_h != target_h or current_w != target_w:
                # Permute from [B, H, W, C] to [B, C, H, W] for interpolation
                image_permuted = image.permute(0, 3, 1, 2)
                # Resize
                resized_image_permuted = F.interpolate(
                    image_permuted,
                    size=(target_h, target_w),
                    mode='bilinear',
                    align_corners=False
                )
                # Permute back to [B, H, W, C]
                image = resized_image_permuted.permute(0, 2, 3, 1)

            # Concatenate the incoming batch with the new (potentially resized) image tensor.
            combined_tensor = torch.cat((image_batch_in, image), dim=0)
            return (combined_tensor,)

    @classmethod
    def IS_CHANGED(s, image, image_batch_in=None):
        # Since the image is an uploaded tensor, we can't hash a file.
        # We'll return the current time to ensure the node re-executes
        # whenever a new image is uploaded.
        return time.time()

# For ComfyUI to discover this node
NODE_CLASS_MAPPINGS = {
    "ChainableUploadImage": ChainableUploadImage
}

# A friendly name for the node in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "ChainableUploadImage": "Upload and Chain Image"
}
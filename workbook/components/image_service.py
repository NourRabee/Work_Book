import base64
import io

from PIL import Image
from django.core.exceptions import BadRequest


class ImageService:

    def image_field_validation(self, image_file):
        if not image_file.name.endswith(('jpg', 'jpeg', 'png')):
            raise BadRequest("Only JPG, JPEG, and PNG files are allowed.")
        if image_file.size > 2 * 1024 * 1024:  # 2MB limit
            raise BadRequest("Image size should be under 2MB.")
        return image_file

    def image_file_to_binary(self, validated_image_file):
        image = Image.open(validated_image_file)
        buffered = io.BytesIO()
        image.save(buffered, format=image.format)

        return f"{image.format.lower()};base64," + base64.b64encode(buffered.getvalue()).decode("utf-8")

    def binary_to_image_field(self, image_binary):
        image_format, encoded_data = image_binary.split(';base64,')
        decoded_data = base64.b64decode(encoded_data)

        image = Image.open(io.BytesIO(decoded_data))

        output_io = io.BytesIO()
        image.save(output_io, format=image.format)
        output_io.seek(0)

        return image_format, output_io





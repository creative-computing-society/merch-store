import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser as User
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import json
import logging
import string

logger = logging.getLogger(__name__)


class SSOAuthenticationBackend(BaseBackend):

    def authenticate(self, request, sso_token=None):
        if sso_token is None:
            logger.debug("SSO token is None")
            return None

        logger.debug(f"SSO token received: {sso_token}")
        user_info = self.validate_sso_token(sso_token)

        if user_info and not isinstance(user_info, Response):
            try:
                user = User.objects.get(id=user_info["rollNo"])
                logger.debug(f"User with ID {user_info['rollNo']} found in database.")
            except User.DoesNotExist:
                roles = user_info.get("roles", [])
                user_role = "user"
                is_member = any(role["role"].lower() != "user" for role in roles)

                for role in roles:
                    if role["role"].lower() != "user":
                        user_role = role["role"]
                        break

                user = User.objects.create(
                    id=user_info["rollNo"],
                    email=user_info["email"],
                    name=user_info["name"],
                    phone_no=user_info["phone"],
                    position=user_role,
                    profilePic=user_info.get("profilePic", None),
                    is_member=is_member,
                )
                user.set_unusable_password()
                user.save()
                logger.debug(f"User with ID {user_info['rollNo']} created successfully.")
            return user
        logger.debug("User info not valid or token is invalid.")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def validate_sso_token(self, sso_token):
        jwt_secret = settings.JWT_SECRET_KEY

        try:
            payload = jwt.decode(sso_token, jwt_secret, algorithms=["HS256"])
            decrypted_data = decrypt(payload["ex"], jwt_secret)

            logger.debug(f"JWT payload: {payload}")
            return decrypted_data
        except ExpiredSignatureError:
            logger.error("Token Expired")
            return Response(
                {"error": "Token Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidTokenError:
            logger.error("Invalid Token")
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


def decrypt(encrypted_data, key):
    if len(key) != 96:
        raise ValueError("Key must be exactly 96 characters long")

    logging.debug(f"Encrypted data received for decryption: {encrypted_data}")

    if len(encrypted_data) < 32:
        logging.error(
            "Encrypted data is too short to contain a valid IV and ciphertext"
        )
        raise ValueError(
            "Encrypted data is too short to contain a valid IV and ciphertext"
        )

    try:
        iv = bytes.fromhex(encrypted_data[:32])
        encrypted_data = bytes.fromhex(encrypted_data[32:])
        encryption_key = key[:32].encode("utf-8")

        cipher = Cipher(
            algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend()
        )
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding if necessary
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()

        # Decode and strip any excessive whitespace
        decoded_string = decrypted_data.decode("utf-8")
        # Convert to JSON
        json_object = json.loads(decoded_string)

        return json_object

    except (ValueError, json.JSONDecodeError) as e:
        logging.error(
            f"Decryption error: {str(e)} - Likely caused by invalid token format or content"
        )
        raise ValueError("Decryption failed or invalid data format")
import json
import logging

from config.cryto_data import secret_key
from crypto.aes_ecb_base64 import AesEcbBase64

logger = logging.getLogger(__name__)


class ResponseEncrypted():
    def get_response(self, org_id, RC, message, description):
        plain = "{\n" \
                + "	\"RC\":\"" + RC + "\",\n" \
                + "	\"message\":\"" + message + "\",\n" \
                + "	\"description\":\"" + description + "\"\n" \
                + "}";

        aesecb = AesEcbBase64(secret_key)
        ciphered = aesecb.do_encrypt(plain)

        json_res = "{\"organisation_id\":\"" + org_id + "\",\"response\":\"" + ciphered + "\"}";

        return json_res


class ResponsePlain():
    def get_response(self, RC, message, description):
        plain = "{\n" \
                + "	\"RC\":\"" + RC + "\",\n" \
                + "	\"message\":\"" + message + "\",\n" \
                + "	\"description\":\"" + description + "\"\n" \
                + "}";

        msg = json.loads(plain)
        json_res = json.dumps(msg)

        return json_res


class ResponseHeader():
    def get_response(self, org_id, plain_msg):
        aesecb = AesEcbBase64(secret_key)
        ciphered = aesecb.do_encrypt(plain_msg)

        json_res = "{\"organisation_id\":\"" + org_id + "\",\"response\":\"" + ciphered + "\"}";

        return json_res

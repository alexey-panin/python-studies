# Copyright 2017-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.

import json
import time
# import urllib.request
import requests
from jose import jwk, jwt
from jose.utils import base64url_decode

region = 'eu-west-1'
userpool_id = 'eu-west-1_cib6IcI4O'
app_client_id = '6fkhhktt2u8moa2da3ttupdbrv'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)
# instead of re-downloading the public keys every time
# we download them only on cold start
# https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
# with urllib.request.urlopen(keys_url) as f:
#     response = f.read()
#     keys = json.loads(response.decode('utf-8'))['keys']

# above mentioned for some reason didn't work => hardcoded downloaded keys
keys = [
    {
        "alg": "RS256",
        "e": "AQAB",
        "kid": "caIsNK2YWowCqIzIFudRmshGleLA5c9vDjYEmR30+U8=",
        "kty": "RSA",
        "n": "xr799DVK0V71v4oP9WapU73N3uAb3EPgRC5qgjpvIFFtbNusOtGKslvoE4ej9_ddWG7fj7pV1enEK3Vmtm3v_7Fw5PcfdrwuPrLjvR3r0IFVbbz36X0OfxCzaLHja2A3hq2Nu1cPxZ49HtdXBq6k-gV7hUwx8IaGM7AdKpXILePJYKD0RTkqYbTRMhM5H7bNC-US8cG2bFa-PH59DkZz2JyVe-fgUKsdw0WeaIwV2uAvjMXHTRGnyubciGUAeK5LarWAEUPaLF2yiFs_rXXjW7Q144LpirAydhqqH91evX92i-QF5_bsDhiubGKkhoFb-LB3UQENIN3l9b19WV7n2w",
        "use": "sig"
    },
    {
        "alg": "RS256",
        "e": "AQAB",
        "kid": "CRms9FXIl2gz8MuV4b/jzcdPehe2XYgCd+QtGg4s9eQ=",
        "kty": "RSA",
        "n": "z4b6aT-k0bxN59g2yC7Z44Dl-gHt39U44PMQtUcMjD-AeTf2gqMU0XR2xkZprY41zqRhDqJONwCjT1hk45yKu0Peafqf_BuHKI4rOGrbGQQhDuxDPgpyK7TWJ-zSeRUDfKrJg9ykUR-9YTEiJcGtlZgdQMVqYYvSNcz4jRFAavPsly_G0hc2tzJN4UOoKMZTCmtfHswgL57FeOu4lYXoT4kpVBw2dPkomhzRX0d8IniDWmiOTqBqP1tPbuD0NdcvmxFnDOz5tvX_dx9a4B-0w9QhBdB_3itIACeTrmEQ-ctcQx7Q3VYqYgSPxgEpQ2ioIrSrFbeRu9omGbJrahL05w",
        "use": "sig"
    }
]


def lambda_handler(event, context):
    token = event['token']
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        print('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != app_client_id:
        print('Token was not issued for this audience')
        return False
    # now we can use the claims
    print(claims)
    return claims


# the following is useful to make this script executable in both
# AWS Lambda and any other local environments
if __name__ == '__main__':
    # for testing locally you can enter the JWT ID Token here
    event = {'token': 'eyJraWQiOiJjYUlzTksyWVdvd0NxSXpJRnVkUm1zaEdsZUxBNWM5dkRqWUVtUjMwK1U4PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI1MGRmZTk5MS0zMDFjLTRmM2UtYjI0ZC04MTRkZWM2YTAzNjIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfY2liNkljSTRPIiwicGhvbmVfbnVtYmVyX3ZlcmlmaWVkIjpmYWxzZSwiY29nbml0bzp1c2VybmFtZSI6IjUwZGZlOTkxLTMwMWMtNGYzZS1iMjRkLTgxNGRlYzZhMDM2MiIsImF1ZCI6IjZma2hoa3R0MnU4bW9hMmRhM3R0dXBkYnJ2IiwiZXZlbnRfaWQiOiJiMTA2MWZmYi02MWM1LTRlYWItOGYyZC02MzExZjk5NjBjYjUiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTYyODUxODk4MCwicGhvbmVfbnVtYmVyIjoiKzM1ODQ0MDg5MDEwMyIsImV4cCI6MTYyODUyMjU4MCwiaWF0IjoxNjI4NTE4OTgwLCJlbWFpbCI6ImFsZXhzZXkucGFuaW5AZ21haWwuY29tIn0.Y2dGmamuQ1TDx5Vzlgfap2bn3u7JycJdyABNOjGN7pGjLUg-0ojhEGI_Dk71oZKRiwMuoThoCMpyyXyiC2pl_H5_LMHHe_1xPUkfE7x3wLrtmd7qsu4Mt2_I8ow8W2aT-OI4_olHoBKBAJhsS2N_UvRILmRR6Iiqb8Sfy_eNlXk-PrmWXPqRAoF4omJmjm7FGx4_wMPv3OqlfELgLAKNwubnPGoTnqTqQ95mlz04b7vIIoZcfq84xDlr4q8AIit3dD2u_EuOZgL7ZdNh1xSyK0woVAF8HDMvMSgeiTBJjxAYBJ9o3GjelzRUAQVDE0Kvuxl1TDjry-qTXzFgzWBMQw'}
    lambda_handler(event, None)

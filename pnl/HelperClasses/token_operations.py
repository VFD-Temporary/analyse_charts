import jwt
import urllib


class TokenOperation():

    def __init__(self):
        self.SECRET_KEY = "bqjR5hVyimL2B3edKHFl2E3lgk0HDy65j7L0754ABxY="  # key for JWT

    def decode_cookie(self, browser_cookie):
        """Takes the encoded url from the cookie. Returns the decoded cookie value"""
        try:
            decoded_cookie = urllib.parse.unquote(browser_cookie)
            return decoded_cookie
        except Exception as e:
            raise Exception("An error occured while decoding cookie value to utf-8. ", str(e))

    def get_JWT_token(self, decoded_cookie):
        """Takes teh decoded cookie and extracts the JWT token.

        Assumes that the JWT token is of the format:
        "jwtToken=%23s" + "<encoded header>" + "." + "<encoded payload>" + "." + "<signature>"

        Removes the "jwtToken=%23s" and returns the rest"""
        # remove the starting string from the decoded token
        if "jwtToken=%23s" not in decoded_cookie:
            # this indicates that the token was tempered with
            return False
        else:
            jwt_token = decoded_cookie.replace("jwtToken=%23s",
                                               "")  # does not return an result in an error if the string is not present
            return jwt_token

    def verify_integrity_and_return_payload(self, jwt_token):
        """Takes the JWT Token, verifies the hash to make sure it was not tampered
        with and returns the payload"""
        try:
            # checking integrity
            payload = jwt.decode(jwt_token, self.SECRET_KEY, algorithms=['HS256', ])
        except:
            # signature verification failed, no need to raise an exception
            return False
        # signature verification successful
        try:
            user_id = payload["id"]
            return user_id
        except:
            # the key "id" does not exist in the payload
            return False

    def get_user_id(self, browser_cookie):
        """Takes the browser cookie and returns a boolean reponse for whether the request
        is valid and should be provided access to API data it was requesting"""
        decoded_cookie = self.decode_cookie(browser_cookie)
        token = self.get_JWT_token(decoded_cookie)
        user_id = self.verify_integrity_and_return_payload(token)
        # returns the userId
        return user_id
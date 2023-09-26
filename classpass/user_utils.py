from urllib.parse import urlparse

from .extensions import login_manager
from .database.models import Users


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# https://flask-login.readthedocs.io/en/latest/#login-example
# url_has_allowed_host_and_scheme should check if the URL is safe
# for redirects, meaning it matches the request host.
# See Django's url_has_allowed_host_and_scheme for an example.
def url_has_allowed_host_and_scheme(url, allowed_hosts, require_https=False):
    """
    Return True if the URL uses an allowed host and a safe scheme.

    :param url: The URL to check.
    :param allowed_hosts: A set of allowed hostnames.
    :param require_https: If True, only 'https' will be considered a valid scheme.
    :return: True if the URL is safe; False otherwise.
    """
    # Parse the URL
    parsed_url = urlparse(url)

    # Check if the hostname is in the set of allowed hosts
    if parsed_url.hostname not in allowed_hosts:
        return False

    # Check the scheme (http or https)
    if require_https and parsed_url.scheme != 'https':
        return False

    # URL is safe
    return True

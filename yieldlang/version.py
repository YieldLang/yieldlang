_MAJOR = "0"
"""
Major version number.
"""
_MINOR = "1"
"""
Minor version number.
"""
_PATCH = "1"
"""
On main and in a nightly release the patch should be one ahead of the last released build.
"""
_SUFFIX = ""
"""
This is mainly for nightly builds which have the suffix ".dev$DATE".  
See: https://semver.org/#is-v123-a-semantic-version for the semantics.
"""

VERSION_SHORT = "{0}.{1}".format(_MAJOR, _MINOR)
"""
Short version number.
"""
VERSION = "{0}.{1}.{2}{3}".format(_MAJOR, _MINOR, _PATCH, _SUFFIX)
"""
Full version number.
"""

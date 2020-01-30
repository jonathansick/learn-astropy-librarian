# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""The astropy-librarian crawls Astropy's web content and feeds its
search database.
"""

__all__ = ('__version__',)

from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = '0.0.0'

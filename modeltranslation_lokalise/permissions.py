from django.conf import settings
from rest_framework import permissions
from ipware import get_client_ip


class WhitelistIPPermission(permissions.BasePermission):
    """
    Permission check for whitelisted IPs.
    """
    DEFAULT_WHITELISTED_IPS = ['159.69.72.82', '138.201.23.91',
                               '94.130.129.237']

    def has_permission(self, request, view):
        ip_addr, _ = get_client_ip(request)

        whitelisted_ips = getattr(settings, 'LOKALISE_IP_ADDRESSES',
                                  self.DEFAULT_WHITELISTED_IPS)
        if whitelisted_ips == '*':
            return True
        return ip_addr in whitelisted_ips


class LokalisePermission(permissions.BasePermission):
    """
    Permission check for secret header.
    """
    def has_permission(self, request, view):
        x_secret = request.META.get('HTTP_X_SECRET', None)

        if not x_secret:
            return False

        valid_secret = settings.LOKALISE_WEBHOOK_X_SECRET
        return x_secret == valid_secret

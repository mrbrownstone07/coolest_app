def get_client_ip(request):
    """Helper function to get the IP address of the client. 
    Given a request object it returns the IP address of the client.
    
    Args:
        request (Request): pass a Request object
    Returns:
        str: ip address of the client
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    return ip
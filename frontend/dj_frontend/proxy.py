import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def proxy_view(request, upstream_url, path=''):
    """
    A simple reverse proxy view using requests.
    """
    # Construct the full URL
    # If path is empty, we just query upstream_url logic
    if path:
        url = f"{upstream_url.rstrip('/')}/{path.lstrip('/')}"
    else:
        url = upstream_url

    # Forward query parameters
    params = request.GET.copy()

    # Forward headers (excluding some hop-by-hop headers)
    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in ['host', 'content-length']
    }
    
    # Add Standard Proxy Headers
    headers['X-Forwarded-For'] = request.META.get('REMOTE_ADDR')
    headers['X-Forwarded-Host'] = request.get_host()
    headers['X-Forwarded-Proto'] = 'https' if request.is_secure() else 'http'
    
    # Internal K8s service calls don't need the external host header usuallly,
    # or they need the specific service name. Requests will handle Host automatically
    # based on the URL, which is correct for K8s DNS.

    try:
        response = requests.request(
            method=request.method,
            url=url,
            params=params,
            headers=headers,
            data=request.body,
            cookies=request.COOKIES,
            allow_redirects=False # Let the client handle redirects
        )
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Proxy Error: {str(e)}", status=502)

    # Create Django response
    proxy_response = HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers.get('Content-Type')
    )

    # Forward headers back to client
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'set-cookie']
    for key, value in response.headers.items():
        if key.lower() not in excluded_headers:
            proxy_response[key] = value

    # Explicitly handle cookies to ensure attributes are preserved
    for cookie in response.cookies:
        # Avoid overwriting Django's internal cookies
        if cookie.name.lower() in ['csrftoken', 'sessionid']:
            continue
            
        proxy_response.set_cookie(
            key=cookie.name,
            value=cookie.value,
            domain=None,  # Crucial: Don't use upstream domain (e.g. 'grafana')
            path='/',     # CRITICAL: Force root path so browser ALWAYS sends the session cookie
            secure=cookie.secure,
            httponly=cookie.has_nonstandard_attr('HttpOnly') or False,
            expires=cookie.expires,
            samesite='Lax'
        )
            
    return proxy_response

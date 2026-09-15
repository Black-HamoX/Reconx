import requests
import hashlib
from reconx.core.utils import is_valid_email
from reconx.core.banner import print_info, print_success, print_error, print_section
from reconx.core.config import TIMEOUT


def check_gravatar(email):
    h = hashlib.md5(email.strip().lower().encode()).hexdigest()
    url = f"https://www.gravatar.com/avatar/{h}?d=404"
    try:
        r = requests.get(url, timeout=TIMEOUT)
        if r.status_code == 200:
            return f"https://www.gravatar.com/avatar/{h}"
    except requests.RequestException:
        pass
    return None


def run(email, save=False):
    print_section(f"Email Recon: {email}")

    if not is_valid_email(email):
        print_error("Invalid email format")
        return {"email": email, "valid": False}

    results = {"email": email, "valid": True}
    print_success("Valid email format")

    print_info("Checking Gravatar...")
    g = check_gravatar(email)
    if g:
        print_success(f"Gravatar found: {g}")
        results["gravatar"] = g
    else:
        print_error("No Gravatar found")

    if save:
        from reconx.core.utils import save_results
        path = save_results(results, f"email_{email}")
        print_success(f"Saved to {path}")

    return results
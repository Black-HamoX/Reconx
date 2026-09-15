import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from reconx.core.config import TIMEOUT, USER_AGENT, MAX_WORKERS
from reconx.core.banner import print_info, print_success, print_error, print_section

USERNAME_RE = re.compile(r"^[a-zA-Z0-9._-]{2,30}$")

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://instagram.com/{}",
    "Reddit": "https://reddit.com/user/{}",
    "Facebook": "https://facebook.com/{}",
    "TikTok": "https://tiktok.com/@{}",
    "Pinterest": "https://pinterest.com/{}",
    "Telegram": "https://t.me/{}",
    "Medium": "https://medium.com/@{}",
    "DevTo": "https://dev.to/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "Keybase": "https://keybase.io/{}",
    "Patreon": "https://patreon.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Twitch": "https://twitch.tv/{}",
    "YouTube": "https://youtube.com/@{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
}

NOT_FOUND_INDICATORS = [
    "not found",
    "page not found",
    "user not found",
    "doesn't exist",
    "does not exist",
    "sorry, nobody on reddit",
    "this account doesn't exist",
    "couldn't find",
    "no user found",
]


def _check(platform, url):
    try:
        r = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT,
            allow_redirects=True,
        )
        if r.status_code != 200:
            return platform, url, False
        text = r.text.lower()
        for indicator in NOT_FOUND_INDICATORS:
            if indicator in text:
                return platform, url, False
        return platform, url, True
    except requests.RequestException:
        return platform, url, False
    except Exception:
        return platform, url, False


def run(username, save=False):
    print_section(f"Username Recon: {username}")

    if not USERNAME_RE.match(username):
        print_error("Invalid username format (2-30 chars, letters/digits/._-)")
        return {"username": username, "valid": False}

    print_info(f"Checking {len(PLATFORMS)} platforms...\n")

    found = []
    results = {"username": username, "found": [], "checked": len(PLATFORMS)}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(_check, p, u.format(username)) for p, u in PLATFORMS.items()]
        for fut in as_completed(futures):
            try:
                platform, url, exists = fut.result()
            except Exception:
                continue
            if exists:
                print_success(f"{platform:15} -> {url}")
                found.append({"platform": platform, "url": url})
            else:
                print_error(f"{platform:15} -> not found")

    results["found"] = found
    print_info(f"\nTotal found: {len(found)}/{len(PLATFORMS)}")

    if save:
        from reconx.core.utils import save_results
        path = save_results(results, f"username_{username}")
        print_success(f"Saved to {path}")

    return results
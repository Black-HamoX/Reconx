import requests
from reconx.core.banner import print_info, print_success, print_error, print_section
from reconx.core.config import TIMEOUT


def run(ip, save=False):
    print_section(f"IP Recon: {ip}")

    results = {"ip": ip}

    print_info("Querying ip-api.com...")
    try:
        r = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,query",
            timeout=TIMEOUT,
        )
        data = r.json()

        if data.get("status") == "success":
            print_success(f"Country:  {data.get('country')} ({data.get('countryCode')})")
            print_success(f"Region:   {data.get('regionName')}")
            print_success(f"City:     {data.get('city')}")
            print_success(f"Zip:      {data.get('zip')}")
            print_success(f"Lat/Lon:  {data.get('lat')}, {data.get('lon')}")
            print_success(f"Timezone: {data.get('timezone')}")
            print_success(f"ISP:      {data.get('isp')}")
            print_success(f"Org:      {data.get('org')}")
            print_success(f"AS:       {data.get('as')}")
            results.update(data)
        else:
            print_error(f"Error: {data.get('message', 'Unknown')}")
    except requests.RequestException as e:
        print_error(f"Request failed: {e}")

    if save:
        from reconx.core.utils import save_results
        path = save_results(results, f"ip_{ip}")
        print_success(f"Saved to {path}")

    return results
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from reconx.core.banner import print_info, print_success, print_error, print_section


def run(phone, save=False):
    print_section(f"Phone Recon: {phone}")

    if not phone.startswith("+"):
        print_error("Include country code (e.g. +201234567890)")
        return {"phone": phone, "valid": False}

    try:
        pn = phonenumbers.parse(phone, None)
    except phonenumbers.NumberParseException as e:
        print_error(f"Parse error: {e}")
        return {"phone": phone, "valid": False}

    if not phonenumbers.is_valid_number(pn):
        print_error("Invalid phone number")
        return {"phone": phone, "valid": False}

    results = {
        "phone": phone,
        "valid": True,
        "country_code": pn.country_code,
        "national_number": pn.national_number,
    }

    print_success("Valid number")

    region = geocoder.description_for_number(pn, "en")
    if region:
        print_success(f"Region:    {region}")
        results["region"] = region

    car = carrier.name_for_number(pn, "en")
    if car:
        print_success(f"Carrier:   {car}")
        results["carrier"] = car

    tz = timezone.time_zones_for_number(pn)
    if tz:
        print_success(f"Timezone:  {', '.join(tz)}")
        results["timezone"] = list(tz)

    if save:
        from reconx.core.utils import save_results
        path = save_results(results, f"phone_{phone}")
        print_success(f"Saved to {path}")

    return results
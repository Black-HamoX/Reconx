import socket
import dns.resolver
import whois
from reconx.core.utils import is_valid_domain, clean_domain
from reconx.core.banner import print_info, print_success, print_error, print_section
from reconx.core.config import TIMEOUT


def get_whois(domain):
    try:
        w = whois.whois(domain)
        return {
            "registrar": str(w.registrar) if w.registrar else None,
            "creation_date": str(w.creation_date) if w.creation_date else None,
            "expiration_date": str(w.expiration_date) if w.expiration_date else None,
            "name_servers": list(w.name_servers) if w.name_servers else [],
            "emails": w.emails if w.emails else [],
            "org": w.org if w.org else None,
            "country": w.country if w.country else None,
        }
    except Exception as e:
        return {"error": str(e)}


def get_dns_records(domain):
    records = {}
    for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]:
        try:
            answers = dns.resolver.resolve(domain, rtype, lifetime=TIMEOUT)
            records[rtype] = [str(r) for r in answers]
        except Exception:
            records[rtype] = []
    return records


def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


def run(domain, save=False):
    domain = clean_domain(domain)
    print_section(f"Domain Recon: {domain}")

    if not is_valid_domain(domain):
        print_error("Invalid domain format")
        return {"domain": domain, "valid": False}

    results = {"domain": domain, "valid": True}

    print_info("Resolving IP...")
    ip = get_ip(domain)
    if ip:
        print_success(f"IP: {ip}")
        results["ip"] = ip
    else:
        print_error("Could not resolve IP")

    print_info("\nFetching WHOIS...")
    w = get_whois(domain)
    if "error" in w:
        print_error(f"WHOIS error: {w['error']}")
    else:
        for k, v in w.items():
            if v:
                print_success(f"{k:18}: {v}")
    results["whois"] = w

    print_info("\nFetching DNS records...")
    dns_data = get_dns_records(domain)
    for rtype, values in dns_data.items():
        if values:
            print_success(f"{rtype:5} -> {', '.join(values[:5])}")
    results["dns"] = dns_data

    if save:
        from reconx.core.utils import save_results
        path = save_results(results, f"domain_{domain}")
        print_success(f"\nSaved to {path}")

    return results
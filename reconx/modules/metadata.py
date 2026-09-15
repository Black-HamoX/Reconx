import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from reconx.core.banner import print_info, print_success, print_error, print_section


def _convert_gps(gps_info):
    def to_deg(value, ref):
        d, m, s = value
        result = float(d) + float(m) / 60 + float(s) / 3600
        if ref in ["S", "W"]:
            result = -result
        return result

    try:
        lat = to_deg(gps_info[2], gps_info[1])
        lon = to_deg(gps_info[4], gps_info[3])
        return lat, lon
    except Exception:
        return None


def run(image_path, save=False):
    print_section(f"Metadata Recon: {image_path}")

    if not os.path.isfile(image_path):
        print_error("File not found")
        return {"file": image_path, "error": "not found"}

    results = {"file": image_path, "exif": {}}

    try:
        img = Image.open(image_path)
        print_success(f"Format: {img.format} | Size: {img.size}")
        results["format"] = img.format
        results["size"] = img.size

        exif = img._getexif()
        if not exif:
            print_error("No EXIF data found")
            return results

        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                gps_data = {GPSTAGS.get(k, k): v for k, v in value.items()}
                coords = _convert_gps(gps_data)
                if coords:
                    print_success(f"GPS:      {coords[0]}, {coords[1]}")
                    print_success(f"Maps:     https://maps.google.com/?q={coords[0]},{coords[1]}")
                    results["gps"] = coords
                results["exif"]["GPSInfo"] = {str(k): str(v) for k, v in gps_data.items()}
            else:
                print_success(f"{str(tag):20}: {value}")
                results["exif"][str(tag)] = str(value)

    except Exception as e:
        print_error(f"Error: {e}")
        results["error"] = str(e)

    if save:
        from reconx.core.utils import save_results
        path = save_results(results, f"meta_{os.path.basename(image_path)}")
        print_success(f"Saved to {path}")

    return results
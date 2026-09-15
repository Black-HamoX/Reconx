
import argparse
import sys
from reconx import __version__
from reconx.core.banner import print_banner, print_error, clear_screen
from reconx.modules import username, domain, ip, phone, metadata

EXAMPLES_TEXT = """
Examples:
  reconx username john_doe
  reconx email test@example.com
  reconx domain example.com
  reconx ip 8.8.8.8
  reconx phone +201234567890
  reconx metadata photo.jpg
  reconx username john_doe --save
"""


def build_parser():
    parser = argparse.ArgumentParser(
        prog="reconx",
        description="ReconX - OSINT Reconnaissance Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )
    parser.add_argument("-h", "--help", action="help", help="Show this help message and examples")
    parser.add_argument("-v", "--version", action="version", version=f"ReconX {__version__}")

    sub = parser.add_subparsers(dest="command")

    def add_flags(sp):
        sp.add_argument("-s", "--save", action="store_true", help="Save results as JSON to ~/reconx")

    p_u = sub.add_parser("username", help="Search username across platforms", add_help=True)
    p_u.add_argument("target", help="Username")
    add_flags(p_u)

    p_e = sub.add_parser("email", help="Email OSINT", add_help=True)
    p_e.add_argument("target", help="Email address")
    add_flags(p_e)

    p_d = sub.add_parser("domain", help="Domain OSINT", add_help=True)
    p_d.add_argument("target", help="Domain name")
    add_flags(p_d)

    p_i = sub.add_parser("ip", help="IP OSINT", add_help=True)
    p_i.add_argument("target", help="IP address")
    add_flags(p_i)

    p_p = sub.add_parser("phone", help="Phone number OSINT", add_help=True)
    p_p.add_argument("target", help="Phone (with country code)")
    add_flags(p_p)

    p_m = sub.add_parser("metadata", help="Extract EXIF/GPS metadata from an image", add_help=True)
    p_m.add_argument("target", help="Path to image file")
    add_flags(p_m)

    return parser


def run_command(args):
    if args.command == "username":
        username.run(args.target, save=args.save)
    elif args.command == "email":
        from reconx.modules import email as email_module
        email_module.run(args.target, save=args.save)
    elif args.command == "domain":
        domain.run(args.target, save=args.save)
    elif args.command == "ip":
        ip.run(args.target, save=args.save)
    elif args.command == "phone":
        phone.run(args.target, save=args.save)
    elif args.command == "metadata":
        metadata.run(args.target, save=args.save)


def main():
    argv = sys.argv[1:]

    if not argv:
        clear_screen()
        print_banner()
        parser = build_parser()
        parser.print_help()
        return

    if argv[0] in ("-h", "--help"):
        print(EXAMPLES_TEXT)
        return

    if argv[0] in ("-v", "--version"):
        print(f"ReconX {__version__}")
        return

    if argv[0] in ("-s", "--save"):
        return

    parser = build_parser()

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return

    if not args.command:
        parser.print_help()
        return

    try:
        run_command(args)
    except KeyboardInterrupt:
        print_error("\nInterrupted by user")
    except Exception as e:
        print_error(f"Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nInterrupted by user")
        sys.exit(130)

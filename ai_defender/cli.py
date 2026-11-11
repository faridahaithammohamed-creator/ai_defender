import argparse
from ai_defender import __version__, check_status

def main():
    parser = argparse.ArgumentParser(
        prog="ai-defender",
        description="In-Line White-Box Neuro-Probing Library for AI Agent Security"
    )
    parser.add_argument(
        "-v", "--version", 
        action="version", 
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--status", 
        action="store_true", 
        help="Check if AI Defender is working properly"
    )

    args = parser.parse_args()

    if args.status:
        print(check_status())
    else:
        print("Welcome to AI Defender! Use --help to see available commands.")

if __name__ == "__main__":
    main()

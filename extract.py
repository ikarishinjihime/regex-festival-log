
import re
import sys
from pathlib import Path

DEFAULT_LOG = Path(__file__).parent / "data" / "festival_log.txt"

EMAIL = re.compile(r"[a-zA-Z0-9._]+@[a-zA-Z0-9]+[.][a-zA-Z0-9.]+")


PHONE = re.compile(r"010[-. ]\d{4}[-. ]\d{4}")

STUDENT = re.compile(r"\[(202\d{6}) / (\w+)\]")

GITHUB = re.compile(r"https?://github[.]com/[\w.-]+/[\w.-]+")

COUPON = re.compile(r"FEST-2026-[A-Z0-9]{4}")

SALES = re.compile(r"매출: ([\d,]+)원")


def extract(text: str) -> dict:
    sales = [int(amount.replace(",", "")) for amount in SALES.findall(text)]
    return {
        "emails": EMAIL.findall(text),
        "phones": PHONE.findall(text),
        "students": STUDENT.findall(text),
        "github": GITHUB.findall(text),
        "coupons": COUPON.findall(text),
        "sales": sales,
        "sales_total": sum(sales),
    }


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LOG
    result = extract(path.read_text(encoding="utf-8"))

    print("1. 유효한 이메일")
    for email in result["emails"]:
        print("  ", email)

    print("\n2. 휴대폰 번호")
    for phone in result["phones"]:
        print("  ", phone)

    print("\n3. 재학생 (학번, 학과)")
    for student in result["students"]:
        print("  ", student)

    print("\n4-1. GitHub 저장소")
    for url in result["github"]:
        print("  ", url)

    print("\n4-2. 2026년 유효 쿠폰")
    for coupon in result["coupons"]:
        print("  ", coupon)

    print("\n5. 부스별 총매출")
    for amount in result["sales"]:
        print(f"   {amount:>10,}원")
    print(f"   합계 {result['sales_total']:,}원")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

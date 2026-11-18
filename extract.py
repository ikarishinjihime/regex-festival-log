"""대동제·해커톤 통합 운영 로그에서 정규표현식으로 정보를 뽑아낸다.

사용법: python extract.py [로그 파일 경로]
"""

import re
import sys
from pathlib import Path

DEFAULT_LOG = Path(__file__).parent / "data" / "festival_log.txt"

# 1. 이메일: @ 바로 뒤에 글자가 와야 하므로 'hyunwoo@.ac.kr'은 걸리지 않는다.
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")

# 2. 휴대폰: 010 + 구분자(-, ., 공백) + 4자리 + 구분자 + 4자리.
#    앞뒤에 숫자가 더 붙은 경우는 (?<!\d), (?!\d)로 막는다.
PHONE = re.compile(r"(?<!\d)010[-. ]\d{4}[-. ]\d{4}(?!\d)")

# 3. 학번/학과: [202로 시작하는 9자리 / 학과명]
STUDENT = re.compile(r"\[(202\d{6})\s*/\s*([^\]]+?)\s*\]")

# 4-1. GitHub 저장소: github.com/소유자/저장소 (gitlab.com은 호스트가 달라 제외된다)
GITHUB = re.compile(r"https?://github\.com/[\w.-]+/[\w.-]+")

# 4-2. 2026년 발급 쿠폰
COUPON = re.compile(r"\bFEST-2026-[A-Z0-9]{4}\b")

# 5. 부스 총매출: '매출:' 바로 뒤 금액만. 카드/현금 내역과 쿠폰 금액은 앞에 '매출:'이 없다.
SALES = re.compile(r"매출:\s*([\d,]+)원")


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

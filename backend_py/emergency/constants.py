API_ROOT = "https://apis.data.go.kr/B552657/ErmctInfoInqireService"
PAGE_SIZE = 1000
MAX_PAGES = 100
REQUEST_TIMEOUT = 15

SEOUL_ORIGIN = {"lat": 37.5668, "lng": 126.9786}
KOREA_BOUNDS = {
    "min_lat": 33.0,
    "max_lat": 39.0,
    "min_lng": 124.0,
    "max_lng": 132.0,
}

ENDPOINTS = {
    "list": "getEgytListInfoInqire",
    "location": "getEgytLcinfoInqire",
    "basic": "getEgytBassInfoInqire",
    "beds": "getEmrrmRltmUsefulSckbdInfoInqire",
    "messages": "getEmrrmSrsillDissMsgInqire",
    "severe": "getSrsillDissAceptncPosblInfoInqire",
    "traumaList": "getStrmListInfoInqire",
    "traumaLocation": "getStrmLcinfoInqire",
    "traumaBasic": "getStrmBassInfoInqire",
}

REGION = {
    "서울": "서울",
    "인천": "인천",
    "경기": "경기",
    "강원": "강원",
    "충북": ("충북", "충청북도"),
    "충남": ("충남", "충청남도"),
    "대전": "대전",
    "전북": ("전북", "전라북도"),
    "광주": "광주",
    "전남": ("전남", "전라남도"),
    "대구": "대구",
    "경북": ("경북", "경상북도"),
    "부산": "부산",
    "경남": ("경남", "경상남도"),
    "울산": "울산",
}

HIGH_HOSPITAL = {
    "서울": [
        "강북삼성병원",
        "건국대학교병원",
        "경희대학교병원",
        "고려대학교의과대학부속구로병원", "고려대학교구로병원", "고려대학교의과대학부속병원", "고려대학교안암병원", "고대안암병원",
        "삼성서울병원",
        "서울대학교병원",
        "강남세브란스병원",
        "연세대학교의과대학세브란스병원", "신촌세브란스병원",
        "이화여자대학교의과대학부속목동병원", "이화여자대학교목동병원", "이대목동병원",
        "서울아산병원",
        "중앙대학교병원",
        "가톨릭대학교서울성모병원", "서울성모병원"
    ]
}

CACHE_KEY = "emergency_snapshot"
CACHE_TIMEOUT = 60  # 캐시 유지 시간(초)
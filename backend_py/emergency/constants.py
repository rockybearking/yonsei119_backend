"""
[constants.py]
전국 응급의료기관 실시간 정보 시스템의 백엔드 상수 모듈입니다.

- 역할: 공공데이터 OpenAPI 설정, 병원 분류 기준, 병상/장비/중증질환 코드 매핑,
        데이터 파싱 규칙을 한곳에서 관리합니다.

- 구성:
  1. API 통신·캐시·좌표 설정 (API_ROOT, ENDPOINTS, SEOUL_ORIGIN, KOREA_BOUNDS)
  2. 상급종합병원 및 기관 분류 기준 (REGION, HIGH_HOSPITAL, HOSPITAL_GROUPS)
  3. 병상·장비·중증질환·기본정보 한글 매핑 (HV_LABELS, HVS_LABELS, EQUIPMENT 등)
  4. 화면 보드 그룹 구조 (EMERGENCY_BED_ITEMS, INPATIENT_BED_SECTIONS, SEVERE_DISEASE_GROUPS)
  5. 진료공지 교차검증 및 파싱 규칙 (SPECIFIC_BLOCK_TARGETS, MISSING_VALUES 등)
"""

# 1. API 통신 및 캐시 설정
API_ROOT = "https://apis.data.go.kr/B552657/ErmctInfoInqireService"
PAGE_SIZE = 1000
MAX_PAGES = 100
REQUEST_TIMEOUT = 15

CACHE_KEY = "emergency_snapshot"
CACHE_TIMEOUT = 60  # 캐시 유지 시간(초)

# 2. 기본 좌표(서울시청) 및 대한민국 유효 경위도 범위
SEOUL_ORIGIN = {"lat": 37.5668, "lng": 126.9786}
KOREA_BOUNDS = {
    "min_lat": 33.0,
    "max_lat": 39.0,
    "min_lng": 124.0,
    "max_lng": 132.0,
}

# 3. OpenAPI 9대 오퍼레이션 엔드포인트
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

# 4. 지역 접두어 및 제5기(2024~2026) 상급종합병원 47개소 목록
REGION = {
    "서울": ("서울", "서울특별시"),
    "인천": ("인천", "인천광역시"),
    "경기": ("경기", "경기도"),
    "강원": ("강원", "강원특별자치도", "강원도"),
    "충북": ("충북", "충청북도"),
    "충남": ("충남", "충청남도"),
    "대전": ("대전", "대전광역시"),
    "세종": ("세종", "세종특별자치시"),
    "전북": ("전북", "전북특별자치도", "전라북도"),
    "광주": ("광주", "광주광역시"),
    "전남": ("전남", "전라남도"),
    "대구": ("대구", "대구광역시"),
    "경북": ("경북", "경상북도"),
    "부산": ("부산", "부산광역시"),
    "경남": ("경남", "경상남도"),
    "울산": ("울산", "울산광역시"),
    "제주": ("제주", "제주특별자치도", "제주도"),
}

HIGH_HOSPITAL = {
    "서울": [
        "강북삼성병원",
        "건국대학교병원",
        "경희대학교병원",
        "고려대학교의과대학부속구로병원", "고려대학교구로병원",
        "고려대학교의과대학부속병원", "고려대학교안암병원", "고대안암병원",
        "삼성서울병원",
        "서울대학교병원",
        "강남세브란스병원",
        "연세대학교의과대학세브란스병원", "신촌세브란스병원",
        "이화여자대학교의과대학부속목동병원", "이화여자대학교목동병원", "이대목동병원",
        "서울아산병원",
        "중앙대학교병원",
        "가톨릭대학교서울성모병원", "서울성모병원",
        "한양대학교병원",
    ],
    "인천": [
        "가톨릭대학교인천성모병원", "인천성모병원",
        "길병원",
        "인하대학교의과대학부속병원", "인하대학교병원",
    ],
    "경기": [
        "순천향대학교부속부천병원", "순천향대학교부천병원",
        "가톨릭대학교성빈센트병원", "성빈센트병원",
        "고려대학교의과대학부속안산병원", "고려대학교안산병원",
        "분당서울대학교병원",
        "아주대학교병원",
        "한림대학교성심병원",
    ],
    "강원": [
        "강릉아산병원",
        "연세대학교원주세브란스기독병원", "원주세브란스기독병원",
    ],
    "충북": ["충북대학교병원"],
    "충남": ["단국대학교의과대학부속병원", "단국대학교병원"],
    "대전": ["충남대학교병원", "건양대학교병원"],
    "전북": ["원광대학교병원", "전북대학교병원"],
    "광주": ["전남대학교병원", "조선대학교병원"],
    "전남": ["화순전남대학교병원"],
    "대구": [
        "경북대학교병원",
        "계명대학교동산병원",
        "대구가톨릭대학교병원",
        "영남대학교병원",
        "칠곡경북대학교병원",
    ],
    "부산": [
        "고신대학교복음병원",
        "동아대학교병원",
        "부산대학교병원",
        "인제대학교부산백병원", "부산백병원",
    ],
    "경남": [
        "양산부산대학교병원",
        "경상국립대학교병원",
        "삼성창원병원",
    ],
    "울산": ["울산대학교병원"],
}

HOSPITAL_GROUPS = {
    "regional": {"label": "권역응급의료센터", "rank": 0},
    "tertiary": {"label": "상급종합병원", "rank": 1},
    "medical": {"label": "의료원", "rank": 2},
    "other": {"label": "일반·기타 응급의료기관", "rank": 3},
}

# 5. 특수 의료장비 11종 및 기준 매핑
EQUIPMENT = {
    "hvamyn": "구급차",
    "hvangioayn": "혈관촬영기",
    "hvcrrtayn": "지속적 신대체요법(CRRT)",
    "hvctayn": "CT",
    "hvecmoayn": "ECMO",
    "hvhypoayn": "중심체온조절유도기(저체온치료)",
    "hvincuayn": "인큐베이터",
    "hvmriayn": "MRI",
    "hvoxyayn": "고압산소치료기",
    "hvventiayn": "인공호흡기 일반",
    "hvventisoayn": "인공호흡기 조산아",
}

EQUIPMENT_BASELINES = {
    "hvctayn": "hvs27",
    "hvmriayn": "hvs28",
    "hvangioayn": "hvs29",
    "hvventiayn": "hvs30",
    "hvventisoayn": "hvs31",
    "hvincuayn": "hvs32",
    "hvcrrtayn": "hvs33",
    "hvecmoayn": "hvs34",
    "hvhypoayn": "hvs35",
    "hvoxyayn": "hvs37",
}

EQUIPMENT_TABLE_ITEMS = [
    {"label": "인공호흡기 일반", "key": "hvventiayn", "baseline": "hvs30"},
    {"label": "인공호흡기 조산아", "key": "hvventisoayn", "baseline": "hvs31"},
    {"label": "인큐베이터", "key": "hvincuayn", "baseline": "hvs32"},
    {"label": "CRRT", "key": "hvcrrtayn", "baseline": "hvs33"},
    {"label": "ECMO", "key": "hvecmoayn", "baseline": "hvs34"},
    {"label": "중심체온조절유도기", "key": "hvhypoayn", "baseline": "hvs35"},
    {"label": "고압산소치료기", "key": "hvoxyayn", "baseline": "hvs37"},
    {"label": "CT", "key": "hvctayn", "baseline": "hvs27"},
    {"label": "MRI", "key": "hvmriayn", "baseline": "hvs28"},
    {"label": "혈관촬영기", "key": "hvangioayn", "baseline": "hvs29"},
    {"label": "구급차", "key": "hvamyn", "baseline": None},
]

# 6. 실시간 가용 병상(HV) 및 기준 병상(HVS) 레이블
CORE_BED_LABELS = {
    "hvec": "일반(응급실 일반병상)",
    "hvoc": "[기타] 수술실",
    "hvcc": "[중환자실] 신경과",
    "hvncc": "[중환자실] 신생아",
    "hvccc": "[중환자실] 흉부외과",
    "hvicc": "[중환자실] 일반",
    "hvgc": "[입원실] 일반",
    "hvdnm": "예비항목1",
    "hvidate": "입력일시",
    "dutytel3": "응급실 직통전화(기관대표전화)",
}

HV_LABELS = {
    "hv1": "예비항목2",
    "hv2": "[중환자실] 내과",
    "hv3": "[중환자실] 외과",
    "hv4": "외과입원실(정형외과)",
    "hv5": "CT",
    "hv6": "[중환자실] 신경외과",
    "hv7": "혈관촬영기",
    "hv8": "[중환자실] 화상",
    "hv9": "[중환자실] 외상",
    "hv10": "VENTI(소아)",
    "hv11": "인큐베이터(보육기)",
    "hv12": "예비항목3",
    "hv13": "격리진료구역 음압격리병상",
    "hv14": "격리진료구역 일반격리병상",
    "hv15": "소아음압격리",
    "hv16": "소아일반격리",
    "hv17": "[응급전용] 중환자실 음압격리",
    "hv18": "[응급전용] 중환자실 일반격리",
    "hv19": "[응급전용] 입원실 음압격리",
    "hv21": "[응급전용] 입원실 일반격리",
    "hv22": "감염병 전담병상 중환자실",
    "hv23": "감염병 전담병상 중환자실 내 음압격리병상",
    "hv24": "[감염] 중증 병상",
    "hv25": "[감염] 준·중증 병상",
    "hv26": "[감염] 중등증 병상",
    "hv27": "코호트 격리",
    "hv28": "소아",
    "hv29": "응급실 음압 격리 병상",
    "hv30": "응급실 일반 격리 병상",
    "hv31": "[응급전용] 중환자실",
    "hv32": "[중환자실] 소아",
    "hv33": "[응급전용] 소아중환자실",
    "hv34": "[중환자실] 심장내과",
    "hv35": "[중환자실] 음압격리",
    "hv36": "[응급전용] 입원실",
    "hv37": "[응급전용] 소아입원실",
    "hv38": "[입원실] 외상전용",
    "hv39": "[기타] 외상전용 수술실",
    "hv40": "[입원실] 정신과 폐쇄병동",
    "hv41": "[입원실] 음압격리",
    "hv42": "[기타] 분만실",
    "hv43": "[기타] 화상전용처치실",
    "hv60": "외상소생실",
    "hv61": "외상환자진료구역",
}

HVS_LABELS = {
    "hvs01": "일반 기준",
    "hvs02": "소아 기준",
    "hvs03": "응급실 음압 격리 병상 기준",
    "hvs04": "응급실 일반 격리 병상 기준",
    "hvs05": "[응급전용] 중환자실 기준",
    "hvs06": "[중환자실] 내과 기준",
    "hvs07": "[중환자실] 외과 기준",
    "hvs08": "[중환자실] 신생아 기준",
    "hvs09": "[중환자실] 소아 기준",
    "hvs10": "[응급전용] 소아중환자실 기준",
    "hvs11": "[중환자실] 신경과 기준",
    "hvs12": "[중환자실] 신경외과 기준",
    "hvs13": "[중환자실] 화상 기준",
    "hvs14": "[중환자실] 외상 기준",
    "hvs15": "[중환자실] 심장내과 기준",
    "hvs16": "[중환자실] 흉부외과 기준",
    "hvs17": "[중환자실] 일반 기준",
    "hvs18": "[중환자실] 음압격리 기준",
    "hvs19": "[응급전용] 입원실 기준",
    "hvs20": "[응급전용] 소아입원실 기준",
    "hvs21": "[입원실] 외상전용 기준",
    "hvs22": "[기타] 수술실 기준",
    "hvs23": "[기타] 외상전용 수술실 기준",
    "hvs24": "[입원실] 정신과 폐쇄병동 기준",
    "hvs25": "[입원실] 음압격리 기준",
    "hvs26": "[기타] 분만실 기준",
    "hvs27": "CT 기준",
    "hvs28": "MRI 기준",
    "hvs29": "혈관촬영기 기준",
    "hvs30": "인공호흡기 일반 기준",
    "hvs31": "인공호흡기 조산아 기준",
    "hvs32": "인큐베이터 기준",
    "hvs33": "CRRT 기준",
    "hvs34": "ECMO 기준",
    "hvs35": "중심체온조절유도기 기준",
    "hvs36": "[기타] 화상전용처치실 기준",
    "hvs37": "고압산소치료기 기준",
    "hvs38": "[입원실] 일반 기준",
    "hvs46": "격리진료구역 음압격리 기준",
    "hvs47": "격리진료구역 일반격리 기준",
    "hvs48": "소아음압격리 기준",
    "hvs49": "소아일반격리 기준",
    "hvs50": "[응급전용] 중환자실 음압격리 기준",
    "hvs51": "[응급전용] 중환자실 일반격리 기준",
    "hvs52": "[응급전용] 입원실 음압격리 기준",
    "hvs53": "[응급전용] 입원실 일반격리 기준",
    "hvs54": "감염병 전담병상 중환자실 기준",
    "hvs55": "감염병 전담병상 중환자실 내 음압격리병상 기준",
    "hvs56": "[감염] 중증 병상 기준",
    "hvs57": "[감염] 준·중증 병상 기준",
    "hvs58": "[감염] 중등증 병상 기준",
    "hvs59": "코호트 격리 기준",
    "hvs60": "외상소생실 기준",
    "hvs61": "외상환자진료구역 기준",
}

# 7. 기본정보 및 실시간 메시지 필드 레이블
BASIC_FIELD_LABELS = {
    "hpid": "기관ID",
    "phpid": "구 기관ID",
    "rnum": "일련번호",
    "cnt": "건수",
    "distance": "거리",
    "dutyname": "기관명",
    "dutyaddr": "주소",
    "dutytel1": "대표전화1",
    "dutytel3": "응급실전화(대표전화2)",
    "dutyfax": "팩스번호",
    "dutyemcls": "응급의료기관분류코드",
    "dutyemclsname": "응급의료기관분류명",
    "dutydiv": "병원분류코드",
    "dutydivname": "병원분류명",
    "dutylvkl": "응급실레벨",
    "postcdn1": "우편번호1",
    "postcdn2": "우편번호2",
    "wgs84lon": "병원경도(WGS84)",
    "wgs84lat": "병원위도(WGS84)",
    "longitude": "병원경도",
    "latitude": "병원위도",
    "starttime": "시작시간",
    "endtime": "종료시간",
    "dutyhayn": "입원실가용여부(1:가능)",
    "dutyhano": "병상수",
    "dutyinf": "기관설명상세",
    "dutymapimg": "간이약도",
    "dutyeryn": "응급실운영여부(1:운영)",
    "dutytime1s": "진료시작(월요일)",
    "dutytime2s": "진료시작(화요일)",
    "dutytime3s": "진료시작(수요일)",
    "dutytime4s": "진료시작(목요일)",
    "dutytime5s": "진료시작(금요일)",
    "dutytime6s": "진료시작(토요일)",
    "dutytime7s": "진료시작(일요일)",
    "dutytime8s": "진료시작(공휴일)",
    "dutytime1c": "진료종료(월요일)",
    "dutytime2c": "진료종료(화요일)",
    "dutytime3c": "진료종료(수요일)",
    "dutytime4c": "진료종료(목요일)",
    "dutytime5c": "진료종료(금요일)",
    "dutytime6c": "진료종료(토요일)",
    "dutytime7c": "진료종료(일요일)",
    "dutytime8c": "진료종료(공휴일)",
    "dgididname": "진료과목",
    "hpbdn": "총 병상수",
    "hpccuyn": "흉부중환자실 병상수",
    "hpcuyn": "신경중환자실 병상수",
    "hperyn": "응급실 병상수",
    "hpgryn": "입원실 병상수",
    "hpicuyn": "일반중환자실 병상수",
    "hpnicuyn": "신생아중환자실 병상수",
    "hpopyn": "수술실 병상수",
}

MESSAGE_FIELD_LABELS = {
    "emcorgcod": "기관코드",
    "symblkmsg": "전달메시지(공지내용)",
    "symblkmsgtyp": "메시지구분(A:응급/B:중증)",
    "symtypcod": "중증질환구분코드",
    "symtypcodmag": "중증질환구분명",
    "trtprtcodmag": "진료과명",
    "symoutdspyon": "중증질환 표출구분(Y:해제/N:차단)",
    "symoutdspmth": "표출 차단구분(A:자동/B:수동)",
    "symblksttdtm": "차단시작일시",
    "symblkenddtm": "차단종료일시",
}

# 8. 화면 보드용 병상 그룹 구조
EMERGENCY_BED_ITEMS = [
    {"label": "일반", "current": "hvec", "baseline": "hvs01"},
    {"label": "소아", "current": "hv28", "baseline": "hvs02"},
    {"label": "외상소생실", "current": "hv60", "baseline": "hvs60"},
    {"label": "외상환자진료구역", "current": "hv61", "baseline": "hvs61"},
    {"label": "일반격리", "current": "hv30", "baseline": "hvs04"},
    {"label": "음압격리", "current": "hv29", "baseline": "hvs03"},
    {"label": "소아일반격리", "current": "hv16", "baseline": "hvs49"},
    {"label": "소아음압격리", "current": "hv15", "baseline": "hvs48"},
    {"label": "격리진료구역 일반격리", "current": "hv14", "baseline": "hvs47"},
    {"label": "격리진료구역 음압격리", "current": "hv13", "baseline": "hvs46"},
    {"label": "코호트격리", "current": "hv27", "baseline": "hvs59"},
]

INPATIENT_BED_SECTIONS = [
    {
        "title": "중환자실",
        "items": [
            {"label": "일반", "current": "hvicc", "baseline": "hvs17"},
            {"label": "음압격리", "current": "hv35", "baseline": "hvs18"},
            {"label": "소아", "current": "hv32", "baseline": "hvs09"},
            {"label": "신생아", "current": "hvncc", "baseline": "hvs08"},
            {"label": "내과", "current": "hv2", "baseline": "hvs06"},
            {"label": "심장내과", "current": "hv34", "baseline": "hvs15"},
            {"label": "신경과", "current": "hvcc", "baseline": "hvs11"},
            {"label": "화상", "current": "hv8", "baseline": "hvs13"},
            {"label": "외과", "current": "hv3", "baseline": "hvs07"},
            {"label": "신경외과", "current": "hv6", "baseline": "hvs12"},
            {"label": "흉부외과", "current": "hvccc", "baseline": "hvs16"},
        ],
    },
    {
        "title": "응급전용",
        "items": [
            {"label": "입원실", "current": "hv36", "baseline": "hvs19"},
            {"label": "입원실 음압격리", "current": "hv19", "baseline": "hvs52"},
            {"label": "입원실 일반격리", "current": "hv21", "baseline": "hvs53"},
            {"label": "중환자실", "current": "hv31", "baseline": "hvs05"},
            {"label": "중환자실 음압격리", "current": "hv17", "baseline": "hvs50"},
            {"label": "중환자실 일반격리", "current": "hv18", "baseline": "hvs51"},
            {"label": "소아입원실", "current": "hv37", "baseline": "hvs20"},
            {"label": "소아중환자실", "current": "hv33", "baseline": "hvs10"},
        ],
    },
    {
        "title": "외상전용",
        "items": [
            {"label": "중환자실", "current": "hv9", "baseline": "hvs14"},
            {"label": "입원실", "current": "hv38", "baseline": "hvs21"},
            {"label": "수술실", "current": "hv39", "baseline": "hvs23"},
        ],
    },
    {
        "title": "입원실",
        "items": [
            {"label": "일반", "current": "hvgc", "baseline": "hvs38"},
            {"label": "외과입원실(정형외과)", "current": "hv4", "baseline": None},
            {"label": "음압격리", "current": "hv41", "baseline": "hvs25"},
            {"label": "정신과 폐쇄병동", "current": "hv40", "baseline": "hvs24"},
        ],
    },
    {
        "title": "감염병 전담·격리 병상",
        "items": [
            {"label": "감염병 전담 중환자실", "current": "hv22", "baseline": "hvs54"},
            {"label": "감염병 전담 중환자실 내 음압격리", "current": "hv23", "baseline": "hvs55"},
            {"label": "[감염] 중증 병상", "current": "hv24", "baseline": "hvs56"},
            {"label": "[감염] 준·중증 병상", "current": "hv25", "baseline": "hvs57"},
            {"label": "[감염] 중등증 병상", "current": "hv26", "baseline": "hvs58"},
        ],
    },
    {
        "title": "기타",
        "items": [
            {"label": "수술실", "current": "hvoc", "baseline": "hvs22"},
            {"label": "분만실", "current": "hv42", "baseline": "hvs26", "type": "delivery"},
            {"label": "화상전용처치실", "current": "hv43", "baseline": "hvs36"},
        ],
    },
]

# 9. 중증응급질환(27+1종) 메타데이터 및 보드 그룹
MKIOSKTY_METADATA = {
    "mkioskty1": "[재관류중재술] 심근경색",
    "mkioskty2": "[재관류중재술] 뇌경색",
    "mkioskty3": "[뇌출혈수술] 거미막하출혈",
    "mkioskty4": "[뇌출혈수술] 거미막하출혈 외",
    "mkioskty5": "[대동맥응급] 흉부",
    "mkioskty6": "[대동맥응급] 복부",
    "mkioskty7": "[담낭담관질환] 담낭질환",
    "mkioskty8": "[담낭담관질환] 담도포함질환",
    "mkioskty9": "[복부응급수술] 비외상",
    "mkioskty10": "[장중첩/폐색] 영유아",
    "mkioskty11": "[응급내시경] 성인 위장관",
    "mkioskty12": "[응급내시경] 영유아 위장관",
    "mkioskty13": "[응급내시경] 성인 기관지",
    "mkioskty14": "[응급내시경] 영유아 기관지",
    "mkioskty15": "[저체중출생아] 집중치료",
    "mkioskty16": "[산부인과응급] 분만",
    "mkioskty17": "[산부인과응급] 산과수술",
    "mkioskty18": "[산부인과응급] 부인과수술",
    "mkioskty19": "[중증화상] 전문치료",
    "mkioskty20": "[사지접합] 수족지접합",
    "mkioskty21": "[사지접합] 수족지접합 외",
    "mkioskty22": "[응급투석] HD",
    "mkioskty23": "[응급투석] CRRT",
    "mkioskty24": "[정신과적응급] 폐쇄병동입원",
    "mkioskty25": "[안과적수술] 응급",
    "mkioskty26": "[영상의학혈관중재] 성인",
    "mkioskty27": "[영상의학혈관중재] 영유아",
    "mkioskty28": "응급실 (Emergency gate keeper)",
    "mkioskty10msg": "장중첩/폐색(영유아) 가능연령 비고",
    "mkioskty12msg": "위장관 응급내시경(영유아) 가능연령 비고",
    "mkioskty14msg": "기관지 응급내시경(영유아) 가능연령 비고",
    "mkioskty15msg": "저체중 출생아 가능연령 비고",
    "mkioskty27msg": "영상의학 혈관 중재적 시술(영유아) 가능연령 비고",
    "mkioskdate": "키오스크 정보 보고일시 (mkioskdate)",
    "hvidate": "중증질환 정보 보고일시 (hvidate)",
}

SEVERE_DISEASE_GROUPS = [
    {
        "title": "뇌출혈수술",
        "items": [
            {"label": "거미막하출혈", "key": "mkioskty3"},
            {"label": "거미막하출혈 외", "key": "mkioskty4"},
        ],
    },
    {
        "title": "대동맥응급",
        "items": [
            {"label": "흉부", "key": "mkioskty5"},
            {"label": "복부", "key": "mkioskty6"},
        ],
    },
    {
        "title": "담낭담관질환",
        "items": [
            {"label": "담낭질환", "key": "mkioskty7"},
            {"label": "담도포함질환", "key": "mkioskty8"},
        ],
    },
    {
        "title": "복부응급수술",
        "items": [
            {"label": "비외상", "key": "mkioskty9"},
        ],
    },
    {
        "title": "사지접합",
        "items": [
            {"label": "수족지접합", "key": "mkioskty20"},
            {"label": "수족지접합 외", "key": "mkioskty21"},
        ],
    },
    {
        "title": "산부인과응급",
        "items": [
            {"label": "분만", "key": "mkioskty16"},
            {"label": "산과수술", "key": "mkioskty17"},
            {"label": "부인과수술", "key": "mkioskty18"},
        ],
    },
    {
        "title": "안과적수술",
        "items": [
            {"label": "응급", "key": "mkioskty25"},
        ],
    },
    {
        "title": "영상의학혈관중재",
        "items": [
            {"label": "성인", "key": "mkioskty26"},
            {"label": "영유아", "key": "mkioskty27"},
        ],
    },
    {
        "title": "응급내시경",
        "items": [
            {"label": "성인 위장관", "key": "mkioskty11"},
            {"label": "영유아 위장관", "key": "mkioskty12"},
            {"label": "성인 기관지", "key": "mkioskty13"},
            {"label": "영유아 기관지", "key": "mkioskty14"},
        ],
    },
    {
        "title": "응급투석",
        "items": [
            {"label": "HD", "key": "mkioskty22"},
            {"label": "CRRT", "key": "mkioskty23"},
        ],
    },
    {
        "title": "장중첩/폐색",
        "items": [
            {"label": "영유아", "key": "mkioskty10"},
        ],
    },
    {
        "title": "재관류중재술",
        "items": [
            {"label": "심근경색", "key": "mkioskty1"},
            {"label": "뇌경색", "key": "mkioskty2"},
        ],
    },
    {
        "title": "저체중출생아",
        "items": [
            {"label": "집중치료", "key": "mkioskty15"},
        ],
    },
    {
        "title": "정신과적응급",
        "items": [
            {"label": "폐쇄병동입원", "key": "mkioskty24"},
        ],
    },
    {
        "title": "중증화상",
        "items": [
            {"label": "전문치료", "key": "mkioskty19"},
        ],
    },
]

# 10. 실시간 진료공지 ↔ 중증응급질환 차단 매핑 사전
SPECIFIC_BLOCK_TARGETS = {
    "mkioskty1": {"codes": ["Y0010"], "names": ["[재관류중재술] 심근경색", "심근경색", "관상동맥중재술"]},
    "mkioskty2": {"codes": ["Y0020"], "names": ["[재관류중재술] 뇌경색", "뇌경색", "혈전용해술"]},
    "mkioskty3": {"codes": ["Y0031"], "names": ["[뇌출혈수술] 거미막하출혈", "거미막하출혈", "지주막하출혈", "뇌동맥류 수술"]},
    "mkioskty4": {"codes": ["Y0032"], "names": ["[뇌출혈수술] 거미막하출혈 외", "거미막하출혈 외", "기타 뇌출혈"]},
    "mkioskty5": {"codes": ["Y0041"], "names": ["[대동맥응급] 흉부", "대동맥응급(흉부)", "흉부대동맥"]},
    "mkioskty6": {"codes": ["Y0042"], "names": ["[대동맥응급] 복부", "대동맥응급(복부)", "복부대동맥"]},
    "mkioskty7": {"codes": ["Y0051"], "names": ["[담낭담관질환] 담낭질환", "담낭질환", "담낭 수술"]},
    "mkioskty8": {"codes": ["Y0052"], "names": ["[담낭담관질환] 담도포함질환", "담도포함질환", "담도질환"]},
    "mkioskty9": {"codes": ["Y0060"], "names": ["[복부응급수술] 비외상", "복부응급수술(비외상)", "비외상 복부수술"]},
    "mkioskty10": {"codes": ["Y0070"], "names": ["[장중첩/폐색] 영유아", "장중첩/폐색(유아)", "장중첩"]},
    "mkioskty11": {"codes": ["Y0081"], "names": ["[응급내시경] 성인 위장관", "위장관 응급내시경(성인)"]},
    "mkioskty12": {"codes": ["Y0082"], "names": ["[응급내시경] 영유아 위장관", "위장관 응급내시경(영유아)"]},
    "mkioskty13": {"codes": ["Y0091"], "names": ["[응급내시경] 성인 기관지", "기관지 응급내시경(성인)"]},
    "mkioskty14": {"codes": ["Y0092"], "names": ["[응급내시경] 영유아 기관지", "기관지 응급내시경(영유아)"]},
    "mkioskty15": {"codes": ["Y0100"], "names": ["[저출생체중아] 집중치료", "[저체중출생아] 집중치료", "저출생체중아", "저체중출생아"]},
    "mkioskty16": {"codes": ["Y0111"], "names": ["[산부인과응급] 분만", "산부인과 응급(분만)", "분만", "자연분만", "제왕절개"]},
    "mkioskty17": {"codes": ["Y0112"], "names": ["[산부인과응급] 산과수술", "산부인과 응급(산과수술)", "산과수술"]},
    "mkioskty18": {"codes": ["Y0113"], "names": ["[산부인과응급] 부인과수술", "산부인과 응급(부인과수술)", "부인과수술"]},
    "mkioskty19": {"codes": ["Y0120"], "names": ["[중증화상] 전문치료", "중증화상", "화상 전문치료"]},
    "mkioskty20": {"codes": ["Y0131"], "names": ["[사지접합] 수족지접합", "수족지접합"]},
    "mkioskty21": {"codes": ["Y0132"], "names": ["[사지접합] 수족지접합 외", "수족지접합 외"]},
    "mkioskty22": {"codes": ["Y0141"], "names": ["[응급투석] HD", "응급투석(HD)", "응급투석 (HD)", "혈액투석", "인공신장실"]},
    "mkioskty23": {"codes": ["Y0142"], "names": ["[응급투석] CRRT", "응급투석(CRRT)", "응급투석 (CRRT)", "CRRT"]},
    "mkioskty24": {"codes": ["Y0150"], "names": ["[정신과적응급] 폐쇄병동입원", "정신과적 응급입원", "폐쇄병동"]},
    "mkioskty25": {"codes": ["Y0160"], "names": ["[안과적수술] 응급", "안과적 응급 수술", "안과 응급 수술"]},
    "mkioskty26": {"codes": ["Y0171"], "names": ["[영상의학혈관중재] 성인", "영상의학혈관중재(성인)"]},
    "mkioskty27": {"codes": ["Y0172"], "names": ["[영상의학혈관중재] 영유아", "영상의학혈관중재(영유아)"]},
}

# 11. 전체 API 필드 통합 레이블 사전
API_FIELD_LABELS = {
    **BASIC_FIELD_LABELS,
    **MESSAGE_FIELD_LABELS,
    **CORE_BED_LABELS,
    **HV_LABELS,
    **HVS_LABELS,
    **EQUIPMENT,
    **MKIOSKTY_METADATA,
}

# 12. 데이터 파싱·정규화·상태 판별 규칙 상수
MISSING_VALUES = frozenset({
    "", "null", "undefined", "none", "n/a", "nan",
    "-", "−", "–", "—", "정보미제공", "미정보",
})

AVAILABILITY_YES_VALUES = frozenset({"Y", "가능", "1"})
AVAILABILITY_NO_VALUES = frozenset({"N", "N1", "불가", "불가능", "0"})

MSG_TYPE_CRITICAL_VALUES = frozenset({"B", "중증"})
MSG_TYPE_URGENT_VALUES = frozenset({"A", "응급"})
MSG_TYPE_NORMALIZE = {"A": "응급", "응급": "응급", "B": "중증", "중증": "중증"}

MSG_DISPLAY_BLOCK_VALUES = frozenset({"N", "차단"})
MSG_DISPLAY_RELEASE_VALUES = frozenset({"Y", "해제"})
MSG_DISPLAY_YON_NORMALIZE = {"Y": "해제", "해제": "해제", "N": "차단", "차단": "차단"}

MSG_METHOD_NORMALIZE = {"A": "자동", "자동": "자동", "B": "수동", "수동": "수동"}

NOTICE_SAFE_KEYWORDS = ("제한없음", "제한 없음", "가능", "원활")
NOTICE_BLOCK_KEYWORDS = (
    "불가", "불가능", "차단",
    "수용불가", "수용 불가",
    "진료불가", "진료 불가",
    "수술불가", "수술 불가",
    "부재", "중단",
)

BED_RATIO_THRESHOLDS = {
    "congested_max": 0.35,  # 35% 이하: 혼잡(Red)
    "moderate_max": 0.70,   # 70% 미만: 보통(Orange), 70% 이상: 원활(Green)
}

LATITUDE_KEYS = ("wgs84lat", "latitude")
LONGITUDE_KEYS = ("wgs84lon", "longitude")
DUTY_DIV_NAME_KEYS = ("dutydivname", "dutydivnam")

# 13. 진료과목 및 응급의료기관 분류 코드표
DGID_CODE_LABELS = {
    "D001": "내과",
    "D002": "소아청소년과",
    "D003": "신경과",
    "D004": "정신건강의학과",
    "D005": "피부과",
    "D006": "외과",
    "D007": "흉부외과",
    "D008": "정형외과",
    "D009": "신경외과",
    "D010": "성형외과",
    "D011": "산부인과",
    "D012": "안과",
    "D013": "이비인후과",
    "D014": "비뇨기과",
    "D016": "재활의학과",
    "D017": "마취통증의학과",
    "D018": "영상의학과",
    "D019": "치료방사선과",
    "D020": "임상병리과",
    "D021": "해부병리과",
    "D022": "가정의학과",
    "D023": "핵의학과",
    "D024": "응급의학과",
    "D026": "치과",
    "D034": "구강악안면외과",
}

EMERGENCY_CLASS_CODES = {
    "G001": "권역응급의료센터",
    "G006": "지역응급의료센터",
    "G007": "지역응급의료기관",
}
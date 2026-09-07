# MLCalculator

![MLCalculator 성 아이콘](icons/MLCalculator_Castle_512.png)

Million Lords 플레이어 스텟과 도시 업그레이드 비용을 계산하는 앱입니다.
Windows, Android, 모바일 웹 버전 및 기존 Python 원본을 함께 보관합니다.

## 다운로드

[Releases](https://github.com/Darong135/MLCalculator/releases)에서 Windows EXE,
Android 테스트 APK, Google Play용 AAB를 받을 수 있습니다.
비공개 저장소이므로 다운로드에도 저장소 접근 권한이 필요합니다.

## 기능

- 장비 공격력·레벨·병력 또는 직접 입력한 공격력으로 목표 레벨 계산
- 도시 업그레이드 비용, 성벽, 승점, 보유 골드로 가능한 업그레이드 계산
- 한국어, 영어, 일본어, 중국어, 힌디어, 필리핀어, 태국어, 베트남어, 러시아어
- 라이트/다크 모드, 입력값과 설정 저장
- Windows·Android 앱 내부에 화면과 계산 코드 포함: 오프라인 사용 가능

## 소스 구성

| 폴더 | 내용 |
| --- | --- |
| `android/` | Android Gradle 프로젝트와 독립 Vite 프런트엔드 `web/` |
| `windows/` | pywebview 실행기, PyInstaller 빌드 스크립트, 포함된 웹 화면 |
| `website/` | Sites로 배포한 모바일 웹의 React 원본 및 구성 |
| `legacy-python/` | 통합 Tkinter 계산기와 초기 Player Stats Python 원본 |
| `icons/` | 성 아이콘 SVG 및 PNG |

## Windows 빌드

Python 3.12 64비트 가상환경에서 실행합니다.

```powershell
cd windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\build.ps1
```

결과는 `windows/dist/MLCalculator.exe`입니다. 실행 PC에는 Python이 필요 없지만
Windows 10/11 64비트와 Microsoft Edge WebView2 Runtime이 필요합니다.
설정은 `%LOCALAPPDATA%\MLCalculator` 아래에 저장됩니다.
Windows 코드 서명 인증서는 적용하지 않았습니다.

Windows 화면을 수정할 때는 `android/web/`의 React 원본을 수정하고
`pnpm build`로 생성된 `android/app/src/main/assets/www/` 내용을
`windows/www/`에 복사한 뒤 EXE를 다시 빌드합니다.

## Android 빌드

JDK 17 또는 21, Android SDK 36, Build Tools 36.0.0이 필요합니다.
`ANDROID_HOME` 또는 로컬 `android/local.properties`로 SDK 경로를 지정합니다.

```powershell
cd android
.\gradlew.bat assembleDebug
```

릴리스 AAB는 로컬 서명키와 `signing.properties`를 준비한 후
`gradlew.bat bundleRelease`로 빌드합니다. 서명키와 비밀번호는 GitHub에 포함하지 않았습니다.
기존 Play 앱 업데이트에는 원래 업로드 서명키를 유지해야 합니다.
패키지명은 `com.arcana.mlcalculator`, 현재 Android 버전은 1.0.3, versionCode는 4입니다.

## 웹 원본

`android/web/`는 독립 Vite 앱이며 `pnpm install`, `pnpm dev`로 개발할 수 있습니다.
`website/`는 기존 Sites 배포 구성의 백업이며, 배포 프로젝트 설정은 원래 환경에 연결되어 있습니다.
이 저장소에 푸시하는 것만으로 기존 사이트가 자동 배포되지는 않습니다.

## 보관 및 검증

서명키, 비밀번호, 로컬 SDK 경로, 사용자 저장값, 의존성 폴더는 제외했습니다.
계산식은 기존 Python과 200개 도시 사례를 비교했고, Windows EXE의 화면 로드,
탭 전환, 도시 계산, 테마 변경과 재실행 시 복원을 확인했습니다.
Android는 빌드·lint·번들 구조 검증을 수행했으며 실기기 검증은 별도로 필요합니다.

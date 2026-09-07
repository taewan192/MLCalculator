# MLCalculator Windows

배포 파일 `MLCalculator.exe`를 더블 클릭하면 실행됩니다. Python 설치는 필요 없습니다.
Windows 10/11 64비트, Microsoft Edge WebView2 Runtime이 필요합니다.
WebView2가 없는 PC는 Microsoft 공식 페이지에서 런타임을 먼저 설치하세요:
https://developer.microsoft.com/microsoft-edge/webview2/

모바일 앱의 플레이어 스텟, 도시 계산기, 9개 언어, 라이트/다크 테마를 그대로 포함합니다.
성 모양 아이콘이 실행 파일과 창에 적용됩니다. 앱의 계산과 화면은 인터넷 없이 작동합니다.
입력값과 설정은 `%LOCALAPPDATA%\MLCalculator\WebView2`에 저장됩니다.
모바일 기기와 PC의 저장 데이터는 별개입니다.
한 번에 하나의 창을 실행하며, 내부 화면 제공에 로컬 포트 18743을 사용합니다.
Windows 배포용 코드 서명 인증서는 적용하지 않았습니다.

## 원본 재빌드

Python 3.12 64비트 가상환경에서 `pip install -r requirements.txt`를 실행하고
PowerShell에서 `./build.ps1`을 실행하면 `dist/MLCalculator.exe`가 생성됩니다.
`www`는 모바일 앱과 동일한 웹 화면의 빌드 결과입니다.
소스 ZIP의 `frontend` 폴더에 수정 가능한 React/TypeScript 원본이 들어 있습니다.
프런트엔드 수정 후에는 Vite 빌드 결과를 `www`에 교체하고 EXE를 다시 빌드하세요.

## 검증

완성된 EXE의 숨김 Windows 창에서 React 화면 로드, 3개 탭 전환,
도시 1개 레벨 1→2 계산 결과 9, 설정 화면, 다크 모드 전환을 확인했습니다.
이전 실행에서 저장한 다크 모드가 완성 EXE 재실행 시 복원되는 것도 확인했습니다.
모든 PC 환경에서의 설치 테스트와 배포 인증서 서명은 수행하지 않았습니다.

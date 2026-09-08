# MLCalculator Android

- 앱 이름: MLCalculator
- 패키지: com.arcana.mlcalculator
- 버전: 1.1.1 (versionCode 5)
- 최소 Android: 8.0 (API 26)
- 대상 Android: 16 (API 36)

## 앱 기능
플레이어 스텟, 도시 계산기, 예상 모집, 9개 언어, 다크/화이트 모드를 포함합니다.
플레이어 스텟과 예상 모집에서 `다이아 & 레전드`·`플&골&실` 그룹을 선택할 수 있습니다.
화면과 계산 코드를 앱 내부에 포함했습니다. 로그인이나 인터넷 없이 작동하며, 입력값과 설정은 앱 내부 WebView 저장소에 저장됩니다.

## 빌드
JDK 17 또는 21, Android SDK 36, Build Tools 36.0.0을 준비하세요.
`local.properties`에 SDK 위치를 지정하거나 ANDROID_HOME을 설정하세요.

기존 웹 파일은 app/src/main/assets/www에 포함되어 있습니다.
웹 화면을 수정한 경우 web 폴더에서 pnpm install 후 pnpm build를 실행하세요.
Android 소스 루트에서 gradlew.bat bundleRelease lintRelease를 실행하세요.

릴리스 서명에는 별도로 제공한 MLCalculator_Signing_Backup.zip의 upload-key.jks와 signing.properties를 이 소스 루트에 복원해야 합니다.
서명키는 소스 ZIP에는 포함하지 않았습니다.

## 업데이트
기존 applicationId와 업로드 서명키를 유지하고, 새 버전마다 versionCode를 증가시키세요.

## Google Play 제출
MLCalculator-1.1.1-release.aab를 Play Console의 릴리스 화면에 업로드하세요.
스토어 설명, 스크린샷, 개인정보처리방침, 데이터 보안 및 콘텐츠 등급 응답, 테스트/심사 절차는 Play Console에서 별도로 작성해야 합니다.
AAB 생성 및 서명 검증은 Google Play 심사 승인과 별개입니다.

## 검증 범위
기존 Python 계산식과 200개 사례 비교를 통과했습니다.
Android 릴리스 빌드, lint 및 bundletool 구조 검사와 서명 검증 결과는 별도 빌드 보고서를 참고하세요.
연결된 안드로이드 기기가 없어 실기기 실행은 확인하지 못했습니다. 테스트 APK를 기기에 설치해 입력, 키보드, 언어, 테마, 뒤로가기 동작을 확인하세요.

## 참고
- https://developer.android.com/google/play/requirements/target-sdk
- https://developer.android.com/develop/ui/views/layout/webapps/load-local-content

"""MLCalculator Windows wrapper; bundled React assets run entirely locally."""
import ctypes
import json
import os
from pathlib import Path
import sys
import time
import traceback

APP_DIR = Path(__file__).resolve().parent
TEST = '--smoke-test' in sys.argv
DATA_DIR = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'MLCalculator'
if TEST:
    DATA_DIR = Path(sys.argv[sys.argv.index('--smoke-test') + 1]).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)


def main():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Arcana.MLCalculator.Desktop')
    kernel = ctypes.windll.kernel32
    kernel.CreateMutexW.restype = ctypes.c_void_p
    mutex = kernel.CreateMutexW(None, False, 'Local\\MLCalculator.Desktop' + ('.Test' if TEST else ''))
    if kernel.GetLastError() == 183:
        ctypes.windll.user32.MessageBoxW(None, 'MLCalculator가 이미 실행 중입니다.', 'MLCalculator', 0x40)
        return
    import webview
    window = webview.create_window(
        'MLCalculator', str(APP_DIR / 'www' / 'index.html'),
        width=560, height=880, min_size=(390, 600), background_color='#F2F5FA', hidden=TEST,
        text_select=True,
    )

    def smoke():
        report = {}
        try:
            def js(script):
                raw = window.run_js('JSON.stringify(' + script + ')')
                return json.loads(raw) if isinstance(raw, str) else raw
            for _ in range(60):
                time.sleep(0.5)
                if js("document.querySelectorAll('.bottom-nav [role=tab]').length") == 3:
                    break
            report['title'] = js('document.title')
            report['tabs'] = js("Array.from(document.querySelectorAll('.bottom-nav [role=tab]')).map(x=>x.textContent)")
            assert len(report['tabs']) == 3, report
            report['restored'] = js("JSON.parse(localStorage.getItem('mlcalculator') || '{}')")
            report['dark'] = js("document.documentElement.classList.contains('dark')")
            report['lang'] = js('document.documentElement.lang')
            window.run_js("document.querySelectorAll('.bottom-nav [role=tab]')[1].click()")
            time.sleep(0.5)
            window.run_js("document.querySelector('.primary-action').click()")
            time.sleep(0.5)
            report['cityResult'] = js("document.querySelector('.gold-result')?.innerText")
            assert report['cityResult'], report
            window.run_js("document.querySelectorAll('.bottom-nav [role=tab]')[2].click()")
            time.sleep(0.5)
            report['settings'] = js("!!document.querySelector('.language-select') && document.querySelectorAll('.theme-switch [role=tab]').length === 2")
            assert report['settings'], report
            window.run_js("document.querySelectorAll('.theme-switch [role=tab]')[1].click()")
            time.sleep(0.5)
            assert js("document.documentElement.classList.contains('dark')")
            report['saved'] = js("JSON.parse(localStorage.getItem('mlcalculator'))")
            report['ok'] = True
        except Exception:
            report['error'] = traceback.format_exc()
        finally:
            (DATA_DIR / 'smoke-result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
            window.destroy()

    webview.start(smoke if TEST else None, gui='edgechromium', private_mode=False,
                  storage_path=str(DATA_DIR / 'WebView2'), http_port=18744 if TEST else 18743,
                  debug=False)
    kernel.CloseHandle(ctypes.c_void_p(mutex))


if __name__ == '__main__':
    try:
        main()
    except Exception:
        (DATA_DIR / 'error.log').write_text(traceback.format_exc(), encoding='utf-8')
        if not TEST:
            ctypes.windll.user32.MessageBoxW(None,
                '프로그램을 실행하지 못했습니다. Microsoft Edge WebView2 Runtime 설치를 확인하세요.\n오류 기록: ' + str(DATA_DIR / 'error.log'),
                'MLCalculator', 0x10)
        raise

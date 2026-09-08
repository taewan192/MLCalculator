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
                if js("document.querySelectorAll('.bottom-nav [role=tab]').length") == 4:
                    break
            report['title'] = js('document.title')
            report['tabs'] = js("Array.from(document.querySelectorAll('.bottom-nav [role=tab]')).map(x=>x.textContent)")
            assert len(report['tabs']) == 4, report
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
            def fill(name, value):
                window.run_js("var el=document.querySelector('input[name=" + name + "]'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el," + json.dumps(value) + "); el.dispatchEvent(new Event('input',{bubbles:true}));")
                time.sleep(0.15)
            window.run_js("document.querySelectorAll('.bottom-nav [role=tab]')[0].click()")
            time.sleep(0.4)
            report['koreanLeagueLabels'] = js("Array.from(document.querySelectorAll('.playerLeague [role=tab]')).map(x=>x.textContent)")
            assert report['koreanLeagueLabels'] == ['다이아 & 레전드', '플&골&실'], report
            fill('troops', '1G')
            fill('equipment', '300')
            fill('level', '105')
            window.run_js("document.querySelectorAll('.playerLeague [role=tab]')[0].click()")
            time.sleep(0.2)
            window.run_js("document.querySelector('.primary-action').click()")
            time.sleep(0.3)
            report['diamondAttack'] = js("document.querySelector('[data-testid=attack-total]').textContent")
            assert report['diamondAttack'] == '8.16G', report
            window.run_js("document.querySelectorAll('.playerLeague [role=tab]')[1].click()")
            time.sleep(0.2)
            assert js("document.querySelector('[data-testid=attack-total]').textContent") == '—'
            window.run_js("document.querySelector('.primary-action').click()")
            time.sleep(0.3)
            report['platinumAttack'] = js("document.querySelector('[data-testid=attack-total]').textContent")
            assert report['platinumAttack'] == '6.08G', report
            fill('direct', '4.73M')
            window.run_js("document.querySelector('.secondary-action').click()")
            time.sleep(0.3)
            report['directTarget'] = js("document.querySelector('.level-value').textContent")
            assert report['directTarget'] == 'LV.62', report
            window.run_js("document.querySelectorAll('.bottom-nav [role=tab]')[2].click()")
            time.sleep(0.4)
            fill('production', '3G')
            fill('recruitEquipment', '360')
            fill('recruitLevel', '110')
            window.run_js("document.querySelectorAll('.recruitLeague [role=tab]')[0].click()")
            time.sleep(0.2)
            window.run_js("document.querySelector('.primary-action').click()")
            time.sleep(0.4)
            report['diamondRecruitment'] = js("document.querySelector('[data-testid=recruit-total]').textContent")
            assert report['diamondRecruitment'] == '30.4G', report
            window.run_js("document.querySelectorAll('.recruitLeague [role=tab]')[1].click()")
            time.sleep(0.2)
            assert js("document.querySelector('[data-testid=recruit-total]').textContent") == '—'
            window.run_js("document.querySelector('.primary-action').click()")
            time.sleep(0.4)
            report['platinumRecruitment'] = js("document.querySelector('[data-testid=recruit-total]').textContent")
            assert report['platinumRecruitment'] == '20.6G', report
            window.run_js("document.querySelectorAll('.bottom-nav [role=tab]')[3].click()")
            time.sleep(0.5)
            report['settings'] = js("!!document.querySelector('.language-select') && document.querySelectorAll('.theme-switch [role=tab]').length === 2")
            assert report['settings'], report
            window.run_js("document.querySelectorAll('.theme-switch [role=tab]')[1].click()")
            time.sleep(0.5)
            assert js("document.documentElement.classList.contains('dark')")
            report['saved'] = js("JSON.parse(localStorage.getItem('mlcalculator'))")
            window.run_js("var s=JSON.parse(localStorage.getItem('mlcalculator'));s.lang='en';localStorage.setItem('mlcalculator',JSON.stringify(s));location.reload()")
            for _ in range(30):
                time.sleep(0.3)
                try:
                    if js("document.documentElement.lang") == 'en':
                        break
                except Exception:
                    pass
            report['englishLeagueLabels'] = js("Array.from(document.querySelectorAll('.playerLeague [role=tab]')).map(x=>x.textContent)")
            assert report['englishLeagueLabels'] == ['Dia & LL', 'P,G,S'], report
            window.run_js("var s=JSON.parse(localStorage.getItem('mlcalculator'));s.lang='ko';localStorage.setItem('mlcalculator',JSON.stringify(s))")
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

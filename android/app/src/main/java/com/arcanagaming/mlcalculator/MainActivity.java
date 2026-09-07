package com.arcanagaming.mlcalculator;
import android.app.Activity;
import android.os.Bundle;
import android.os.Build;
import android.graphics.Color;
import android.view.WindowInsets;
import android.view.View;
import android.webkit.*;
import android.widget.FrameLayout;
import androidx.webkit.WebViewAssetLoader;
import java.io.ByteArrayInputStream;
public class MainActivity extends Activity {
    private WebView web;
    private FrameLayout root;
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        root = new FrameLayout(this);
        root.setBackgroundColor(Color.rgb(37,99,235));
        setContentView(root);
        if (Build.VERSION.SDK_INT >= 30) {
            getWindow().setDecorFitsSystemWindows(false);
            root.setOnApplyWindowInsetsListener((v,insets)-> {
                android.graphics.Insets bars=insets.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                android.graphics.Insets ime=insets.getInsets(WindowInsets.Type.ime());
                v.setPadding(bars.left,bars.top,bars.right,Math.max(bars.bottom,ime.bottom));
                return insets;
            });
        }
        createWebView();
        if (Build.VERSION.SDK_INT >= 33) getOnBackInvokedDispatcher().registerOnBackInvokedCallback(android.window.OnBackInvokedDispatcher.PRIORITY_DEFAULT,this::handleBack);
    }
    // Only bundled same-origin assets execute JavaScript; all network requests are blocked.
    @android.annotation.SuppressLint("SetJavaScriptEnabled")
    private void createWebView() {
        web=new WebView(this);
        web.setBackgroundColor(Color.rgb(242,245,250));
        root.addView(web,new FrameLayout.LayoutParams(-1,-1));
        WebSettings settings=web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setSupportMultipleWindows(false);
        WebView.setWebContentsDebuggingEnabled(false);
        final WebViewAssetLoader loader=new WebViewAssetLoader.Builder().addPathHandler("/assets/",new WebViewAssetLoader.AssetsPathHandler(this)).build();
        web.setWebViewClient(new WebViewClient(){
            @Override public WebResourceResponse shouldInterceptRequest(WebView view,WebResourceRequest request){
                WebResourceResponse response=loader.shouldInterceptRequest(request.getUrl());
                return response!=null?response:new WebResourceResponse("text/plain","UTF-8",403,"Blocked",java.util.Collections.emptyMap(),new ByteArrayInputStream(new byte[0]));
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view,WebResourceRequest request){ return !"appassets.androidplatform.net".equals(request.getUrl().getHost()); }
            @Override public boolean onRenderProcessGone(WebView view,RenderProcessGoneDetail detail){root.removeView(view);view.destroy();createWebView();return true;}
        });
        web.loadUrl("https://appassets.androidplatform.net/assets/www/index.html");
    }
    private void handleBack(){ if(web.canGoBack())web.goBack();else finish(); }
    @Override protected void onPause(){super.onPause();web.onPause();}
    @Override protected void onResume(){super.onResume();if(web!=null)web.onResume();}
    @Override protected void onDestroy(){if(web!=null){root.removeView(web);web.destroy();}super.onDestroy();}
}

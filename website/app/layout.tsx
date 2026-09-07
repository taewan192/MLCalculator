import type { Metadata, Viewport } from 'next';
import './globals.css';
export const metadata: Metadata={title:'Million Lords · Mobile',description:'플레이어 스텟과 도시 업그레이드를 위한 모바일 계산기'};
export const viewport:Viewport={width:'device-width',initialScale:1,viewportFit:'cover',themeColor:'#2563eb'};
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="ko"><body>{children}</body></html>}

import React from 'react';
import {registerRoot, Composition, AbsoluteFill, Sequence, OffthreadVideo, Img, staticFile, useCurrentFrame, interpolate, spring, useVideoConfig, Easing} from 'remotion';

const FPS = 30;
const GOLD = '#B4935A';
const fontCss = [400, 600, 800].map((w) => `@font-face{font-family:Outfit;font-weight:${w};src:url(${staticFile(`outfit-latin-${w}-normal.woff2`)}) format('woff2');}`).join('');

type Shot = {src: string; dur: number; from?: number; text?: string; grade: string; zoom?: [number, number]; origin?: string; blur?: boolean; scale?: number; shiftY?: number};
// Durées en secondes. Le film bascule du froid (plans 1 à 3) au chaud (plans 4 à 6).
const COLD = 'saturate(0.82) contrast(1.1) brightness(0.94)';
const WARM = 'saturate(1.05) contrast(1.08)';
const SHOTS: Shot[] = [
  {src: 'p1.mp4', dur: 4.4, text: 'L’hiver est là.', grade: COLD, zoom: [1.0, 1.06]},
  {src: 'p2a.mp4', dur: 2.6, from: 0.4, text: 'Le froid. Le sel. Le givre.', grade: COLD, zoom: [1.04, 1.1]},
  {src: 'p2b.mp4', dur: 1.5, from: 1.0, grade: COLD, zoom: [1.1, 1.16]},
  {src: 'p3.mp4', dur: 3.7, text: 'Mais un gardien veille.', grade: COLD, blur: true},
  {src: 'p4.mp4', dur: 3.2, from: 0.3, grade: WARM, zoom: [1.0, 1.05]},
  {src: 'p5.mp4', dur: 2.8, from: 0.2, grade: 'saturate(0.9) contrast(1.08)', zoom: [1.0, 1.05]},
  {src: 'p6.mp4', dur: 3.6, text: 'Votre voiture ne craint plus l’hiver.', grade: WARM, scale: 1.2, shiftY: 1.7, zoom: [1.0, 1.04]},
];
const END = 3.8;
const f = (s: number) => Math.round(s * FPS);
export const TOTAL = SHOTS.reduce((a, s) => a + f(s.dur), 0) + f(END);

const Caption: React.FC<{text: string; dur: number}> = ({text, dur}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const words = text.split(' ');
  const out = interpolate(frame, [dur - 10, dur - 2], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const line = interpolate(frame, [6, 26], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', padding: '0 110px 120px', opacity: out}}>
      <div style={{height: 4, width: 90 * line, background: GOLD, marginBottom: 26}} />
      <div style={{fontFamily: 'Outfit', fontWeight: 800, fontSize: 84, lineHeight: 1.05, color: '#fff', letterSpacing: '-0.01em', textShadow: '0 4px 30px rgba(0,0,0,.55)', maxWidth: 1300}}>
        {words.map((w, i) => {
          const s = spring({frame: frame - 8 - i * 3, fps, config: {damping: 200}});
          return <span key={i} style={{display: 'inline-block', overflow: 'hidden', verticalAlign: 'top', marginRight: '0.26em', paddingBottom: 8}}>
            <span style={{display: 'inline-block', transform: `translateY(${(1 - s) * 105}%)`}}>{w}</span>
          </span>;
        })}
      </div>
    </AbsoluteFill>
  );
};

const Clip: React.FC<{s: Shot; dur: number}> = ({s, dur}) => {
  const frame = useCurrentFrame();
  const z = s.zoom ? interpolate(frame, [0, dur], s.zoom) : 1;
  const base = s.scale ?? 1;
  const t = frame / FPS;
  // Plaque du plan 3 : le cache flou suit la voiture qui grossit.
  const bx = interpolate(t, [0, 1.3, 2.6, 3.9], [0.755, 0.785, 0.812, 0.855]);
  const by = interpolate(t, [0, 1.3, 2.6, 3.9], [0.602, 0.615, 0.645, 0.688]);
  const bw = interpolate(t, [0, 3.9], [0.095, 0.165]);
  const bh = interpolate(t, [0, 3.9], [0.042, 0.068]);
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${base * z}) translateY(${s.shiftY ?? 0}%)`, transformOrigin: s.origin ?? '50% 50%', filter: s.grade}}>
        <OffthreadVideo src={staticFile(s.src)} startFrom={f(s.from ?? 0)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        {s.blur ? <div style={{position: 'absolute', left: `${(bx - bw / 2) * 100}%`, top: `${(by - bh / 2) * 100}%`, width: `${bw * 100}%`, height: `${bh * 100}%`, backdropFilter: 'blur(14px)', WebkitBackdropFilter: 'blur(14px)', borderRadius: 8}} /> : null}
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,.18) 0%, rgba(0,0,0,0) 30%, rgba(0,0,0,0) 52%, rgba(0,0,0,.62) 100%)'}} />
      {s.text ? <Caption text={s.text} dur={dur} /> : null}
    </AbsoluteFill>
  );
};

const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = (d: number) => spring({frame: frame - d, fps, config: {damping: 200}});
  const row = (d: number): React.CSSProperties => ({opacity: a(d), transform: `translateY(${(1 - a(d)) * 30}px)`});
  return (
    <AbsoluteFill style={{background: '#0E1418', alignItems: 'center', justifyContent: 'center', fontFamily: 'Outfit', color: '#fff', textAlign: 'center'}}>
      <Img src={staticFile('logo.png')} style={{height: 250, ...row(4)}} />
      <div style={{height: 3, width: 120 * a(14), background: GOLD, margin: '38px 0 34px'}} />
      <div style={{fontSize: 40, fontWeight: 400, color: 'rgba(255,255,255,.82)', ...row(16)}}>Nettoyage auto à domicile · Essonne et Seine-et-Marne</div>
      <div style={{fontSize: 96, fontWeight: 800, marginTop: 22, letterSpacing: '-0.01em', ...row(24)}}>Dès 49 €</div>
      <div style={{fontSize: 38, fontWeight: 600, marginTop: 26, letterSpacing: '0.04em', ...row(32)}}>continentaldetailing.fr <span style={{color: GOLD, margin: '0 18px'}}>·</span> 07 50 87 59 64</div>
    </AbsoluteFill>
  );
};

const Film: React.FC = () => {
  const frame = useCurrentFrame();
  let at = 0;
  const fadeIn = interpolate(frame, [0, 14], [1, 0], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <style>{fontCss}</style>
      {SHOTS.map((s, i) => {
        const d = f(s.dur);
        const el = <Sequence key={i} from={at} durationInFrames={d}><Clip s={s} dur={d} /></Sequence>;
        at += d;
        return el;
      })}
      <Sequence from={at} durationInFrames={f(END)}><EndCard /></Sequence>
      <AbsoluteFill style={{background: '#000', opacity: fadeIn}} />
    </AbsoluteFill>
  );
};

registerRoot(() => <Composition id="Hiver" component={Film} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080} />);

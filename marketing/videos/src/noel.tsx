import React from 'react';
import {registerRoot, Composition, AbsoluteFill, Sequence, OffthreadVideo, Img, staticFile, useCurrentFrame, interpolate, spring, useVideoConfig, Easing, random} from 'remotion';

const FPS = 30;
const GOLD = '#B4935A';
const RED = '#B4232A';
const NIGHT = '#0E1418';
const fontCss = [400, 600, 800].map((w) => `@font-face{font-family:Outfit;font-weight:${w};src:url(${staticFile(`outfit-latin-${w}-normal.woff2`)}) format('woff2');}`).join('');
const f = (s: number) => Math.round(s * FPS);

type Shot = {src: string; dur: number; from?: number; text: string; grade: string; scale?: number; shiftY?: number; pos?: string};
const SHOTS: Shot[] = [
  {src: 'p1.mp4', dur: 3.2, from: 0.6, text: 'Noël approche.', grade: 'saturate(0.9) contrast(1.08)', pos: '42% 50%'},
  {src: 'p4.mp4', dur: 2.5, from: 0.3, text: 'On vient chez vous.', grade: 'saturate(1.05) contrast(1.06)', pos: '35% 50%'},
  {src: 'p5.mp4', dur: 2.5, from: 0.2, text: 'À la main, dans le détail.', grade: 'saturate(0.92) contrast(1.06)', pos: '40% 50%'},
  {src: 'p6.mp4', dur: 3.0, text: 'Votre voiture comme neuve.', grade: 'saturate(1.05) contrast(1.06)', scale: 1.22, shiftY: 1.6, pos: '50% 50%'},
];
const OFFER = 4.0, END = 3.6;
const SHOTS_FRAMES = SHOTS.reduce((a, s) => a + f(s.dur), 0);
const TOTAL = SHOTS_FRAMES + f(OFFER) + f(END);
const VH = 1350; // hauteur de la zone vidéo (4:5)

const Words: React.FC<{text: string; size: number; delay?: number; color?: string}> = ({text, size, delay = 6, color = '#fff'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <div style={{fontFamily: 'Outfit', fontWeight: 800, fontSize: size, lineHeight: 1.04, color, letterSpacing: '-0.015em'}}>
      {text.split(' ').map((w, i) => {
        const s = spring({frame: frame - delay - i * 3, fps, config: {damping: 200}});
        return <span key={i} style={{display: 'inline-block', overflow: 'hidden', verticalAlign: 'top', marginRight: '0.24em', paddingBottom: 10}}>
          <span style={{display: 'inline-block', transform: `translateY(${(1 - s) * 108}%)`}}>{w}</span>
        </span>;
      })}
    </div>
  );
};

const Snow: React.FC<{count?: number; opacity?: number}> = ({count = 70, opacity = 1}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity}}>
      {Array.from({length: count}).map((_, i) => {
        const r = 3 + random(`r${i}`) * 7;
        const speed = 2.2 + r * 0.45 + random(`s${i}`) * 2;
        const y = ((random(`y${i}`) * 2100 + frame * speed) % 2100) - 90;
        const x = random(`x${i}`) * 1080 + Math.sin(frame / 26 + i) * 22;
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: r, height: r, borderRadius: '50%', background: '#fff', opacity: 0.35 + random(`o${i}`) * 0.5, filter: r > 7 ? 'blur(1.5px)' : undefined}} />;
      })}
    </AbsoluteFill>
  );
};

const Chip: React.FC = () => (
  <div style={{display: 'inline-block', background: RED, color: '#fff', fontFamily: 'Outfit', fontWeight: 600, fontSize: 30, letterSpacing: '0.16em', padding: '12px 26px', borderRadius: 999}}>OFFRE DE NOËL</div>
);

const Clip: React.FC<{s: Shot; dur: number}> = ({s, dur}) => {
  const frame = useCurrentFrame();
  const z = interpolate(frame, [0, dur], [1.0, 1.07]);
  const fade = interpolate(frame, [0, 6], [0, 1], {extrapolateRight: 'clamp'});
  const line = interpolate(frame, [4, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  return (
    <AbsoluteFill style={{background: NIGHT}}>
      <div style={{position: 'absolute', top: 0, left: 0, width: 1080, height: VH, overflow: 'hidden', opacity: fade}}>
        <AbsoluteFill style={{transform: `scale(${(s.scale ?? 1) * z}) translateY(${s.shiftY ?? 0}%)`, filter: s.grade}}>
          <OffthreadVideo src={staticFile(s.src)} startFrom={f(s.from ?? 0)} muted style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: s.pos ?? '50% 50%'}} />
        </AbsoluteFill>
        <AbsoluteFill style={{background: `linear-gradient(180deg, rgba(14,20,24,.35) 0%, rgba(14,20,24,0) 22%, rgba(14,20,24,0) 62%, ${NIGHT} 100%)`}} />
      </div>
      <div style={{position: 'absolute', left: 80, right: 80, top: VH - 70}}>
        <div style={{height: 5, width: 110 * line, background: GOLD, marginBottom: 30}} />
        <Words text={s.text} size={104} />
      </div>
    </AbsoluteFill>
  );
};

const Offer: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = (d: number) => spring({frame: frame - d, fps, config: {damping: 200}});
  const pop = spring({frame: frame - 6, fps, config: {damping: 13, mass: 0.7}});
  const row = (d: number): React.CSSProperties => ({opacity: a(d), transform: `translateY(${(1 - a(d)) * 40}px)`});
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 38%, #1c2a33 0%, ${NIGHT} 62%)`, alignItems: 'center', justifyContent: 'center', fontFamily: 'Outfit', color: '#fff', textAlign: 'center', padding: 80}}>
      <div style={row(2)}><Chip /></div>
      <div style={{fontSize: 400, fontWeight: 800, lineHeight: 0.95, letterSpacing: '-0.03em', marginTop: 40, transform: `scale(${0.6 + pop * 0.4})`, opacity: Math.min(1, pop * 1.4)}}>−20<span style={{fontSize: 220}}>%</span></div>
      <div style={{height: 5, width: 150 * a(18), background: GOLD, margin: '46px 0 40px'}} />
      <div style={{fontSize: 68, fontWeight: 800, lineHeight: 1.1, ...row(20)}}>sur toutes les prestations</div>
      <div style={{fontSize: 52, fontWeight: 400, color: 'rgba(255,255,255,.82)', marginTop: 18, ...row(28)}}>et sur les cartes cadeaux</div>
      <div style={{fontSize: 46, fontWeight: 600, marginTop: 70, padding: '18px 40px', border: '2px solid rgba(255,255,255,.35)', borderRadius: 999, ...row(40)}}>Jusqu’au 24 décembre</div>
    </AbsoluteFill>
  );
};

const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = (d: number) => spring({frame: frame - d, fps, config: {damping: 200}});
  const row = (d: number): React.CSSProperties => ({opacity: a(d), transform: `translateY(${(1 - a(d)) * 36}px)`});
  return (
    <AbsoluteFill style={{background: NIGHT, alignItems: 'center', justifyContent: 'center', fontFamily: 'Outfit', color: '#fff', textAlign: 'center', padding: 80}}>
      <Img src={staticFile('logo.png')} style={{width: 720, ...row(4)}} />
      <div style={{height: 4, width: 140 * a(14), background: GOLD, margin: '60px 0 54px'}} />
      <div style={{fontSize: 54, fontWeight: 400, color: 'rgba(255,255,255,.85)', lineHeight: 1.25, ...row(16)}}>Nettoyage auto à domicile<br />Essonne et Seine-et-Marne</div>
      <div style={{fontSize: 128, fontWeight: 800, marginTop: 56, letterSpacing: '-0.01em', ...row(26)}}>Dès 39 €</div>
      <div style={{fontSize: 40, fontWeight: 400, color: 'rgba(255,255,255,.6)', marginTop: 4, ...row(30)}}>au lieu de 49 €, jusqu’au 24 décembre</div>
      <div style={{fontSize: 56, fontWeight: 600, marginTop: 80, ...row(38)}}>continentaldetailing.fr</div>
      <div style={{fontSize: 56, fontWeight: 600, marginTop: 14, color: GOLD, ...row(44)}}>07 50 87 59 64</div>
    </AbsoluteFill>
  );
};

const Film: React.FC = () => {
  const frame = useCurrentFrame();
  let at = 0;
  const open = interpolate(frame, [0, 12], [1, 0], {extrapolateRight: 'clamp'});
  const chipIn = spring({frame: frame - 10, fps: FPS, config: {damping: 200}});
  return (
    <AbsoluteFill style={{background: NIGHT}}>
      <style>{fontCss}</style>
      {SHOTS.map((s, i) => {
        const d = f(s.dur);
        const el = <Sequence key={i} from={at} durationInFrames={d}><Clip s={s} dur={d} /></Sequence>;
        at += d;
        return el;
      })}
      <Sequence from={0} durationInFrames={SHOTS_FRAMES}>
        <div style={{position: 'absolute', top: 70, left: 80, opacity: chipIn, transform: `translateY(${(1 - chipIn) * -30}px)`}}><Chip /></div>
      </Sequence>
      <Sequence from={SHOTS_FRAMES} durationInFrames={f(OFFER)}><Offer /></Sequence>
      <Sequence from={SHOTS_FRAMES + f(OFFER)} durationInFrames={f(END)}><EndCard /></Sequence>
      <Snow />
      <AbsoluteFill style={{background: '#000', opacity: open}} />
    </AbsoluteFill>
  );
};

registerRoot(() => <Composition id="Noel" component={Film} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} />);

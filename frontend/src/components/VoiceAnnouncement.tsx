import { useState } from 'react';
import { Volume2, Loader2 } from 'lucide-react';
import { getVoiceAnnouncement } from '../services/api';

interface VoiceAnnouncementProps {
  alertText: string;
}

const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिंदी' },
  { code: 'ta', label: 'தமிழ்' },
  { code: 'te', label: 'తెలుగు' },
  { code: 'bn', label: 'বাংলা' },
  { code: 'mr', label: 'मराठी' },
  { code: 'gu', label: 'ગુજરાતી' },
];

const VoiceAnnouncement = ({ alertText }: VoiceAnnouncementProps) => {
  const [lang, setLang] = useState('hi');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePlay = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await getVoiceAnnouncement(alertText, lang);
      const audio = new Audio(`data:audio/wav;base64,${res.audio_base64}`);
      await audio.play();
    } catch (err) {
      console.error(err);
      setError('Could not play announcement.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center gap-2 flex-wrap">
      <select
        value={lang}
        onChange={(e) => setLang(e.target.value)}
        className="border border-indigo-200 rounded-full px-3 py-1.5 text-xs font-medium text-indigo-900 bg-white outline-none"
      >
        {LANGUAGES.map((l) => (
          <option key={l.code} value={l.code}>{l.label}</option>
        ))}
      </select>
      <button
        type="button"
        onClick={handlePlay}
        disabled={loading}
        className="flex items-center gap-1.5 bg-white/20 hover:bg-white/30 text-white text-xs font-semibold px-3 py-1.5 rounded-full transition-colors disabled:opacity-50"
      >
        {loading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Volume2 className="w-3.5 h-3.5" />}
        Listen
      </button>
      {error && <span className="text-red-200 text-xs">{error}</span>}
    </div>
  );
};

export default VoiceAnnouncement;

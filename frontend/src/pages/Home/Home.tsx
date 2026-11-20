import React, { useState, useRef, useCallback, useEffect } from 'react';
import { Film, Activity, Upload, Download, Trash2, FileSpreadsheet, CheckCircle2, XCircle, Loader2, FolderDown, ChevronDown, ChevronUp, BarChart3 } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';
import { Button } from '../../components/ui/button';
import api from '../../services/api';

// ─── Types ───────────────────────────────────────────────────
interface VideoInfo {
  id: number;
  filename: string;
  fps: number | null;
  total_frames: number | null;
  status: string;
  progress?: number;
  created_at: string;
}

interface EvalResult {
  video_id: number;
  filename: string;
  status: string;
  progress?: number;
  mean_lpips: number | null;
  var_lpips: number | null;
  max_lpips: number | null;
  error_message: string | null;
  results: { frame_a: string; frame_b: string; lpips_score: number }[];
}

// ─── Upload Zone ──────────────────────────────────────────────
function UploadZone({ onFiles, uploading, multiple = true }: { onFiles: (files: FileList) => void; uploading: boolean; multiple?: boolean }) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') setDragging(true);
    else if (e.type === 'dragleave') setDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragging(false);
    if (e.dataTransfer.files?.length) onFiles(e.dataTransfer.files);
  }, [onFiles]);

  return (
    <div
      className={`upload-zone p-8 text-center ${dragging ? 'dragging' : ''}`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onClick={() => !uploading && inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".mp4"
        multiple={multiple}
        className="hidden"
        onChange={e => e.target.files?.length && onFiles(e.target.files)}
      />
      <div className="flex flex-col items-center gap-3">
        <div className="w-16 h-16 rounded-2xl bg-[rgba(99,102,241,0.1)] flex items-center justify-center">
          <Upload className="w-7 h-7 text-indigo-400" />
        </div>
        <div>
          <p className="text-base font-medium text-foreground">
            {uploading ? 'Uploading...' : 'Drag & drop MP4 files here'}
          </p>
          <p className="text-sm text-muted-foreground mt-1">
            or click to browse • {multiple ? 'multiple files supported' : 'single file'}
          </p>
        </div>
      </div>
    </div>
  );
}

// ─── Status Badge ─────────────────────────────────────────────
function StatusBadge({ status, progress }: { status: string, progress?: number }) {
  const cls = status === 'completed' ? 'status-completed' : status === 'failed' ? 'status-failed' : 'status-processing';
  const Icon = status === 'completed' ? CheckCircle2 : status === 'failed' ? XCircle : Loader2;
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${cls}`}>
      <Icon className={`w-3 h-3 ${status === 'processing' ? 'animate-spin' : ''}`} />
      {status === 'processing' && progress !== undefined ? `${status} (${progress}%)` : status}
    </span>
  );
}

// ─── Frame Extraction Tab ─────────────────────────────────────
function FrameExtractorTab() {
  const [videos, setVideos] = useState<VideoInfo[]>([]);
  const [uploading, setUploading] = useState(false);
  const [downloadingId, setDownloadingId] = useState<number | null>(null);
  const pollRef = useRef<number | null>(null);

  const pollVideos = useCallback(async (ids: number[]) => {
    if (ids.length === 0) return;
    try {
      const results = await Promise.all(ids.map(id => api.get(`/videos/${id}`)));
      setVideos(prev => {
        const updated = [...prev];
        results.forEach(res => {
          const idx = updated.findIndex(v => v.id === res.data.id);
          if (idx >= 0) updated[idx] = res.data;
        });
        return updated;
      });
      // Continue polling for processing videos
      const stillProcessing = results.filter(r => r.data.status === 'processing').map(r => r.data.id);
      if (stillProcessing.length > 0) {
        pollRef.current = window.setTimeout(() => pollVideos(stillProcessing), 2000);
      }
    } catch (err) {
      console.error(err);
    }
  }, []);

  useEffect(() => {
    return () => { if (pollRef.current) clearTimeout(pollRef.current); };
  }, []);

  const handleFiles = async (files: FileList) => {
    setUploading(true);
    const newIds: number[] = [];
    for (const file of Array.from(files)) {
      if (!file.name.toLowerCase().endsWith('.mp4')) continue;
      try {
        const formData = new FormData();
        formData.append('file', file);
        const res = await api.post('/videos/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        setVideos(prev => [res.data, ...prev]);
        newIds.push(res.data.id);
      } catch (err) {
        console.error(`Upload failed: ${file.name}`);
      }
    }
    setUploading(false);
    if (newIds.length > 0) pollVideos(newIds);
  };

  const downloadFrames = async (videoId: number, filename: string) => {
    setDownloadingId(videoId);
    try {
      const res = await api.get(`/videos/${videoId}/download-frames`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement('a');
      a.href = url;
      a.download = `${filename.split('.')[0]}_frames.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Download failed', err);
    } finally {
      setDownloadingId(null);
    }
  };

  const deleteVideo = async (videoId: number) => {
    try {
      await api.delete(`/videos/${videoId}`);
      setVideos(prev => prev.filter(v => v.id !== videoId));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <UploadZone onFiles={handleFiles} uploading={uploading} />

      {videos.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Film className="w-5 h-5 text-indigo-400" />
            Videos ({videos.length})
          </h3>
          <div className="space-y-2">
            {videos.map((v, idx) => (
              <div key={v.id} className="video-card flex items-center justify-between gap-4 animate-slide-up" style={{ animationDelay: `${idx * 50}ms` }}>
                <div className="flex items-center gap-4 flex-1 min-w-0">
                  <div className="w-10 h-10 rounded-xl bg-[rgba(99,102,241,0.1)] flex items-center justify-center shrink-0">
                    <Film className="w-5 h-5 text-indigo-400" />
                  </div>
                  <div className="min-w-0">
                    <p className="font-medium truncate">{v.filename}</p>
                    <div className="flex gap-3 text-xs text-muted-foreground mt-0.5">
                      {v.fps && <span>{Math.round(v.fps)} FPS</span>}
                      {v.total_frames && <span>{v.total_frames} frames</span>}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <StatusBadge status={v.status} progress={v.progress} />
                  {v.status === 'completed' && (
                    <Button size="sm" variant="outline" onClick={() => downloadFrames(v.id, v.filename)} disabled={downloadingId === v.id} className="gap-1.5" title="Download frames as ZIP">
                      {downloadingId === v.id ? <Loader2 className="w-4 h-4 animate-spin" /> : <FolderDown className="w-4 h-4" />}
                      {downloadingId === v.id ? 'Downloading...' : 'Download'}
                    </Button>
                  )}
                  <Button size="sm" variant="ghost" onClick={() => deleteVideo(v.id)} className="text-muted-foreground hover:text-destructive">
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── LPIPS Evaluation Tab ─────────────────────────────────────
function LpipsEvaluatorTab() {
  const [videos, setVideos] = useState<VideoInfo[]>([]);
  const [evalResults, setEvalResults] = useState<Map<number, EvalResult>>(new Map());
  const [uploading, setUploading] = useState(false);
  const [downloadingExcel, setDownloadingExcel] = useState(false);
  const [expandedVideo, setExpandedVideo] = useState<number | null>(null);
  const pollRef = useRef<number | null>(null);
  const evalPollRef = useRef<number | null>(null);

  useEffect(() => {
    return () => {
      if (pollRef.current) clearTimeout(pollRef.current);
      if (evalPollRef.current) clearTimeout(evalPollRef.current);
    };
  }, []);

  // Poll extraction status, then auto-trigger evaluation
  const pollExtractionAndEval = useCallback(async (ids: number[]) => {
    if (ids.length === 0) return;
    try {
      const results = await Promise.all(ids.map(id => api.get(`/videos/${id}`)));
      const stillProcessing: number[] = [];
      const readyForEval: number[] = [];

      results.forEach(res => {
        if (res.data.status === 'processing') stillProcessing.push(res.data.id);
        if (res.data.status === 'completed') readyForEval.push(res.data.id);
      });

      setVideos(prev => {
        const updated = [...prev];
        results.forEach(res => {
          const idx = updated.findIndex(v => v.id === res.data.id);
          if (idx >= 0) updated[idx] = res.data;
        });
        return updated;
      });

      // Auto-trigger LPIPS for completed extractions
      for (const vid of readyForEval) {
        if (!evalResults.has(vid)) {
          try {
            await api.post(`/evaluations/trigger/${vid}`);
            setEvalResults(prev => {
              const m = new Map(prev);
              m.set(vid, { video_id: vid, filename: '', status: 'processing', progress: 0, mean_lpips: null, var_lpips: null, max_lpips: null, error_message: null, results: [] });
              return m;
            });
          } catch (e) { console.error(e); }
        }
      }

      if (stillProcessing.length > 0) {
        pollRef.current = window.setTimeout(() => pollExtractionAndEval(stillProcessing), 2000);
      }

      // Start polling evaluations
      const evalIds = [...readyForEval, ...Array.from(evalResults.keys()).filter(k => evalResults.get(k)?.status === 'processing')];
      if (evalIds.length > 0) pollEvaluations(evalIds);
    } catch (err) { console.error(err); }
  }, [evalResults]);

  const pollEvaluations = useCallback(async (videoIds: number[]) => {
    const stillProcessing: number[] = [];
    for (const vid of videoIds) {
      try {
        const res = await api.get(`/evaluations/${vid}`);
        const video = videos.find(v => v.id === vid);
        setEvalResults(prev => {
          const m = new Map(prev);
          m.set(vid, {
            video_id: vid,
            filename: video?.filename || `Video ${vid}`,
            status: res.data.status,
            progress: res.data.progress,
            mean_lpips: res.data.mean_lpips,
            var_lpips: res.data.var_lpips,
            max_lpips: res.data.max_lpips,
            error_message: res.data.error_message,
            results: res.data.results || []
          });
          return m;
        });
        if (res.data.status === 'processing' || res.data.status === 'pending') {
          stillProcessing.push(vid);
        }
      } catch (e) { /* not ready yet */ stillProcessing.push(vid); }
    }
    if (stillProcessing.length > 0) {
      evalPollRef.current = window.setTimeout(() => pollEvaluations(stillProcessing), 3000);
    }
  }, [videos]);

  const handleFiles = async (files: FileList) => {
    setUploading(true);
    const newIds: number[] = [];
    for (const file of Array.from(files)) {
      if (!file.name.toLowerCase().endsWith('.mp4')) continue;
      try {
        const formData = new FormData();
        formData.append('file', file);
        const res = await api.post('/videos/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        setVideos(prev => [res.data, ...prev]);
        newIds.push(res.data.id);
      } catch (err) {
        console.error(`Upload failed: ${file.name}`);
      }
    }
    setUploading(false);
    if (newIds.length > 0) pollExtractionAndEval(newIds);
  };

  const downloadExcel = async () => {
    const completedIds = Array.from(evalResults.entries())
      .filter(([_, r]) => r.status === 'completed')
      .map(([id]) => id);
    if (completedIds.length === 0) return;
    
    setDownloadingExcel(true);
    try {
      const res = await api.get(`/evaluations/export/excel?video_ids=${completedIds.join(',')}`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement('a');
      a.href = url;
      a.download = `lpips_evaluation_results.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Download failed', err);
    } finally {
      setDownloadingExcel(false);
    }
  };

  const completedEvals = Array.from(evalResults.values()).filter(r => r.status === 'completed');

  return (
    <div className="space-y-6 animate-fade-in">
      <UploadZone onFiles={handleFiles} uploading={uploading} />

      {videos.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <Activity className="w-5 h-5 text-purple-400" />
              Videos & Evaluation ({videos.length})
            </h3>
            {completedEvals.length > 0 && (
              <Button onClick={downloadExcel} variant="outline" disabled={downloadingExcel} className="gap-2">
                {downloadingExcel ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileSpreadsheet className="w-4 h-4" />}
                {downloadingExcel ? 'Downloading...' : 'Download Excel'}
              </Button>
            )}
          </div>

          {/* Summary Stats */}
          {completedEvals.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="stat-card">
                <p className="text-xs text-muted-foreground font-medium uppercase tracking-wider">Avg Mean LPIPS</p>
                <p className="text-2xl font-bold mt-1 gradient-text">
                  {(completedEvals.reduce((s, e) => s + (e.mean_lpips || 0), 0) / completedEvals.length).toFixed(5)}
                </p>
                <p className="text-xs text-muted-foreground mt-1">Across {completedEvals.length} video(s)</p>
              </div>
              <div className="stat-card">
                <p className="text-xs text-muted-foreground font-medium uppercase tracking-wider">Avg Variance (Flicker)</p>
                <p className="text-2xl font-bold mt-1 gradient-text">
                  {(completedEvals.reduce((s, e) => s + (e.var_lpips || 0), 0) / completedEvals.length).toFixed(6)}
                </p>
                <p className="text-xs text-muted-foreground mt-1">Lower = more stable</p>
              </div>
              <div className="stat-card">
                <p className="text-xs text-muted-foreground font-medium uppercase tracking-wider">Avg Max LPIPS (Morphing)</p>
                <p className="text-2xl font-bold mt-1 gradient-text">
                  {(completedEvals.reduce((s, e) => s + (e.max_lpips || 0), 0) / completedEvals.length).toFixed(5)}
                </p>
                <p className="text-xs text-muted-foreground mt-1">Peak distortion</p>
              </div>
            </div>
          )}

          {/* Video list */}
          <div className="space-y-2">
            {videos.map((v, idx) => {
              const evalR = evalResults.get(v.id);
              const isExpanded = expandedVideo === v.id;
              const chartData = evalR?.results?.map((r, i) => ({ name: `F${i}`, score: r.lpips_score })) || [];

              return (
                <div key={v.id} className="animate-slide-up" style={{ animationDelay: `${idx * 50}ms` }}>
                  <div
                    className="video-card cursor-pointer"
                    onClick={() => evalR?.status === 'completed' && setExpandedVideo(isExpanded ? null : v.id)}
                  >
                    <div className="flex items-center justify-between gap-4">
                      <div className="flex items-center gap-4 flex-1 min-w-0">
                        <div className="w-10 h-10 rounded-xl bg-[rgba(168,85,247,0.1)] flex items-center justify-center shrink-0">
                          <Film className="w-5 h-5 text-purple-400" />
                        </div>
                        <div className="min-w-0">
                          <p className="font-medium truncate">{v.filename}</p>
                          <div className="flex gap-3 text-xs text-muted-foreground mt-0.5">
                            {v.fps && <span>{Math.round(v.fps)} FPS</span>}
                            {v.total_frames && <span>{v.total_frames} frames</span>}
                            {evalR?.status === 'completed' && (
                              <>
                                <span className="text-indigo-400">Mean: {evalR.mean_lpips?.toFixed(5)}</span>
                                <span className="text-purple-400">Var: {evalR.var_lpips?.toFixed(6)}</span>
                                <span className="text-pink-400">Max: {evalR.max_lpips?.toFixed(5)}</span>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        {evalR ? <StatusBadge status={evalR.status} progress={evalR.progress} /> : <StatusBadge status={v.status === 'completed' ? 'processing' : v.status} progress={v.status === 'processing' ? v.progress : undefined} />}
                        {evalR?.status === 'completed' && (
                          isExpanded ? <ChevronUp className="w-4 h-4 text-muted-foreground" /> : <ChevronDown className="w-4 h-4 text-muted-foreground" />
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Expanded chart */}
                  {isExpanded && evalR?.status === 'completed' && chartData.length > 0 && (
                    <div className="mt-2 glass rounded-xl p-6 animate-fade-in">
                      <div className="flex items-center gap-2 mb-4">
                        <BarChart3 className="w-4 h-4 text-indigo-400" />
                        <h4 className="text-sm font-semibold">LPIPS Timeline — {v.filename}</h4>
                      </div>
                      <div className="h-[280px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                          <AreaChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 0 }}>
                            <defs>
                              <linearGradient id={`grad-${v.id}`} x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#818cf8" stopOpacity={0.6} />
                                <stop offset="95%" stopColor="#818cf8" stopOpacity={0} />
                              </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.08)" vertical={false} />
                            <XAxis dataKey="name" stroke="#555" tick={{ fontSize: 11 }} minTickGap={20} />
                            <YAxis stroke="#555" tick={{ fontSize: 11 }} />
                            <RechartsTooltip
                              contentStyle={{ backgroundColor: '#0f0f1a', borderColor: 'rgba(99,102,241,0.2)', borderRadius: '10px', fontSize: '13px' }}
                              itemStyle={{ color: '#c4b5fd' }}
                            />
                            <Area type="monotone" dataKey="score" stroke="#818cf8" strokeWidth={2} fillOpacity={1} fill={`url(#grad-${v.id})`} />
                          </AreaChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Main Home Page ───────────────────────────────────────────
export default function Home() {
  const [activeTab, setActiveTab] = useState<'extract' | 'evaluate'>('extract');

  return (
    <div className="min-h-screen bg-grid-pattern">
      {/* Background gradient orbs */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-indigo-500/[0.04] rounded-full blur-3xl" />
        <div className="absolute top-1/2 -left-40 w-96 h-96 bg-purple-500/[0.04] rounded-full blur-3xl" />
        <div className="absolute -bottom-40 right-1/3 w-96 h-96 bg-pink-500/[0.03] rounded-full blur-3xl" />
      </div>

      <div className="relative container mx-auto max-w-5xl px-6 py-10">
        {/* Header */}
        <header className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[rgba(99,102,241,0.08)] border border-[rgba(99,102,241,0.15)] text-xs font-medium text-indigo-300 mb-4">
            <Activity className="w-3.5 h-3.5" />
            LPIPS Video Evaluation Tool
          </div>
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
            <span className="gradient-text">Video Analysis</span>
            <span className="text-foreground"> Platform</span>
          </h1>
          <p className="text-muted-foreground mt-3 max-w-xl mx-auto">
            Extract video frames and evaluate temporal stability using LPIPS perceptual distance metric.
          </p>
        </header>

        {/* Tab Navigation */}
        <div className="flex justify-center gap-3 mb-8">
          <button
            className={`tab-button flex items-center gap-2 ${activeTab === 'extract' ? 'active' : ''}`}
            onClick={() => setActiveTab('extract')}
          >
            <Film className="w-4 h-4" />
            Ekstrak Frame
          </button>
          <button
            className={`tab-button flex items-center gap-2 ${activeTab === 'evaluate' ? 'active' : ''}`}
            onClick={() => setActiveTab('evaluate')}
          >
            <Activity className="w-4 h-4" />
            Evaluasi LPIPS
          </button>
        </div>

        {/* Tab Content */}
        <div className="glass-strong rounded-2xl p-6 md:p-8 animate-pulse-glow">
          {activeTab === 'extract' ? <FrameExtractorTab /> : <LpipsEvaluatorTab />}
        </div>

        {/* Footer */}
        <footer className="text-center mt-10 text-xs text-muted-foreground">
          LPIPS Evaluation Platform • Temporal Stability Analysis
        </footer>
      </div>
    </div>
  );
}

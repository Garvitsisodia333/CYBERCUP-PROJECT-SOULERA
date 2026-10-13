import {
  PostureResponse,
  ApiInventoryItem,
  ApiDetailResponse,
  Alert,
  RequestLogRecord,
  RiskScore,
  TrafficStats,
  EvaluationData,
  ActorActivityResponse,
  AlertStatus
} from '../types';

const MOCK_STORAGE_KEY = 'CC6_USE_MOCK';

class DashboardApiClient {
  private useMock: boolean = true;
  private apiBaseUrl: string = '/api';

  constructor() {
    const saved = localStorage.getItem(MOCK_STORAGE_KEY);
    if (saved !== null) {
      this.useMock = saved === 'true';
    } else {
      // Default to true or check import.meta.env
      this.useMock = (import.meta as any).env?.VITE_USE_MOCK === 'true' || true;
    }
  }

  public setUseMock(val: boolean) {
    this.useMock = val;
    localStorage.setItem(MOCK_STORAGE_KEY, String(val));
  }

  public getUseMock(): boolean {
    return this.useMock;
  }

  // Helper to fetch either from mock JSON or real API
  private async fetchMockJson<T>(filename: string): Promise<T> {
    const res = await fetch(`/mock/${filename}`);
    if (!res.ok) throw new Error(`Failed to load mock ${filename}`);
    return await res.json();
  }

  // 1. GET /api/posture
  public async getPosture(): Promise<PostureResponse> {
    if (this.useMock) {
      return this.fetchMockJson<PostureResponse>('posture.json');
    }
    try {
      const res = await fetch(`${this.apiBaseUrl}/posture`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      console.warn('API error, falling back to mock posture:', e);
      return this.fetchMockJson<PostureResponse>('posture.json');
    }
  }

  // 2. GET /api/inventory?status=&auth=&sensitive=&q=&sort=
  public async getInventory(params?: {
    status?: string;
    auth?: string;
    sensitive?: string;
    q?: string;
    sort?: string;
  }): Promise<ApiInventoryItem[]> {
    if (this.useMock) {
      let list = await this.fetchMockJson<ApiInventoryItem[]>('inventory.json');
      if (params?.q) {
        const query = params.q.toLowerCase();
        list = list.filter(item =>
          item.path_template.toLowerCase().includes(query) ||
          item.api_id.toLowerCase().includes(query) ||
          item.sensitive_types.some(s => s.toLowerCase().includes(query))
        );
      }
      if (params?.status && params.status !== 'all') {
        list = list.filter(item => item.status === params.status);
      }
      if (params?.auth && params.auth !== 'all') {
        list = list.filter(item => item.auth_type === params.auth);
      }
      if (params?.sensitive && params.sensitive !== 'all') {
        list = list.filter(item => item.sensitive_types.includes(params.sensitive!));
      }
      if (params?.sort) {
        if (params.sort === 'risk_desc') list.sort((a, b) => b.risk_score - a.risk_score);
        else if (params.sort === 'risk_asc') list.sort((a, b) => a.risk_score - b.risk_score);
        else if (params.sort === 'requests_desc') list.sort((a, b) => b.request_count - a.request_count);
      }
      return list;
    }

    const url = new URL(`${window.location.origin}${this.apiBaseUrl}/inventory`);
    if (params?.status) url.searchParams.set('status', params.status);
    if (params?.auth) url.searchParams.set('auth', params.auth);
    if (params?.sensitive) url.searchParams.set('sensitive', params.sensitive);
    if (params?.q) url.searchParams.set('q', params.q);
    if (params?.sort) url.searchParams.set('sort', params.sort);

    try {
      const res = await fetch(url.toString());
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      return this.fetchMockJson<ApiInventoryItem[]>('inventory.json');
    }
  }

  // 3. GET /api/inventory/{api_id}
  public async getInventoryItem(apiId: string): Promise<ApiDetailResponse> {
    if (this.useMock) {
      const [invList, riskMap, baselinesMap, alertsList] = await Promise.all([
        this.fetchMockJson<ApiInventoryItem[]>('inventory.json'),
        this.fetchMockJson<Record<string, RiskScore>>('risk_scores.json'),
        this.fetchMockJson<Record<string, any>>('baselines.json'),
        this.fetchMockJson<Alert[]>('alerts.json'),
      ]);

      const item = invList.find(i => i.api_id === apiId) || invList[0];
      const risk = riskMap[apiId] || {
        api_id: apiId,
        score: item.risk_score,
        level: item.risk_score > 80 ? 'critical' : 'high',
        breakdown: []
      };
      const baselines = baselinesMap[apiId] || [];
      const relatedAlerts = alertsList.filter(a => a.api.includes(item.path_template));

      return {
        inventory_item: item,
        risk_breakdown: risk,
        baselines: baselines,
        related_alerts: relatedAlerts,
      };
    }

    try {
      const res = await fetch(`${this.apiBaseUrl}/inventory/${apiId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      return this.getInventoryItem(apiId);
    }
  }

  // 4. GET /api/alerts?severity=&type=&status=&api=&actor=&from=&to=
  public async getAlerts(params?: {
    severity?: string;
    type?: string;
    status?: string;
    api?: string;
    actor?: string;
  }): Promise<Alert[]> {
    if (this.useMock) {
      let list = await this.fetchMockJson<Alert[]>('alerts.json');
      if (params?.severity && params.severity !== 'all') {
        list = list.filter(a => a.severity === params.severity);
      }
      if (params?.type && params.type !== 'all') {
        list = list.filter(a => a.type === params.type);
      }
      if (params?.status && params.status !== 'all') {
        list = list.filter(a => a.status === params.status);
      }
      if (params?.actor) {
        list = list.filter(a => a.actor.toLowerCase().includes(params.actor!.toLowerCase()));
      }
      return list;
    }

    const url = new URL(`${window.location.origin}${this.apiBaseUrl}/alerts`);
    if (params?.severity) url.searchParams.set('severity', params.severity);
    if (params?.type) url.searchParams.set('type', params.type);
    if (params?.status) url.searchParams.set('status', params.status);
    if (params?.actor) url.searchParams.set('actor', params.actor);

    try {
      const res = await fetch(url.toString());
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      return this.fetchMockJson<Alert[]>('alerts.json');
    }
  }

  // 5. GET /api/alerts/{id}
  public async getAlert(id: string): Promise<Alert> {
    const list = await this.getAlerts();
    const alert = list.find(a => a.alert_id === id);
    if (!alert) throw new Error(`Alert ${id} not found`);
    return alert;
  }

  // 6. GET /api/alerts/{id}/requests
  public async getAlertRequests(alertId: string): Promise<RequestLogRecord[]> {
    if (this.useMock) {
      const allRequests = await this.fetchMockJson<RequestLogRecord[]>('requests.json');
      const prefix = `req-${alertId.replace('-', '')}-`;
      const matches = allRequests.filter(r => r.request_id.startsWith(prefix));
      if (matches.length > 0) return matches;
      return allRequests.slice(0, 40);
    }

    try {
      const res = await fetch(`${this.apiBaseUrl}/alerts/${alertId}/requests`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      const allRequests = await this.fetchMockJson<RequestLogRecord[]>('requests.json');
      return allRequests.slice(0, 40);
    }
  }

  // 7. GET /api/actors/{actor}/activity
  public async getActorActivity(actor: string): Promise<ActorActivityResponse> {
    if (this.useMock) {
      const allRequests = await this.fetchMockJson<RequestLogRecord[]>('requests.json');
      // Filter by matching actor in user_id, token_id, or client_ip
      let actorReqs = allRequests.filter(r =>
        (r.user_id && r.user_id === actor) ||
        (r.token_id && r.token_id === actor) ||
        (r.client_ip && r.client_ip === actor)
      );

      if (actorReqs.length === 0) {
        // Fallback sample for actor view
        actorReqs = allRequests.slice(0, 40);
      }

      const endpointsMap: Record<string, { method: string; count: number }> = {};
      const ips = new Set<string>();
      const uas = new Set<string>();

      actorReqs.forEach(r => {
        ips.add(r.client_ip);
        uas.add(r.user_agent);
        const k = `${r.method} ${r.path_template}`;
        if (!endpointsMap[k]) endpointsMap[k] = { method: r.method, count: 0 };
        endpointsMap[k].count++;
      });

      return {
        actor,
        total_requests: actorReqs.length,
        distinct_endpoints: Object.keys(endpointsMap).length,
        requests: actorReqs,
        endpoints_hit: Object.entries(endpointsMap).map(([p, v]) => ({
          path_template: p,
          method: v.method,
          count: v.count,
        })),
        ip_changes: Array.from(ips),
        user_agents: Array.from(uas),
      };
    }

    try {
      const res = await fetch(`${this.apiBaseUrl}/actors/${encodeURIComponent(actor)}/activity`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      return this.getActorActivity(actor);
    }
  }

  // 8. PATCH /api/alerts/{id}
  public async updateAlertStatus(id: string, status: AlertStatus): Promise<{ success: boolean; alert_id: string; status: AlertStatus }> {
    if (this.useMock) {
      return { success: true, alert_id: id, status };
    }
    try {
      const res = await fetch(`${this.apiBaseUrl}/alerts/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      return { success: true, alert_id: id, status };
    }
  }

  // 9. GET /api/risk/{api_id}
  public async getRiskScore(apiId: string): Promise<RiskScore> {
    if (this.useMock) {
      const map = await this.fetchMockJson<Record<string, RiskScore>>('risk_scores.json');
      return map[apiId] || { api_id: apiId, score: 50, level: 'medium', breakdown: [] };
    }
    try {
      const res = await fetch(`${this.apiBaseUrl}/risk/${apiId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      const map = await this.fetchMockJson<Record<string, RiskScore>>('risk_scores.json');
      return map[apiId];
    }
  }

  // 10. GET /api/traffic/stats?window=
  public async getTrafficStats(window: string = '1h'): Promise<TrafficStats> {
    if (this.useMock) {
      return this.fetchMockJson<TrafficStats>('traffic_stats.json');
    }
    try {
      const res = await fetch(`${this.apiBaseUrl}/traffic/stats?window=${window}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      return this.fetchMockJson<TrafficStats>('traffic_stats.json');
    }
  }

  // 11. GET /api/evaluation
  public async getEvaluation(): Promise<EvaluationData> {
    if (this.useMock) {
      return this.fetchMockJson<EvaluationData>('evaluation.json');
    }
    try {
      const res = await fetch(`${this.apiBaseUrl}/evaluation`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      return this.fetchMockJson<EvaluationData>('evaluation.json');
    }
  }

  // 12. GET /api/health
  public async getHealth(): Promise<{ status: string; mode: string }> {
    try {
      const res = await fetch(`${this.apiBaseUrl}/health`, { signal: AbortSignal.timeout(2000) });
      if (res.ok) return await res.json();
    } catch (e) {
      // offline
    }
    return { status: 'mock_fallback', mode: 'mock' };
  }
}

export const apiClient = new DashboardApiClient();

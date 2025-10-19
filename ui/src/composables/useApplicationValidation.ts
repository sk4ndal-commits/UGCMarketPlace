export function parseParametersJson(input: string) {
  if (!input || !input.trim()) return { ok: true, value: {} };
  try {
    const parsed = JSON.parse(input);
    return { ok: true, value: parsed };
  } catch (err: any) {
    return { ok: false, error: 'Invalid JSON format' };
  }
}

export function normalizeGitIntegration(enable: boolean, git: any) {
  if (!enable) return {};
  if (!git?.repository_url) return {};
  return {
    repository_url: git.repository_url,
    ...(git.branch ? { branch: git.branch } : {}),
  };
}

export function normalizeOidcIntegration(enable: boolean, oidc: any) {
  if (!enable) return {};
  if (!oidc?.provider || !oidc?.client_id) return {};
  return {
    provider: oidc.provider,
    client_id: oidc.client_id,
  };
}

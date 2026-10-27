/**
 * Normalizes HeadersInit to a plain Record<string, string> for manipulation.
 * Handles Headers objects, arrays of tuples, and plain objects.
 */
export function normalizeHeaders(headers) {
    if (!headers)
        return {};
    if (headers instanceof Headers) {
        return Object.fromEntries(headers.entries());
    }
    if (Array.isArray(headers)) {
        return Object.fromEntries(headers);
    }
    return { ...headers };
}
/**
 * Creates a fetch function that includes base RequestInit options.
 * This ensures requests inherit settings like credentials, mode, headers, etc. from the base init.
 *
 * @param baseFetch - The base fetch function to wrap (defaults to global fetch)
 * @param baseInit - The base RequestInit to merge with each request
 * @returns A wrapped fetch function that merges base options with call-specific options
 */
export function createFetchWithInit(baseFetch = fetch, baseInit) {
    if (!baseInit) {
        return baseFetch;
    }
    // Return a wrapped fetch that merges base RequestInit with call-specific init
    return async (url, init) => {
        const mergedInit = {
            ...baseInit,
            ...init,
            // Headers need special handling - merge instead of replace
            headers: init?.headers ? { ...normalizeHeaders(baseInit.headers), ...normalizeHeaders(init.headers) } : baseInit.headers
        };
        return baseFetch(url, mergedInit);
    };
}
const MAX_REDIRECTS = 5;
const REDIRECT_STATUSES = [301, 302, 303, 307, 308];
/** @internal Whether `to` has the scheme, host and port of `from`, or is its https form with both on default ports. */
export function isWithinOrigin(from, to) {
    if (from.protocol === to.protocol && from.hostname === to.hostname && from.port === to.port) {
        return true;
    }
    return from.hostname === to.hostname && from.protocol === 'http:' && from.port === '' && to.protocol === 'https:' && to.port === '';
}
function redirectTarget(response, requestUrl) {
    const location = REDIRECT_STATUSES.includes(response.status) ? response.headers.get('location') : null;
    try {
        return location ? new URL(location, requestUrl) : undefined;
    }
    catch {
        return undefined;
    }
}
/** @internal Follows the redirect in `response` while it stays within the origin of `url`; undefined when `response` is to be used as is. */
export function followWithinOrigin(baseFetch, url, init, response, followed = 0) {
    const target = redirectTarget(response, url);
    // 301, 302 and 303 turn a request with a body into a GET, so only 307 and 308 are followed for those.
    const keepsMethod = response.status === 307 || response.status === 308 || (init?.method ?? 'GET').toUpperCase() === 'GET';
    if (!target || followed === MAX_REDIRECTS || !keepsMethod) {
        return undefined;
    }
    const from = new URL(url);
    const addsUserinfo = (target.username || target.password) && (target.username !== from.username || target.password !== from.password);
    if (addsUserinfo || !isWithinOrigin(from, target)) {
        return undefined;
    }
    return Promise.resolve(response.body?.cancel())
        .then(() => baseFetch(target, { ...init, redirect: 'manual' }))
        .then(next => followWithinOrigin(baseFetch, target, init, next, followed + 1) ?? next);
}
const followingFetches = new WeakSet();
/** @internal Wraps a fetch for `redirectPolicy: 'follow'`: `fetchWithinOrigin` returns the result as it is, so redirects are left to the fetch. */
export function fetchLeavingRedirects(baseFetch) {
    const following = (url, init) => (baseFetch ?? fetch)(url, init);
    followingFetches.add(following);
    return following;
}
/** @internal Wraps a fetch so it follows a redirect only within the request's origin; any other redirect response is returned as is. */
export function fetchWithinOrigin(baseFetch = fetch) {
    if (followingFetches.has(baseFetch)) {
        return baseFetch;
    }
    return (url, init) => {
        if (init?.redirect === 'error' || init?.redirect === 'manual') {
            return baseFetch(url, init);
        }
        // Browsers answer a manual redirect with an opaque response: it is returned and nothing is followed.
        return Promise.resolve(baseFetch(url, { ...init, redirect: 'manual' })).then(response => followWithinOrigin(baseFetch, url, init, response) ?? response);
    };
}
/** @internal Describes a redirect that `fetchWithinOrigin` returned unfollowed, naming its target without userinfo, query or fragment. */
export function unfollowedRedirect(response, requestUrl) {
    if (response.type === 'opaqueredirect') {
        return 'Redirect not followed: this runtime does not expose the redirect target';
    }
    const from = response.url || requestUrl;
    const target = redirectTarget(response, from);
    if (!target) {
        return undefined;
    }
    target.username = target.password = target.search = target.hash = '';
    if (target.protocol === 'http:' && new URL(from).protocol === 'https:') {
        target.protocol = 'https:';
        return `Redirect to plain http not followed; try ${target.href} instead`;
    }
    return `Redirect to ${target.href} not followed`;
}
//# sourceMappingURL=transport.js.map
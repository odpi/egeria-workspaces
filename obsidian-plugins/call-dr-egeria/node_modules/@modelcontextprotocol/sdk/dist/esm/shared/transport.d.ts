import { JSONRPCMessage, MessageExtraInfo, RequestId } from '../types.js';
export type FetchLike = (url: string | URL, init?: RequestInit) => Promise<Response>;
/**
 * Normalizes HeadersInit to a plain Record<string, string> for manipulation.
 * Handles Headers objects, arrays of tuples, and plain objects.
 */
export declare function normalizeHeaders(headers: HeadersInit | undefined): Record<string, string>;
/**
 * Creates a fetch function that includes base RequestInit options.
 * This ensures requests inherit settings like credentials, mode, headers, etc. from the base init.
 *
 * @param baseFetch - The base fetch function to wrap (defaults to global fetch)
 * @param baseInit - The base RequestInit to merge with each request
 * @returns A wrapped fetch function that merges base options with call-specific options
 */
export declare function createFetchWithInit(baseFetch?: FetchLike, baseInit?: RequestInit): FetchLike;
/** @internal Whether `to` has the scheme, host and port of `from`, or is its https form with both on default ports. */
export declare function isWithinOrigin(from: URL, to: URL): boolean;
/** @internal Follows the redirect in `response` while it stays within the origin of `url`; undefined when `response` is to be used as is. */
export declare function followWithinOrigin(baseFetch: FetchLike, url: string | URL, init: RequestInit | undefined, response: Response, followed?: number): Promise<Response> | undefined;
/** @internal Wraps a fetch for `redirectPolicy: 'follow'`: `fetchWithinOrigin` returns the result as it is, so redirects are left to the fetch. */
export declare function fetchLeavingRedirects(baseFetch?: FetchLike): FetchLike;
/** @internal Wraps a fetch so it follows a redirect only within the request's origin; any other redirect response is returned as is. */
export declare function fetchWithinOrigin(baseFetch?: FetchLike): FetchLike;
/** @internal Describes a redirect that `fetchWithinOrigin` returned unfollowed, naming its target without userinfo, query or fragment. */
export declare function unfollowedRedirect(response: Response, requestUrl: string | URL): string | undefined;
/**
 * Options for sending a JSON-RPC message.
 */
export type TransportSendOptions = {
    /**
     * If present, `relatedRequestId` is used to indicate to the transport which incoming request to associate this outgoing message with.
     */
    relatedRequestId?: RequestId | undefined;
    /**
     * The resumption token used to continue long-running requests that were interrupted.
     *
     * This allows clients to reconnect and continue from where they left off, if supported by the transport.
     */
    resumptionToken?: string | undefined;
    /**
     * A callback that is invoked when the resumption token changes, if supported by the transport.
     *
     * This allows clients to persist the latest token for potential reconnection.
     */
    onresumptiontoken?: ((token: string) => void) | undefined;
};
/**
 * Describes the minimal contract for an MCP transport that a client or server can communicate over.
 */
export interface Transport {
    /**
     * Starts processing messages on the transport, including any connection steps that might need to be taken.
     *
     * This method should only be called after callbacks are installed, or else messages may be lost.
     *
     * NOTE: This method should not be called explicitly when using Client, Server, or Protocol classes, as they will implicitly call start().
     */
    start(): Promise<void>;
    /**
     * Sends a JSON-RPC message (request or response).
     *
     * If present, `relatedRequestId` is used to indicate to the transport which incoming request to associate this outgoing message with.
     */
    send(message: JSONRPCMessage, options?: TransportSendOptions): Promise<void>;
    /**
     * Closes the connection.
     */
    close(): Promise<void>;
    /**
     * Callback for when the connection is closed for any reason.
     *
     * This should be invoked when close() is called as well.
     */
    onclose?: (() => void) | undefined;
    /**
     * Callback for when an error occurs.
     *
     * Note that errors are not necessarily fatal; they are used for reporting any kind of exceptional condition out of band.
     */
    onerror?: ((error: Error) => void) | undefined;
    /**
     * Callback for when a message (request or response) is received over the connection.
     *
     * Includes the requestInfo and authInfo if the transport is authenticated.
     *
     * The requestInfo can be used to get the original request information (headers, etc.)
     */
    onmessage?: (<T extends JSONRPCMessage>(message: T, extra?: MessageExtraInfo) => void) | undefined;
    /**
     * The session ID generated for this connection.
     */
    sessionId?: string | undefined;
    /**
     * Sets the protocol version used for the connection (called when the initialize response is received).
     */
    setProtocolVersion?: ((version: string) => void) | undefined;
}
//# sourceMappingURL=transport.d.ts.map
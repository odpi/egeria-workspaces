import { RequestHandler } from 'express';
import { OAuthTokenVerifier } from '../provider.js';
import { AuthInfo } from '../types.js';
export type BearerAuthMiddlewareOptions = {
    /**
     * A provider used to verify tokens.
     */
    verifier: OAuthTokenVerifier;
    /**
     * Optional scopes that the token must have.
     */
    requiredScopes?: string[];
    /**
     * Optional resource metadata URL to include in WWW-Authenticate header.
     */
    resourceMetadataUrl?: string;
    /**
     * Accept only tokens issued for this resource (the token's audience): the value the authorization server puts
     * into tokens meant for this server, usually the server's URL.
     * When set, a token is accepted only if the verifier reports that value in `AuthInfo.resource`
     * (compared as strings, ignoring a fragment and one trailing slash); any other token is refused with `401 invalid_token`.
     * When unset, `AuthInfo.resource` is not compared with anything.
     */
    expectedResource?: URL;
};
declare module 'express-serve-static-core' {
    interface Request {
        /**
         * Information about the validated access token, if the `requireBearerAuth` middleware was used.
         */
        auth?: AuthInfo;
    }
}
/**
 * Middleware that requires a valid Bearer token in the Authorization header.
 *
 * This will validate the token with the auth provider and add the resulting auth info to the request object.
 *
 * If resourceMetadataUrl is provided, it will be included in the WWW-Authenticate header
 * for 401 responses as per the OAuth 2.0 Protected Resource Metadata spec.
 */
export declare function requireBearerAuth({ verifier, requiredScopes, resourceMetadataUrl, expectedResource }: BearerAuthMiddlewareOptions): RequestHandler;
//# sourceMappingURL=bearerAuth.d.ts.map
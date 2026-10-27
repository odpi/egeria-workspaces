import { HtmlEscapedString } from "../utils/html.js";
import { PropsWithChildren } from "./index.js";
import { Child, FC } from "./index.js";
//#region src/jsx/components.d.ts
export declare const childrenToString: (children: Child[]) => Promise<HtmlEscapedString[]>;
export type ErrorHandler = (error: Error) => void;
export type FallbackRender = (error: Error) => Child;
/**
 * @experimental
 * `ErrorBoundary` is an experimental feature.
 * The API might be changed.
 */
export declare const ErrorBoundary: FC<PropsWithChildren<{
  fallback?: Child;
  fallbackRender?: FallbackRender;
  onError?: ErrorHandler;
}>>;
//#endregion
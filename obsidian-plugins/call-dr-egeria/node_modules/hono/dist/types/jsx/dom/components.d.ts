import { ErrorHandler, FallbackRender } from "../components.js";
import { PropsWithChildren } from "../index.js";
import { Child, FC } from "../index.js";
//#region src/jsx/dom/components.d.ts
export declare const ErrorBoundary: FC<PropsWithChildren<{
  fallback?: Child;
  fallbackRender?: FallbackRender;
  onError?: ErrorHandler;
}>>;
export declare const Suspense: FC<PropsWithChildren<{
  fallback: any;
}>>;
//#endregion
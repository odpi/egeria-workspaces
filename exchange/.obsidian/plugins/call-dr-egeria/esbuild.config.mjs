// esbuild.config.mjs
import esbuild from "esbuild";

const isProd = process.argv[2] === "production";

const shared = {
    entryPoints: ["main.ts"],
    bundle: true,
    outfile: "main.js",
    format: "cjs",             // Obsidian expects CommonJS
    platform: "browser",
    target: ["es2020"],
    sourcemap: isProd ? false : "inline",
    minify: isProd,
    external: [
        // Obsidian runtime provides these
        "obsidian",
        "electron",
        "@codemirror/*",
        "codemirror"
    ],
    logLevel: "info",
    define: {
        "process.env.NODE_ENV": JSON.stringify(isProd ? "production" : "development")
    }
};

if (isProd) {
    await esbuild.build(shared);
    console.log("Built production bundle to main.js");
} else {
    const ctx = await esbuild.context(shared);
    await ctx.watch();
    console.log("Watching for changes... (Ctrl+C to exit)");
}
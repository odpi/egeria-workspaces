import { App, Modal, Notice, Plugin, PluginSettingTab, Setting, normalizePath, requestUrl } from "obsidian";

type DrEgeriaDirective = "process" | "validate" | "display";

interface DrEgeriaConfigBlock {
    [key: string]: string | number | boolean | null;
}

interface DrEgeriaProfile {
    id: string;
    name: string;
    apiUrl: string;
    environmentKey: string;
    userProfileKey: string;
    environment: DrEgeriaConfigBlock;
    userProfile: DrEgeriaConfigBlock;
    outputFolder: string;
    inputFolder?: string;
}

interface SendNoteSettings {
    activeProfileId: string;
    directive: DrEgeriaDirective;
    userId: string;
    userPass: string;
    profiles: DrEgeriaProfile[];
}

interface DrEgeriaProcessResponse {
    status: "success" | "error";
    message: string;
    input_file?: string;
    output_folder?: string;
    output_file?: string | null;
    output_path?: string | null;
    console_output?: string;
    environment_key?: string;
    user_profile_key?: string;
}

const DEFAULT_PROFILE_ID = "quickstart-local";

const DEFAULT_SETTINGS: SendNoteSettings = {
    activeProfileId: DEFAULT_PROFILE_ID,
    directive: "process",
    userId: "erinoverview",
    userPass: "secret",
    profiles: [
        {
            id: DEFAULT_PROFILE_ID,
            name: "Quickstart Local",
            apiUrl: "http://localhost:8085/dr-egeria/process",
            environmentKey: "Quickstart Local",
            userProfileKey: "Egeria Markdown",
            outputFolder: "dr-egeria-outbox",
            inputFolder: "",
            environment: {
                "Egeria Kafka Endpoint": "host.docker.internal:9192",
                "Egeria Jupyter": true,
                "Dr.Egeria Outbox": ".",
                "Dr.Egeria Inbox": ".",
                "Egeria Integration Daemon": "qs-integration-daemon",
                "Egeria Integration Daemon URL": "https://host.docker.internal:9443",
                "Egeria View Server": "qs-view-server",
                "Egeria View Server URL": "https://host.docker.internal:9443",
                "Egeria Metadata Store": "qs-metadata-store",
                "Egeria Platform URL": "https://host.docker.internal:9443",
                "Egeria Engine Host": "qs-engine-host",
                "Egeria Engine Host URL": "https://host.docker.internal:9443",
                "Egeria Glossary Path": "/work/Work-Obsidian/glossary",
                "Egeria Mermaid Folder": "/work/Work-Obsidian/mermaid_graphs",
                "Pyegeria Root": "/work/Work-Obsidian",
                "Pyegeria Config Directory": "/config",
                "Pyegeria User Format Sets Dir": "/config/format-sets",
                "Pyegeria Publishing Root": "http://localhost:8085/work/Work-Obsidian/dr-egeria-outbox",
                "console_width": 250
            },
            userProfile: {
                "Egeria Home Glossary Name": "Egeria-Markdown",
                "Egeria Local Qualifier": "PDR",
                "Egeria Home Collection": "MyHome"
            }
        }
    ]
};

export default class SendNotePlugin extends Plugin {
    settings: SendNoteSettings = DEFAULT_SETTINGS;

    async onload() {
        await this.loadSettings();

        this.addRibbonIcon("phone", "Call Dr.Egeria", async () => {
            await this.sendCurrentNote();
        });

        this.addCommand({
            id: "send-current-note-to-dr-egeria",
            name: "Send Current Note to Dr.Egeria",
            callback: async () => {
                await this.sendCurrentNote();
            }
        });

        this.addCommand({
            id: "refresh-dr-egeria-command-specs",
            name: "Refresh Dr.Egeria Command Specs",
            callback: async () => {
                await this.refreshCommandSpecs();
            }
        });

        this.addSettingTab(new SendNoteSettingTab(this.app, this));
    }

    getActiveProfile(): DrEgeriaProfile {
        return this.settings.profiles.find(profile => profile.id === this.settings.activeProfileId)
            ?? this.settings.profiles[0]
            ?? DEFAULT_SETTINGS.profiles[0];
    }

    async sendCurrentNote() {
        const file = this.app.workspace.getActiveFile();
        if (!file) {
            new Notice("No active file.");
            return;
        }

        const profile = this.getActiveProfile();
        const basePath = normalizePath(file.path);

        let inputFile = basePath;
        if (profile.inputFolder && profile.inputFolder.trim().length > 0) {
            const normalizedInputFolder = profile.inputFolder.replace(/[\\/]+$/g, "").replace(/^[\\/]+/g, "");
            const normalizedBasePath = basePath.replace(/^[\\/]+/g, "");
            
            const inputSegments = normalizedInputFolder.split(/[\\/]+/);
            const baseSegments = normalizedBasePath.split(/[\\/]+/);

            // Check for overlap: does normalizedInputFolder end with segments that normalizedBasePath starts with?
            let overlapIndex = -1;
            for (let i = 0; i < inputSegments.length; i++) {
                // Check if inputSegments starting from i match the beginning of baseSegments
                let match = true;
                for (let j = 0; j < inputSegments.length - i && j < baseSegments.length; j++) {
                    if (inputSegments[i + j] !== baseSegments[j]) {
                        match = false;
                        break;
                    }
                }
                if (match && (inputSegments.length - i) > 0) {
                    overlapIndex = i;
                    break;
                }
            }

            console.log("🛠️ Path Debug:", {
                normalizedInputFolder,
                normalizedBasePath,
                overlapIndex,
                inputSegments,
                baseSegments
            });

            if (overlapIndex !== -1) {
                // Merge segments
                const combined = [...inputSegments.slice(0, overlapIndex), ...baseSegments];
                inputFile = (profile.inputFolder.startsWith("/") ? "/" : "") + combined.join("/");
            } else if (normalizedInputFolder === ".") {
                inputFile = normalizedBasePath;
            } else if (normalizedBasePath.startsWith(normalizedInputFolder + "/")) {
                inputFile = (profile.inputFolder.startsWith("/") ? "/" : "") + normalizedBasePath;
            } else {
                inputFile = (profile.inputFolder.startsWith("/") ? "/" : "") + `${normalizedInputFolder}/${normalizedBasePath}`;
            }
        }
        
        console.log("🛠️ Final inputFile:", inputFile);

        const payload = {
            input_file: inputFile,
            source_file: file.name,
            output_folder: profile.outputFolder || file.parent?.path || "",
            directive: this.settings.directive,
            environment_key: profile.environmentKey,
            user_profile_key: profile.userProfileKey,
            environment: profile.environment,
            user_profile: profile.userProfile,
            user_id: this.settings.userId,
            user_pass: this.settings.userPass
        };

        console.log("📤 Sending note with payload:", {
            ...payload,
            user_pass: payload.user_pass ? "(redacted)" : ""
        });

        try {
            const response = await requestUrl({
                url: profile.apiUrl,
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify(payload),
                throw: false
            });

            const rawBody = response.text ?? "";
            const parsed = this.parseProcessResponse(rawBody);

            console.log("📥 Response status:", response.status);
            console.log("📥 Response body:", parsed ?? rawBody);

            if (response.status < 200 || response.status >= 300) {
                const detail = parsed?.message || this.extractFastApiError(rawBody) || rawBody || "Request failed";
                console.error("Dr.Egeria HTTP Error:", response.status, rawBody);
                throw new Error(`HTTP ${response.status} - ${detail}`);
            }

            if (!parsed) {
                new ResultModal(this.app, rawBody || "(no output)").open();
                new Notice("✅ Dr.Egeria completed, but returned an unstructured response.");
                return;
            }

            if (parsed.status === "error") {
                const errorContent = this.formatProcessResponse(parsed);
                new ResultModal(this.app, errorContent).open();
                throw new Error(parsed.message || "Dr.Egeria processing failed.");
            }

            const outputLocation = parsed.output_path || parsed.output_file || parsed.output_folder;
            new Notice(outputLocation
                ? `✅ Dr.Egeria completed. Output: ${outputLocation}`
                : "✅ Dr.Egeria completed.");

            new ResultModal(this.app, this.formatProcessResponse(parsed)).open();

        } catch (err: unknown) {
            const message = this.formatError(err);
            new Notice("❌ Failed to send note: " + message);
            console.error("SendNotePlugin error:", err);
        }
    }

    async refreshCommandSpecs() {
        const profile = this.getActiveProfile();
        const refreshUrl = profile.apiUrl.replace("/process", "/refresh");

        try {
            const response = await requestUrl({
                url: refreshUrl,
                method: "POST",
                headers: {
                    "Accept": "application/json"
                },
                throw: false
            });

            if (response.status >= 200 && response.status < 300) {
                new Notice("✅ Command specs refreshed.");
            } else {
                new Notice(`❌ Refresh failed (${response.status}): ${response.text}`);
            }
        } catch (err) {
            new Notice(`❌ Refresh failed: ${this.formatError(err)}`);
        }
    }

    parseProcessResponse(rawBody: string): DrEgeriaProcessResponse | undefined {
        if (!rawBody || rawBody.trim().length === 0) {
            return undefined;
        }

        try {
            return JSON.parse(rawBody) as DrEgeriaProcessResponse;
        } catch {
            return undefined;
        }
    }

    extractFastApiError(rawBody: string): string | undefined {
        try {
            const parsed = JSON.parse(rawBody) as { detail?: unknown };
            if (typeof parsed.detail === "string") {
                return parsed.detail;
            }
            if (parsed.detail && typeof parsed.detail === "object") {
                const detail = parsed.detail as { message?: unknown };
                if (typeof detail.message === "string") {
                    return detail.message;
                }
            }
        } catch {
            return undefined;
        }

        return undefined;
    }

    formatProcessResponse(response: DrEgeriaProcessResponse): string {
        return [
            `Status: ${response.status}`,
            `Message: ${response.message}`,
            response.input_file ? `Input file: ${response.input_file}` : undefined,
            response.output_folder ? `Output folder: ${response.output_folder}` : undefined,
            response.output_file ? `Output file: ${response.output_file}` : undefined,
            response.output_path ? `Output path: ${response.output_path}` : undefined,
            response.environment_key ? `Environment: ${response.environment_key}` : undefined,
            response.user_profile_key ? `User profile: ${response.user_profile_key}` : undefined,
            "",
            response.console_output || ""
        ].filter(line => line !== undefined).join("\n");
    }

    formatError(err: unknown): string {
        if (err instanceof Error) {
            return err.message;
        }
        if (typeof err === "string") {
            return err;
        }
        try {
            return JSON.stringify(err);
        } catch {
            return "Unknown error";
        }
    }

    async loadSettings() {
        const loaded = await this.loadData();
        this.settings = Object.assign({}, DEFAULT_SETTINGS, loaded);

        if (!this.settings.profiles || this.settings.profiles.length === 0) {
            this.settings.profiles = DEFAULT_SETTINGS.profiles;
        }

        if (!this.settings.activeProfileId) {
            this.settings.activeProfileId = this.settings.profiles[0].id;
        }

        if (!this.settings.directive) {
            this.settings.directive = "process";
        }

        this.repairDefaultProfile();
        await this.saveSettings();
    }

    repairDefaultProfile() {
        const defaultProfile = DEFAULT_SETTINGS.profiles[0];
        const activeProfile = this.getActiveProfile();

        activeProfile.environment = Object.assign(
            {},
            defaultProfile.environment,
            activeProfile.environment
        );

        activeProfile.userProfile = Object.assign(
            {},
            defaultProfile.userProfile,
            activeProfile.userProfile
        );

        if (!activeProfile.environment["Dr.Egeria Inbox"]) {
            activeProfile.environment["Dr.Egeria Inbox"] = "loading-bay/dr-egeria-inbox";
        }

        if (!activeProfile.environment["Dr.Egeria Outbox"]) {
            activeProfile.environment["Dr.Egeria Outbox"] = "distribution-hub/dr-egeria-outbox";
        }

        if (!activeProfile.environment["Pyegeria Root"]) {
            // Default to work/Obsidian relative to workspace root if not specified.
            // In the backend, WORKSPACE_ROOT is the parent of the deployment dir.
            activeProfile.environment["Pyegeria Root"] = "work/Obsidian";
        }

        if (!activeProfile.inputFolder || activeProfile.inputFolder === "") {
            // Default input folder for quickstart
            activeProfile.inputFolder = "loading-bay/dr-egeria-inbox";
        }

        if (!activeProfile.outputFolder) {
            activeProfile.outputFolder = "distribution-hub/dr-egeria-outbox";
        }
    }

    async saveSettings() {
        await this.saveData(this.settings);
    }
}

    class SendNoteSettingTab extends PluginSettingTab {
    plugin: SendNotePlugin;

    constructor(app: App, plugin: SendNotePlugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display(): void {
        const { containerEl } = this;
        containerEl.empty();

        const activeProfile = this.plugin.getActiveProfile();

        containerEl.createEl("h2", { text: "Dr.Egeria Settings" });

        new Setting(containerEl)
            .setName("Active Profile")
            .setDesc("Select the Dr.Egeria configuration profile to use.")
            .addDropdown(dropdown => {
                for (const profile of this.plugin.settings.profiles) {
                    dropdown.addOption(profile.id, profile.name);
                }

                dropdown
                    .setValue(this.plugin.settings.activeProfileId)
                    .onChange(async value => {
                        this.plugin.settings.activeProfileId = value;
                        await this.plugin.saveSettings();
                        this.display();
                    });
            });

        new Setting(containerEl)
            .setName("Directive")
            .setDesc("How Dr.Egeria should handle the file.")
            .addDropdown(dropdown => dropdown
                .addOption("process", "process")
                .addOption("validate", "validate")
                .addOption("display", "display")
                .setValue(this.plugin.settings.directive)
                .onChange(async value => {
                    if (value === "process" || value === "validate" || value === "display") {
                        this.plugin.settings.directive = value;
                    }
                    await this.plugin.saveSettings();
                }));

        containerEl.createEl("h3", { text: "Credentials" });

        new Setting(containerEl)
            .setName("User ID")
            .setDesc("Egeria user name. Stored separately from the profile configuration.")
            .addText(text => text
                .setPlaceholder("erinoverview")
                .setValue(this.plugin.settings.userId)
                .onChange(async value => {
                    this.plugin.settings.userId = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Password")
            .setDesc("Egeria password. Stored separately from the profile configuration.")
            .addText(text => {
                text.setPlaceholder("secret")
                    .setValue(this.plugin.settings.userPass)
                    .onChange(async value => {
                        this.plugin.settings.userPass = value;
                        await this.plugin.saveSettings();
                    });
                text.inputEl.type = "password";
                return text;
            });

        containerEl.createEl("h3", { text: `Profile: ${activeProfile.name}` });

        new Setting(containerEl)
            .setName("Profile Name")
            .addText(text => text
                .setValue(activeProfile.name)
                .onChange(async value => {
                    activeProfile.name = value;
                    await this.plugin.saveSettings();
                    this.display();
                }));

        new Setting(containerEl)
            .setName("API URL")
            .setDesc("FastAPI endpoint that accepts Dr.Egeria process requests.")
            .addText(text => text
                .setPlaceholder("http://localhost:8085/dr-egeria/process")
                .setValue(activeProfile.apiUrl)
                .onChange(async value => {
                    activeProfile.apiUrl = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Environment Key")
            .setDesc("Logical key for the Environment configuration.")
            .addText(text => text
                .setPlaceholder("Quickstart Local")
                .setValue(activeProfile.environmentKey)
                .onChange(async value => {
                    activeProfile.environmentKey = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("User Profile Key")
            .setDesc("Logical key for the User Profile configuration.")
            .addText(text => text
                .setPlaceholder("Egeria Markdown")
                .setValue(activeProfile.userProfileKey)
                .onChange(async value => {
                    activeProfile.userProfileKey = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Output Folder")
            .setDesc("Output folder passed to Dr.Egeria.")
            .addText(text => text
                .setPlaceholder("distribution-hub/dr-egeria-outbox")
                .setValue(activeProfile.outputFolder)
                .onChange(async value => {
                    activeProfile.outputFolder = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Input Folder")
            .setDesc("Optional folder to prepend to the active note path.")
            .addText(text => text
                .setPlaceholder("loading-bay/dr-egeria-inbox")
                .setValue(activeProfile.inputFolder || "")
                .onChange(async value => {
                    activeProfile.inputFolder = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Environment JSON")
            .setDesc("Environment configuration equivalent to the Environment block in config_workspaces.json.")
            .addTextArea(text => {
                text.inputEl.rows = 12;
                text.inputEl.cols = 80;
                text.setValue(JSON.stringify(activeProfile.environment, null, 2));
                text.onChange(async value => {
                    try {
                        activeProfile.environment = JSON.parse(value) as DrEgeriaConfigBlock;
                        await this.plugin.saveSettings();
                    } catch {
                        // Do not save invalid JSON while the user is editing.
                    }
                });
            });

        new Setting(containerEl)
            .setName("User Profile JSON")
            .setDesc("User profile configuration equivalent to the User Profile block in config_workspaces.json. Do not include credentials here.")
            .addTextArea(text => {
                text.inputEl.rows = 6;
                text.inputEl.cols = 80;
                text.setValue(JSON.stringify(activeProfile.userProfile, null, 2));
                text.onChange(async value => {
                    try {
                        activeProfile.userProfile = JSON.parse(value) as DrEgeriaConfigBlock;
                        await this.plugin.saveSettings();
                    } catch {
                        // Do not save invalid JSON while the user is editing.
                    }
                });
            });

        containerEl.createEl("h3", { text: "Maintenance" });

        new Setting(containerEl)
            .setName("Refresh Command Specs")
            .setDesc("Reload Dr.Egeria command definitions from JSON files on the server.")
            .addButton(button => button
                .setButtonText("Refresh Now")
                .onClick(async () => {
                    await this.plugin.refreshCommandSpecs();
                }));
    }
}

class ResultModal extends Modal {
    text: string;

    constructor(app: App, text: string) {
        super(app);
        this.text = text;
    }

    onOpen() {
        const { contentEl, modalEl } = this;
        contentEl.createEl("h2", { text: "Dr.Egeria Results" });
        
        // Make the modal resizable via CSS
        modalEl.style.resize = "both";
        modalEl.style.overflow = "auto";
        modalEl.style.minWidth = "400px";
        modalEl.style.minHeight = "300px";
        modalEl.style.width = "80%";
        modalEl.style.height = "70%";

        const pre = contentEl.createEl("pre", { text: this.text });
        pre.style.whiteSpace = "pre-wrap";
        pre.style.wordBreak = "break-word";
        pre.style.height = "calc(100% - 60px)";
        pre.style.overflowY = "auto";
        pre.style.margin = "0";
        pre.style.padding = "10px";
        pre.style.border = "1px solid var(--background-modifier-border)";
        pre.style.backgroundColor = "var(--background-secondary)";
    }

    onClose() {
        const { contentEl } = this;
        contentEl.empty();
    }
}
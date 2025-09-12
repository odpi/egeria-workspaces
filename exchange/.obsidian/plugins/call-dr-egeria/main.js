"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// main.ts
var main_exports = {};
__export(main_exports, {
  default: () => SendNotePlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian = require("obsidian");
var DEFAULT_SETTINGS = {
  apiUrl: "http://localhost:8085/dr-egeria/process",
  userId: "erinoverview",
  userPass: "secret",
  outputFolder: "Monday",
  inputFolder: ""
};
var SendNotePlugin = class extends import_obsidian.Plugin {
  constructor() {
    super(...arguments);
    this.settings = DEFAULT_SETTINGS;
  }
  async onload() {
    await this.loadSettings();
    this.addRibbonIcon("phone", "Call Dr.Egeria", async () => {
      await this.sendCurrentNote();
    });
    this.addCommand({
      id: "send-current-note",
      name: "Send Current Note via REST",
      callback: async () => {
        await this.sendCurrentNote();
      }
    });
    this.addSettingTab(new SendNoteSettingTab(this.app, this));
  }
  async sendCurrentNote() {
    const file = this.app.workspace.getActiveFile();
    if (!file) {
      new import_obsidian.Notice("No active file.");
      return;
    }
    const content = await this.app.vault.read(file);
    const baseName = file.basename + ".md";
    const inputFile = this.settings.inputFolder && this.settings.inputFolder.trim().length > 0 ? `${this.settings.inputFolder.replace(/\\+$/,'').replace(/\/+$/,'')}/${baseName}` : baseName;
    const payload = {
      input_file: inputFile,
      output_folder: this.settings.outputFolder,
      directive: "process",
      url: "https://host.docker.internal:9443",
      server: "qs-view-server",
      user_id: this.settings.userId,
      user_pass: this.settings.userPass
      // content: content
    };
    console.log("\u{1F4E4} Sending note with payload:", payload);
    try {
      const response = await (0, import_obsidian.requestUrl)({
        url: this.settings.apiUrl,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify(payload),
        // timeout: 30000, // optional
        throw: true
        // set to false if you prefer not to throw on non-2xx
      });
      const contentType = (response.headers?.["content-type"] ?? "").toLowerCase();
      const rawBody = response.text ?? "";
      let parsed = void 0;
      if (contentType.includes("application/json")) {
        try {
          parsed = JSON.parse(rawBody);
        } catch {
        }
      }
      console.log("\u{1F4E5} Response status:", response.status);
      console.log("\u{1F4E5} Response body:", parsed ?? rawBody);
      if (response.status < 200 || response.status >= 300) {
        const detail = parsed && (parsed.message || parsed.error || parsed.detail) || rawBody || "Request failed";
        throw new Error(`HTTP ${response.status} - ${detail}`);
      }
      new import_obsidian.Notice("\u2705 Note sent successfully!");
    } catch (err) {
      let message = "Unknown error";
      if (err instanceof Error) {
        message = err.message;
      } else if (typeof err === "string") {
        message = err;
      } else {
        try {
          message = JSON.stringify(err);
        } catch {
        }
      }
      new import_obsidian.Notice("\u274C Failed to send note: " + message);
      console.error("SendNotePlugin error:", err);
    }
  }
  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }
  async saveSettings() {
    await this.saveData(this.settings);
  }
};
var SendNoteSettingTab = class extends import_obsidian.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.createEl("h2", { text: "Send Note Plugin Settings" });
    new import_obsidian.Setting(containerEl).setName("API URL").setDesc("Endpoint to send notes to").addText((text) => text.setPlaceholder("https://localhost:8085/dr-egeria/process").setValue(this.plugin.settings.apiUrl).onChange(async (value) => {
      this.plugin.settings.apiUrl = value;
      await this.plugin.saveSettings();
    }));
    new import_obsidian.Setting(containerEl).setName("User ID").setDesc("User name for authentication").addText((text) => text.setPlaceholder("erinoverview").setValue(this.plugin.settings.userId).onChange(async (value) => {
      this.plugin.settings.userId = value;
      await this.plugin.saveSettings();
    }));
    new import_obsidian.Setting(containerEl).setName("Password").setDesc("Password for authentication").addText((text) => text.setPlaceholder("secret").setValue(this.plugin.settings.userPass).onChange(async (value) => {
      this.plugin.settings.userPass = value;
      await this.plugin.saveSettings();
    }));
    new import_obsidian.Setting(containerEl).setName("Output Folder").setDesc("Name of the output folder").addText((text) => text.setPlaceholder("Monday").setValue(this.plugin.settings.outputFolder).onChange(async (value) => {
      this.plugin.settings.outputFolder = value;
      await this.plugin.saveSettings();
    }));
    new import_obsidian.Setting(containerEl).setName("Input Folder (optional)").setDesc("If set, will be prepended to input_file as 'input_folder/filename.md'").addText((text) => text.setPlaceholder("inbox").setValue(this.plugin.settings.inputFolder || "").onChange(async (value) => {
      this.plugin.settings.inputFolder = value;
      await this.plugin.saveSettings();
    }));
  }
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsibWFpbi50cyJdLAogICJzb3VyY2VzQ29udGVudCI6IFsiaW1wb3J0IHsgQXBwLCBFZGl0b3IsIE1hcmtkb3duVmlldywgTW9kYWwsIFBsdWdpbiwgTm90aWNlLCBQbHVnaW5TZXR0aW5nVGFiLCBTZXR0aW5nLCByZXF1ZXN0VXJsIH0gZnJvbSBcIm9ic2lkaWFuXCI7XG5cbmludGVyZmFjZSBTZW5kTm90ZVNldHRpbmdzIHtcbiAgICBhcGlVcmw6IHN0cmluZztcbiAgICB1c2VySWQ6IHN0cmluZztcbiAgICB1c2VyUGFzczogc3RyaW5nO1xuICAgIG91dHB1dEZvbGRlcjogc3RyaW5nO1xufVxuXG5jb25zdCBERUZBVUxUX1NFVFRJTkdTOiBTZW5kTm90ZVNldHRpbmdzID0ge1xuICAgIGFwaVVybDogXCJodHRwOi8vbG9jYWxob3N0OjgwODUvZHItZWdlcmlhL3Byb2Nlc3NcIixcbiAgICB1c2VySWQ6IFwiZXJpbm92ZXJ2aWV3XCIsXG4gICAgdXNlclBhc3M6IFwic2VjcmV0XCIsXG4gICAgb3V0cHV0Rm9sZGVyOiBcIk1vbmRheVwiXG59O1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBTZW5kTm90ZVBsdWdpbiBleHRlbmRzIFBsdWdpbiB7XG4gICAgc2V0dGluZ3M6IFNlbmROb3RlU2V0dGluZ3MgPSBERUZBVUxUX1NFVFRJTkdTO1xuXG4gICAgYXN5bmMgb25sb2FkKCkge1xuICAgICAgICBhd2FpdCB0aGlzLmxvYWRTZXR0aW5ncygpO1xuXG4gICAgICAgIC8vIFJpYmJvbiBpY29uXG4gICAgICAgIHRoaXMuYWRkUmliYm9uSWNvbihcInBob25lXCIsIFwiQ2FsbCBEci5FZ2VyaWFcIiwgYXN5bmMgKCkgPT4ge1xuICAgICAgICAgICAgYXdhaXQgdGhpcy5zZW5kQ3VycmVudE5vdGUoKTtcbiAgICAgICAgfSk7XG5cbiAgICAgICAgLy8gQ29tbWFuZCBwYWxldHRlXG4gICAgICAgIHRoaXMuYWRkQ29tbWFuZCh7XG4gICAgICAgICAgICBpZDogXCJzZW5kLWN1cnJlbnQtbm90ZVwiLFxuICAgICAgICAgICAgbmFtZTogXCJTZW5kIEN1cnJlbnQgTm90ZSB2aWEgUkVTVFwiLFxuICAgICAgICAgICAgY2FsbGJhY2s6IGFzeW5jICgpID0+IHtcbiAgICAgICAgICAgICAgICBhd2FpdCB0aGlzLnNlbmRDdXJyZW50Tm90ZSgpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9KTtcblxuICAgICAgICAvLyBTZXR0aW5ncyB0YWJcbiAgICAgICAgdGhpcy5hZGRTZXR0aW5nVGFiKG5ldyBTZW5kTm90ZVNldHRpbmdUYWIodGhpcy5hcHAsIHRoaXMpKTtcbiAgICB9XG5cbiAgICBhc3luYyBzZW5kQ3VycmVudE5vdGUoKSB7XG4gICAgICAgIGNvbnN0IGZpbGUgPSB0aGlzLmFwcC53b3Jrc3BhY2UuZ2V0QWN0aXZlRmlsZSgpO1xuICAgICAgICBpZiAoIWZpbGUpIHtcbiAgICAgICAgICAgIG5ldyBOb3RpY2UoXCJObyBhY3RpdmUgZmlsZS5cIik7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBjb250ZW50ID0gYXdhaXQgdGhpcy5hcHAudmF1bHQucmVhZChmaWxlKTtcblxuICAgICAgICBjb25zdCBwYXlsb2FkID0ge1xuICAgICAgICAgICAgaW5wdXRfZmlsZTogZmlsZS5iYXNlbmFtZStcIi5tZFwiLFxuICAgICAgICAgICAgb3V0cHV0X2ZvbGRlcjogdGhpcy5zZXR0aW5ncy5vdXRwdXRGb2xkZXIsXG4gICAgICAgICAgICBkaXJlY3RpdmU6IFwicHJvY2Vzc1wiLFxuICAgICAgICAgICAgdXJsOiBcImh0dHBzOi8vaG9zdC5kb2NrZXIuaW50ZXJuYWw6OTQ0M1wiLFxuICAgICAgICAgICAgc2VydmVyOiBcInFzLXZpZXctc2VydmVyXCIsXG4gICAgICAgICAgICB1c2VyX2lkOiB0aGlzLnNldHRpbmdzLnVzZXJJZCxcbiAgICAgICAgICAgIHVzZXJfcGFzczogdGhpcy5zZXR0aW5ncy51c2VyUGFzc1xuICAgICAgICAgICAvLyBjb250ZW50OiBjb250ZW50XG4gICAgICAgIH07XG5cbiAgICAgICAgY29uc29sZS5sb2coXCJcdUQ4M0RcdURDRTQgU2VuZGluZyBub3RlIHdpdGggcGF5bG9hZDpcIiwgcGF5bG9hZCk7XG5cbiAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgIGNvbnN0IHJlc3BvbnNlID0gYXdhaXQgcmVxdWVzdFVybCh7XG4gICAgICAgICAgICAgICAgdXJsOiB0aGlzLnNldHRpbmdzLmFwaVVybCxcbiAgICAgICAgICAgICAgICBtZXRob2Q6IFwiUE9TVFwiLFxuICAgICAgICAgICAgICAgIGhlYWRlcnM6IHtcbiAgICAgICAgICAgICAgICAgICAgXCJDb250ZW50LVR5cGVcIjogXCJhcHBsaWNhdGlvbi9qc29uXCIsXG4gICAgICAgICAgICAgICAgICAgIFwiQWNjZXB0XCI6IFwiYXBwbGljYXRpb24vanNvblwiXG4gICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICBib2R5OiBKU09OLnN0cmluZ2lmeShwYXlsb2FkKSxcbiAgICAgICAgICAgICAgICAvLyB0aW1lb3V0OiAzMDAwMCwgLy8gb3B0aW9uYWxcbiAgICAgICAgICAgICAgICAgdGhyb3c6IHRydWUsICAgLy8gc2V0IHRvIGZhbHNlIGlmIHlvdSBwcmVmZXIgbm90IHRvIHRocm93IG9uIG5vbi0yeHhcbiAgICAgICAgICAgIH0pO1xuXG5cbiAgICAgICAgICAgIGNvbnN0IGNvbnRlbnRUeXBlID0gKHJlc3BvbnNlLmhlYWRlcnM/LltcImNvbnRlbnQtdHlwZVwiXSA/PyBcIlwiKS50b0xvd2VyQ2FzZSgpO1xuICAgICAgICAgICAgY29uc3QgcmF3Qm9keTogc3RyaW5nID0gcmVzcG9uc2UudGV4dCA/PyBcIlwiO1xuICAgICAgICAgICAgbGV0IHBhcnNlZDogYW55ID0gdW5kZWZpbmVkO1xuICAgICAgICAgICAgaWYgKGNvbnRlbnRUeXBlLmluY2x1ZGVzKFwiYXBwbGljYXRpb24vanNvblwiKSkge1xuICAgICAgICAgICAgICAgIHRyeSB7XG4gICAgICAgICAgICAgICAgICAgIHBhcnNlZCA9IEpTT04ucGFyc2UocmF3Qm9keSk7XG4gICAgICAgICAgICAgICAgfSBjYXRjaCB7XG4gICAgICAgICAgICAgICAgICAgIC8vIGxlYXZlIHBhcnNlZCB1bmRlZmluZWQgaWYgSlNPTiBpcyBtYWxmb3JtZWRcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG5cbiAgICAgICAgICAgIGNvbnNvbGUubG9nKFwiXHVEODNEXHVEQ0U1IFJlc3BvbnNlIHN0YXR1czpcIiwgcmVzcG9uc2Uuc3RhdHVzKTtcbiAgICAgICAgICAgIGNvbnNvbGUubG9nKFwiXHVEODNEXHVEQ0U1IFJlc3BvbnNlIGJvZHk6XCIsIHBhcnNlZCA/PyByYXdCb2R5KTtcblxuICAgICAgICAgICAgaWYgKHJlc3BvbnNlLnN0YXR1cyA8IDIwMCB8fCByZXNwb25zZS5zdGF0dXMgPj0gMzAwKSB7XG4gICAgICAgICAgICAgICAgY29uc3QgZGV0YWlsID1cbiAgICAgICAgICAgICAgICAgICAgKHBhcnNlZCAmJiAocGFyc2VkLm1lc3NhZ2UgfHwgcGFyc2VkLmVycm9yIHx8IHBhcnNlZC5kZXRhaWwpKSB8fFxuICAgICAgICAgICAgICAgICAgICByYXdCb2R5IHx8XG4gICAgICAgICAgICAgICAgICAgIFwiUmVxdWVzdCBmYWlsZWRcIjtcbiAgICAgICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoYEhUVFAgJHtyZXNwb25zZS5zdGF0dXN9IC0gJHtkZXRhaWx9YCk7XG4gICAgICAgICAgICB9XG5cbiAgICAgICAgICAgIG5ldyBOb3RpY2UoXCJcdTI3MDUgTm90ZSBzZW50IHN1Y2Nlc3NmdWxseSFcIik7XG5cbiAgICAgICAgfSBjYXRjaCAoZXJyOiB1bmtub3duKSB7XG4gICAgICAgICAgICBsZXQgbWVzc2FnZSA9IFwiVW5rbm93biBlcnJvclwiO1xuICAgICAgICAgICAgaWYgKGVyciBpbnN0YW5jZW9mIEVycm9yKSB7XG4gICAgICAgICAgICAgICAgbWVzc2FnZSA9IGVyci5tZXNzYWdlO1xuICAgICAgICAgICAgfSBlbHNlIGlmICh0eXBlb2YgZXJyID09PSBcInN0cmluZ1wiKSB7XG4gICAgICAgICAgICAgICAgbWVzc2FnZSA9IGVycjtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgdHJ5IHsgbWVzc2FnZSA9IEpTT04uc3RyaW5naWZ5KGVycik7IH0gY2F0Y2gge31cbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIG5ldyBOb3RpY2UoXCJcdTI3NEMgRmFpbGVkIHRvIHNlbmQgbm90ZTogXCIgKyBtZXNzYWdlKTtcbiAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoXCJTZW5kTm90ZVBsdWdpbiBlcnJvcjpcIiwgZXJyKTtcbiAgICAgICAgfVxuXG4gICAgfVxuXG4gICAgYXN5bmMgbG9hZFNldHRpbmdzKCkge1xuICAgICAgICB0aGlzLnNldHRpbmdzID0gT2JqZWN0LmFzc2lnbih7fSwgREVGQVVMVF9TRVRUSU5HUywgYXdhaXQgdGhpcy5sb2FkRGF0YSgpKTtcbiAgICB9XG5cbiAgICBhc3luYyBzYXZlU2V0dGluZ3MoKSB7XG4gICAgICAgIGF3YWl0IHRoaXMuc2F2ZURhdGEodGhpcy5zZXR0aW5ncyk7XG4gICAgfVxufVxuXG5jbGFzcyBTZW5kTm90ZVNldHRpbmdUYWIgZXh0ZW5kcyBQbHVnaW5TZXR0aW5nVGFiIHtcbiAgICBwbHVnaW46IFNlbmROb3RlUGx1Z2luO1xuXG4gICAgY29uc3RydWN0b3IoYXBwOiBBcHAsIHBsdWdpbjogU2VuZE5vdGVQbHVnaW4pIHtcbiAgICAgICAgc3VwZXIoYXBwLCBwbHVnaW4pO1xuICAgICAgICB0aGlzLnBsdWdpbiA9IHBsdWdpbjtcbiAgICB9XG5cbiAgICBkaXNwbGF5KCk6IHZvaWQge1xuICAgICAgICBjb25zdCB7IGNvbnRhaW5lckVsIH0gPSB0aGlzO1xuICAgICAgICBjb250YWluZXJFbC5lbXB0eSgpO1xuXG4gICAgICAgIGNvbnRhaW5lckVsLmNyZWF0ZUVsKFwiaDJcIiwgeyB0ZXh0OiBcIlNlbmQgTm90ZSBQbHVnaW4gU2V0dGluZ3NcIiB9KTtcblxuICAgICAgICBuZXcgU2V0dGluZyhjb250YWluZXJFbClcbiAgICAgICAgICAgIC5zZXROYW1lKFwiQVBJIFVSTFwiKVxuICAgICAgICAgICAgLnNldERlc2MoXCJFbmRwb2ludCB0byBzZW5kIG5vdGVzIHRvXCIpXG4gICAgICAgICAgICAuYWRkVGV4dCh0ZXh0ID0+IHRleHRcbiAgICAgICAgICAgICAgICAuc2V0UGxhY2Vob2xkZXIoXCJodHRwczovL2xvY2FsaG9zdDo4MDg1L2RyLWVnZXJpYS9wcm9jZXNzXCIpXG4gICAgICAgICAgICAgICAgLnNldFZhbHVlKHRoaXMucGx1Z2luLnNldHRpbmdzLmFwaVVybClcbiAgICAgICAgICAgICAgICAub25DaGFuZ2UoYXN5bmMgKHZhbHVlKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMucGx1Z2luLnNldHRpbmdzLmFwaVVybCA9IHZhbHVlO1xuICAgICAgICAgICAgICAgICAgICBhd2FpdCB0aGlzLnBsdWdpbi5zYXZlU2V0dGluZ3MoKTtcbiAgICAgICAgICAgICAgICB9KSk7XG5cbiAgICAgICAgbmV3IFNldHRpbmcoY29udGFpbmVyRWwpXG4gICAgICAgICAgICAuc2V0TmFtZShcIlVzZXIgSURcIilcbiAgICAgICAgICAgIC5zZXREZXNjKFwiVXNlciBuYW1lIGZvciBhdXRoZW50aWNhdGlvblwiKVxuICAgICAgICAgICAgLmFkZFRleHQodGV4dCA9PiB0ZXh0XG4gICAgICAgICAgICAgICAgLnNldFBsYWNlaG9sZGVyKFwiZXJpbm92ZXJ2aWV3XCIpXG4gICAgICAgICAgICAgICAgLnNldFZhbHVlKHRoaXMucGx1Z2luLnNldHRpbmdzLnVzZXJJZClcbiAgICAgICAgICAgICAgICAub25DaGFuZ2UoYXN5bmMgKHZhbHVlKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMucGx1Z2luLnNldHRpbmdzLnVzZXJJZCA9IHZhbHVlO1xuICAgICAgICAgICAgICAgICAgICBhd2FpdCB0aGlzLnBsdWdpbi5zYXZlU2V0dGluZ3MoKTtcbiAgICAgICAgICAgICAgICB9KSk7XG5cbiAgICAgICAgbmV3IFNldHRpbmcoY29udGFpbmVyRWwpXG4gICAgICAgICAgICAuc2V0TmFtZShcIlBhc3N3b3JkXCIpXG4gICAgICAgICAgICAuc2V0RGVzYyhcIlBhc3N3b3JkIGZvciBhdXRoZW50aWNhdGlvblwiKVxuICAgICAgICAgICAgLmFkZFRleHQodGV4dCA9PiB0ZXh0XG4gICAgICAgICAgICAgICAgLnNldFBsYWNlaG9sZGVyKFwic2VjcmV0XCIpXG4gICAgICAgICAgICAgICAgLnNldFZhbHVlKHRoaXMucGx1Z2luLnNldHRpbmdzLnVzZXJQYXNzKVxuICAgICAgICAgICAgICAgIC5vbkNoYW5nZShhc3luYyAodmFsdWUpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5wbHVnaW4uc2V0dGluZ3MudXNlclBhc3MgPSB2YWx1ZTtcbiAgICAgICAgICAgICAgICAgICAgYXdhaXQgdGhpcy5wbHVnaW4uc2F2ZVNldHRpbmdzKCk7XG4gICAgICAgICAgICAgICAgfSkpO1xuXG4gICAgICAgIG5ldyBTZXR0aW5nKGNvbnRhaW5lckVsKVxuICAgICAgICAgICAgLnNldE5hbWUoXCJPdXRwdXQgRm9sZGVyXCIpXG4gICAgICAgICAgICAuc2V0RGVzYyhcIk5hbWUgb2YgdGhlIG91dHB1dCBmb2xkZXJcIilcbiAgICAgICAgICAgIC5hZGRUZXh0KHRleHQgPT4gdGV4dFxuICAgICAgICAgICAgICAgIC5zZXRQbGFjZWhvbGRlcihcIk1vbmRheVwiKVxuICAgICAgICAgICAgICAgIC5zZXRWYWx1ZSh0aGlzLnBsdWdpbi5zZXR0aW5ncy5vdXRwdXRGb2xkZXIpXG4gICAgICAgICAgICAgICAgLm9uQ2hhbmdlKGFzeW5jICh2YWx1ZSkgPT4ge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLnBsdWdpbi5zZXR0aW5ncy5vdXRwdXRGb2xkZXIgPSB2YWx1ZTtcbiAgICAgICAgICAgICAgICAgICAgYXdhaXQgdGhpcy5wbHVnaW4uc2F2ZVNldHRpbmdzKCk7XG4gICAgICAgICAgICAgICAgfSkpO1xuICAgIH1cbn1cbiJdLAogICJtYXBwaW5ncyI6ICI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBLHNCQUF3RztBQVN4RyxJQUFNLG1CQUFxQztBQUFBLEVBQ3ZDLFFBQVE7QUFBQSxFQUNSLFFBQVE7QUFBQSxFQUNSLFVBQVU7QUFBQSxFQUNWLGNBQWM7QUFDbEI7QUFFQSxJQUFxQixpQkFBckIsY0FBNEMsdUJBQU87QUFBQSxFQUFuRDtBQUFBO0FBQ0ksb0JBQTZCO0FBQUE7QUFBQSxFQUU3QixNQUFNLFNBQVM7QUFDWCxVQUFNLEtBQUssYUFBYTtBQUd4QixTQUFLLGNBQWMsU0FBUyxrQkFBa0IsWUFBWTtBQUN0RCxZQUFNLEtBQUssZ0JBQWdCO0FBQUEsSUFDL0IsQ0FBQztBQUdELFNBQUssV0FBVztBQUFBLE1BQ1osSUFBSTtBQUFBLE1BQ0osTUFBTTtBQUFBLE1BQ04sVUFBVSxZQUFZO0FBQ2xCLGNBQU0sS0FBSyxnQkFBZ0I7QUFBQSxNQUMvQjtBQUFBLElBQ0osQ0FBQztBQUdELFNBQUssY0FBYyxJQUFJLG1CQUFtQixLQUFLLEtBQUssSUFBSSxDQUFDO0FBQUEsRUFDN0Q7QUFBQSxFQUVBLE1BQU0sa0JBQWtCO0FBQ3BCLFVBQU0sT0FBTyxLQUFLLElBQUksVUFBVSxjQUFjO0FBQzlDLFFBQUksQ0FBQyxNQUFNO0FBQ1AsVUFBSSx1QkFBTyxpQkFBaUI7QUFDNUI7QUFBQSxJQUNKO0FBRUEsVUFBTSxVQUFVLE1BQU0sS0FBSyxJQUFJLE1BQU0sS0FBSyxJQUFJO0FBRTlDLFVBQU0sVUFBVTtBQUFBLE1BQ1osWUFBWSxLQUFLLFdBQVM7QUFBQSxNQUMxQixlQUFlLEtBQUssU0FBUztBQUFBLE1BQzdCLFdBQVc7QUFBQSxNQUNYLEtBQUs7QUFBQSxNQUNMLFFBQVE7QUFBQSxNQUNSLFNB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

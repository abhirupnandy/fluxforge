import { motion } from "framer-motion";
import { useTaskSync } from "../../features/tasks/hooks/use-task-sync";

import {
    useWorkspaceStore,
    type WorkspaceView,
} from "../../stores/workspace-store";

import { DashboardPanel } from "../workspace/dashboard-panel";
import { DownloadsPanel } from "../workspace/downloads-panel";
import { EncoderPanel } from "../workspace/encoder-panel";
import { QueuePanel } from "../workspace/queue-panel";
import { HistoryPanel } from "../workspace/history-panel";
import { PresetsPanel } from "../workspace/presets-panel";
import { SettingsPanel } from "../workspace/settings-panel";

const navItems: {
    id: WorkspaceView;
    label: string;
}[] = [
    {
        id: "dashboard",
        label: "Dashboard",
    },
    {
        id: "downloads",
        label: "Downloads",
    },
    {
        id: "encoder",
        label: "Encoder",
    },
    {
        id: "queue",
        label: "Queue",
    },
    {
        id: "history",
        label: "History",
    },
    {
        id: "presets",
        label: "Presets",
    },
    {
        id: "settings",
        label: "Settings",
    },
];

export function AppShell() {
    useTaskSync();

    const {
        currentView,
        setView,
    } = useWorkspaceStore();

    function renderPanel() {
        switch (currentView) {
            case "dashboard":
                return <DashboardPanel />;

            case "downloads":
                return <DownloadsPanel />;

            case "encoder":
                return <EncoderPanel />;

            case "queue":
                return <QueuePanel />;

            case "history":
                return <HistoryPanel />;

            case "presets":
                return <PresetsPanel />;

            case "settings":
                return <SettingsPanel />;

            default:
                return <DashboardPanel />;
        }
    }

    return (
        <div className="flex h-screen overflow-hidden bg-slate-950 text-white">
            <aside className="flex w-64 flex-col border-r border-slate-800 bg-slate-900">
                <div className="border-b border-slate-800 p-6">
                    <h1 className="text-3xl font-bold">
                        FluxForge
                    </h1>
                </div>

                <nav className="flex-1 space-y-2 p-4">
                    {navItems.map((item) => (
                        <button
                            key={item.id}
                            onClick={() => setView(item.id)}
                            className={`w-full rounded-xl px-4 py-3 text-left transition ${
                                currentView === item.id
                                    ? "bg-slate-800"
                                    : "hover:bg-slate-800/50"
                            }`}
                        >
                            {item.label}
                        </button>
                    ))}
                </nav>
            </aside>

            <main className="flex-1 overflow-auto p-8">
                <motion.div
                    key={currentView}
                    initial={{
                        opacity: 0,
                        y: 10,
                    }}
                    animate={{
                        opacity: 1,
                        y: 0,
                    }}
                    transition={{
                        duration: 0.15,
                    }}
                >
                    {renderPanel()}
                </motion.div>
            </main>
        </div>
    );
}
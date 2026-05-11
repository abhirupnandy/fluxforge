import { create } from "zustand";

export type WorkspaceView =
    | "dashboard"
    | "downloads"
    | "encoder"
    | "queue"
    | "history"
    | "presets"
    | "settings";

interface WorkspaceStore {
    currentView: WorkspaceView;

    setView: (view: WorkspaceView) => void;
}

export const useWorkspaceStore =
    create<WorkspaceStore>((set) => ({
        currentView: "dashboard",

        setView: (view) =>
            set({
                currentView: view,
            }),
    }));